import logging
import json
import requests
from typing import Any, MutableMapping, Optional

from cloudformation_cli_python_lib import (
    Action,
    HandlerErrorCode,
    OperationStatus,
    ProgressEvent,
    Resource,
    SessionProxy,
    exceptions,
    identifier_utils,
)

from .models import ResourceHandlerRequest, ResourceModel, TypeConfigurationModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Stocks::Orders::MarketOrder"

resource = Resource(TYPE_NAME, ResourceModel, TypeConfigurationModel)
test_entrypoint = resource.test_entrypoint


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    config = request.typeConfiguration
    model.Notes = None

    try:
        req = requests.post(
            url='https://{}/v2/orders'.format(("api.alpaca.markets" if config.Credentials.Environment == "LIVE" else "paper-api.alpaca.markets")),
            headers={
                'APCA-API-KEY-ID': config.Credentials.ApiKey,
                'APCA-API-SECRET-KEY': config.Credentials.SecretKey
            },
            json={
                'symbol': model.Symbol,
                'qty': model.Quantity,
                'side': 'buy',
                'type': 'market',
                'time_in_force': 'day'
            })
        order = json.loads(req.text)
        model.Id = order['id']
        model.FilledQuantity = 0
        model.FilledValue = 0
        model.CurrentValue = 0
        model.FilledAt = order['filled_at']

    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.UPDATE)
def update_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    config = request.typeConfiguration
    model.Notes = None
    
    return read_handler(session, request, callback_context)


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    config = request.typeConfiguration
    model.Notes = None

    if not model.Id:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
    
    try:
        req = requests.get(
            url='https://{}/v2/orders/{}'.format(("api.alpaca.markets" if config.Credentials.Environment == "LIVE" else "paper-api.alpaca.markets"), model.Id),
            headers={
                'APCA-API-KEY-ID': config.Credentials.ApiKey,
                'APCA-API-SECRET-KEY': config.Credentials.SecretKey
            })
        if req.status_code == 404:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
        order = json.loads(req.text)
        if 'code' in order and order['code'] in [40410000, 40010001]:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
        if 'id' not in order:
            raise exceptions.InternalFailure(f"Internal failure")
        if order['canceled_at'] is not None:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
        
        req = requests.delete(
            url='https://{}/v2/orders/{}'.format(("api.alpaca.markets" if config.Credentials.Environment == "LIVE" else "paper-api.alpaca.markets"), model.Id),
            headers={
                'APCA-API-KEY-ID': config.Credentials.ApiKey,
                'APCA-API-SECRET-KEY': config.Credentials.SecretKey
            })
        if req.status_code < 200 or req.status_code > 299:
            if req.status_code == 422:
                req = requests.post(
                    url='https://{}/v2/orders'.format(("api.alpaca.markets" if config.Credentials.Environment == "LIVE" else "paper-api.alpaca.markets")),
                    headers={
                        'APCA-API-KEY-ID': config.Credentials.ApiKey,
                        'APCA-API-SECRET-KEY': config.Credentials.SecretKey
                    },
                    json={
                        'symbol': model.Symbol,
                        'qty': model.FilledQuantity,
                        'side': 'sell',
                        'type': 'market',
                        'time_in_force': 'day'
                    })
                if req.status_code < 200 or req.status_code > 299:
                    raise exceptions.InternalFailure(f"Internal failure")
            else:
                raise exceptions.InternalFailure(f"Internal failure")

    except Exception as e:
        if not isinstance(e, exceptions.NotFound):
            raise exceptions.InternalFailure(f"{e}")
        raise e

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=None,
    )


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    config = request.typeConfiguration
    model.Notes = None
    
    try:
        req = requests.get(
            url='https://{}/v2/orders/{}'.format(("api.alpaca.markets" if config.Credentials.Environment == "LIVE" else "paper-api.alpaca.markets"), model.Id),
            headers={
                'APCA-API-KEY-ID': config.Credentials.ApiKey,
                'APCA-API-SECRET-KEY': config.Credentials.SecretKey
            })
        if req.status_code == 404:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
        order = json.loads(req.text)
        if 'code' in order and order['code'] in [40410000, 40010001]:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
        if 'id' not in order:
            raise exceptions.InternalFailure(f"Internal failure")
        if order['canceled_at'] is not None:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.Id)
        model.Symbol = order['symbol']
        model.Quantity = float(order['qty'])
        model.FilledQuantity = float(order['filled_qty'])
        if order['filled_avg_price'] == None:
            model.FilledValue = 0
            model.CurrentValue = 0
        else:
            model.FilledValue = float(order['filled_qty']) * float(order['filled_avg_price'])
            req = requests.get(
                url='https://data.alpaca.markets/v2/stocks/{}/trades/latest'.format(order['symbol']),
                headers={
                    'APCA-API-KEY-ID': config.Credentials.ApiKey,
                    'APCA-API-SECRET-KEY': config.Credentials.SecretKey
                })
            trade = json.loads(req.text)
            model.CurrentValue = float(order['filled_qty']) * float(trade['trade']['p'])
        model.FilledAt = order['filled_at']

    except Exception as e:
        if not isinstance(e, exceptions.NotFound):
            raise exceptions.InternalFailure(f"{e}")
        raise e

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.LIST)
def list_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    config = request.typeConfiguration
    models = []
    
    try:
        req = requests.get(
            url='https://{}/v2/orders'.format(("api.alpaca.markets" if config.Credentials.Environment == "LIVE" else "paper-api.alpaca.markets")),
            headers={
                'APCA-API-KEY-ID': config.Credentials.ApiKey,
                'APCA-API-SECRET-KEY': config.Credentials.SecretKey
            })
        orders = json.loads(req.text)

        for order in orders:
            model = ResourceModel(
                Id=order['id'],
                Quantity=float(order['qty']),
                Symbol=order['symbol'],
                Notes=None,
                FilledQuantity=float(order['filled_qty']),
                FilledValue=0,
                CurrentValue=0,
                FilledAt=order['filled_at'],
            )
            if order['filled_avg_price'] != None:
                model.FilledValue = float(order['filled_qty']) * float(order['filled_avg_price'])
                req = requests.get(
                    url='https://data.alpaca.markets/v2/stocks/{}/trades/latest'.format(order['symbol']),
                    headers={
                        'APCA-API-KEY-ID': config.Credentials.ApiKey,
                        'APCA-API-SECRET-KEY': config.Credentials.SecretKey
                    })
                trade = json.loads(req.text)
                model.CurrentValue = float(order['filled_qty']) * float(trade['trade']['p'])
            
            models.append(model)

    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )