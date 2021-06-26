import logging
import uuid
import time
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

from .models import ResourceHandlerRequest, ResourceModel

# Use this logger to forward log messages to CloudWatch Logs.
LOG = logging.getLogger(__name__)
TYPE_NAME = "Generic::Aurora::Execution"
TRACKING_TABLE_NAME = "aurora-execution-tracking-table"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


def ensure_tracking_table_exists(session: Optional[SessionProxy]):
    ddbclient = session.client('dynamodb')

    try:
        ddbclient.describe_table(
            TableName=TRACKING_TABLE_NAME
        )
    except ddbclient.exceptions.ResourceNotFoundException:
        ddbclient.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': 'executionId',
                    'AttributeType': 'S'
                },
            ],
            TableName=TRACKING_TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'executionId',
                    'KeyType': 'HASH'
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        ddbclient.get_waiter('table_exists').wait(TableName=TRACKING_TABLE_NAME)


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    ensure_tracking_table_exists(session)

    executionId = str(uuid.uuid4())
    model.ExecutionId = executionId
    
    try:
        rdsdataclient = session.client("rds-data")
        ddbclient = session.client('dynamodb')
        
        ddbclient.put_item(
            TableName=TRACKING_TABLE_NAME,
            Item={
                'executionId': {
                    'S': executionId
                },
                'lastUpdated': {
                    'N': str(int(time.time()))
                }
            }
        )
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    model.ClusterArn = None
    model.SecretArn = None
    model.Databases = None
    model.SQL = None
    model.Users = None

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
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=model,
    )

    ensure_tracking_table_exists(session)

    try:
        rdsdataclient = session.client("rds-data")
        ddbclient = session.client('dynamodb')

        item = ddbclient.get_item(
            TableName=TRACKING_TABLE_NAME,
            Key={
                'executionId': {
                    'S': model.ExecutionId
                }
            }
        )
        if 'Item' not in item:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
        
        ddbclient.update_item(
            TableName=TRACKING_TABLE_NAME,
            Key={
                'executionId': {
                    'S': model.ExecutionId
                }
            },
            AttributeUpdates={
                'lastUpdated': {
                    'Value': {
                        'N': str(int(time.time()))
                    },
                    'Action': 'PUT'
                }
            }
        )
    except ddbclient.exceptions.ResourceNotFoundException:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
    except Exception as e:
        if not isinstance(e, exceptions.NotFound):
            raise exceptions.InternalFailure(f"{e}")

    model.ClusterArn = None
    model.SecretArn = None
    model.Databases = None
    model.SQL = None
    model.Users = None

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModel=model,
    )


@resource.handler(Action.DELETE)
def delete_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    progress: ProgressEvent = ProgressEvent(
        status=OperationStatus.IN_PROGRESS,
        resourceModel=None,
    )

    ensure_tracking_table_exists(session)
    
    try:
        ddbclient = session.client('dynamodb')

        item = ddbclient.get_item(
            TableName=TRACKING_TABLE_NAME,
            Key={
                'executionId': {
                    'S': model.ExecutionId
                }
            }
        )
        if 'Item' not in item:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
        
        ddbclient.delete_item(
            TableName=TRACKING_TABLE_NAME,
            Key={
                'executionId': {
                    'S': model.ExecutionId
                }
            }
        )
    except ddbclient.exceptions.ResourceNotFoundException:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
    except Exception as e:
        if not isinstance(e, exceptions.NotFound):
            raise exceptions.InternalFailure(f"{e}")

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

    ensure_tracking_table_exists(session)
    
    try:
        ddbclient = session.client('dynamodb')
        
        item = ddbclient.get_item(
            TableName=TRACKING_TABLE_NAME,
            Key={
                'executionId': {
                    'S': model.ExecutionId
                }
            }
        )
        if 'Item' not in item:
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
    except ddbclient.exceptions.ResourceNotFoundException:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
    except Exception as e:
        if not isinstance(e, exceptions.NotFound):
            raise exceptions.InternalFailure(f"{e}")

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
    models = []

    ensure_tracking_table_exists(session)

    try:
        ddbclient = session.client('dynamodb')
        
        ddbclient.scan(
            TableName=TRACKING_TABLE_NAME
        )
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )
