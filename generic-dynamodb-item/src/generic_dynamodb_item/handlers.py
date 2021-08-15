import logging
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
TYPE_NAME = "Generic::DynamoDB::Item"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


def attribute_to_item_property(attribute):
    prop = {}
    
    if 'S' in attribute.Value:
        prop['S'] = attribute.Value.S
    elif 'N' in attribute.Value:
        prop['N'] = attribute.Value.N
    elif 'B' in attribute.Value:
        prop['B'] = attribute.Value.B.encode()
    elif 'SS' in attribute.Value:
        prop['SS'] = attribute.Value.SS
    elif 'NS' in attribute.Value:
        prop['NS'] = attribute.Value.NS
    elif 'BS' in attribute.Value:
        prop['BS'] = []
        for listitem in attribute.Value.BS:
            prop['BS'].append(listitem.encode())
    elif 'M' in attribute.Value:
        prop['M'] = attribute_to_item_property(attribute.Value.M)
    elif 'L' in attribute.Value:
        prop['L'] = []
        for listitem in attribute.Value.L:
            prop['L'].append(attribute_to_item_property(listitem))
    elif 'NULL' in attribute.Value:
        prop['NULL'] = attribute.Value.NULL
    elif 'BOOL' in attribute.Value:
        prop['BOOL'] = attribute.Value.BOOL
    
    return prop


def item_property_to_attribute_value(prop):
    attr = {}

    if 'S' in prop:
        attr['S'] = prop.S
    elif 'N' in prop:
        attr['N'] = prop.N
    elif 'B' in prop:
        attr['B'] = prop.B.decode('base64', 'strict')
    elif 'SS' in prop:
        attr['SS'] = prop.SS
    elif 'NS' in prop:
        attr['NS'] = prop.NS
    elif 'BS' in prop:
        attr['BS'] = []
        for listitem in prop.BS:
            attr['BS'].append(listitem.decode('base64', 'strict'))
    elif 'M' in prop:
        attr['M'] = []
        for key in prop.M.keys():
            attr['M'].append(
                Name=key,
                Value=item_property_to_attribute_value(prop.M[key])
            )
    elif 'L' in prop:
        attr['L'] = []
        for listitem in prop.L:
            item = []
            for key in listitem.keys():
                item.append(
                    Name=key,
                    Value=item_property_to_attribute_value(listitem[key])
                )
            attr['L'].append(item)
    elif 'NULL' in prop:
        attr['NULL'] = prop.NULL
    elif 'BOOL' in prop:
        attr['BOOL'] = prop.BOOL

    return attr


def get_keys(client, tablename):
    partition_key = None
    sort_key = None
    partition_key_type = None
    sort_key_type = None

    table = client.describe_table(
        TableName=tablename
    )['Table']

    for keytype in table['KeySchema']:
        if keytype['KeyType'] == "HASH":
            partition_key = keytype['AttributeName']
        elif keytype['KeyType'] == "RANGE":
            sort_key = keytype['AttributeName']

    for attrdef in table['AttributeDefinitions']:
        if attrdef['AttributeName'] == partition_key:
            partition_key_type = attrdef['AttributeType']
        elif attrdef['AttributeName'] == sort_key:
            sort_key_type = attrdef['AttributeType']

    return partition_key, sort_key, partition_key_type, sort_key_type


@resource.handler(Action.CREATE)
def create_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState
    
    try:
        client = None
        if isinstance(session, SessionProxy):
            client = session.client("dynamodb")
        else:
            raise Exception("Session proxy not available")
        
        partition_key, sort_key, _, _ = get_keys(client, model.TableName)

        item = {}
        for attribute in model.Attributes:
            item[attribute.Name] = attribute_to_item_property(attribute.Value)
        
        client.put_item(
            TableName=model.TableName,
            Item=item,
            ConditionExpression="attribute_not_exists(#pk)",
            ExpressionAttributeNames={
                "#pk": partition_key
            }
        )

        model.PartitionKey = item[partition_key].values()[0]
        model.SortKey = ""
        if sort_key is not None:
            model.SortKey = item[sort_key].values()[0]
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
    oldModel = request.previousResourceState
    
    try:
        client = None
        if isinstance(session, SessionProxy):
            client = session.client("dynamodb")
        else:
            raise Exception("Session proxy not available")
        
        partition_key, sort_key, _, _ = get_keys(client, model.TableName)

        oldkey = {}
        for attribute in oldModel.Attributes:
            if attribute.Name == partition_key or attribute.Name == sort_key:
                oldkey[attribute.Name] = attribute_to_item_property(attribute.Value)

        item = {}
        for attribute in model.Attributes:
            item[attribute.Name] = attribute_to_item_property(attribute.Value)

        if item[partition_key].values()[0] != oldkey[partition_key].values()[0] or (sort_key != None and item[sort_key].values()[0] != oldkey[sort_key].values()[0]):
            client.delete_item(
                TableName=model.TableName,
                Key=oldkey
            )
        
        client.put_item(
            TableName=model.TableName,
            Item=item,
            ConditionExpression="attribute_exists(#pk)",
            ExpressionAttributeNames={
                "#pk": partition_key
            }
        )

        model.PartitionKey = item[partition_key].values()[0]
        model.SortKey = ""
        if sort_key is not None:
            model.SortKey = item[sort_key].values()[0]
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

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

    try:
        client = None
        if isinstance(session, SessionProxy):
            client = session.client("dynamodb")
        else:
            raise Exception("Session proxy not available")
        
        partition_key, sort_key, _, _ = get_keys(client, model.TableName)

        key = {}
        for attribute in model.Attributes:
            if attribute.Name == partition_key or attribute.Name == sort_key:
                key[attribute.Name] = attribute_to_item_property(attribute.Value)

        client.delete_item(
            TableName=model.TableName,
            Key=key
        )
    except Exception as e:
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
    
    try:
        client = None
        if isinstance(session, SessionProxy):
            client = session.client("dynamodb")
        else:
            raise Exception("Session proxy not available")

        partition_key, sort_key, partition_key_type, sort_key_type = get_keys(client, model.TableName)

        key = {}
        key[partition_key] = {}
        key[partition_key][partition_key_type] = model.PartitionValue
        if sort_key is not None:
            key[sort_key] = {}
            key[sort_key][sort_key_type] = model.SortValue
        item = client.get_item(
            TableName=model.TableName,
            Key=key
        )['Item']

        model.Attributes = []
        for key in item.keys():
            model.Attributes.append(
                Name=key,
                Value=item_property_to_attribute_value(item[key])
            )
    except Exception as e:
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

    try:
        client = None
        if isinstance(session, SessionProxy):
            client = session.client("dynamodb")
        else:
            raise Exception("Session proxy not available")
        
        tables = []
        try:
            tables = client.list_tables()['TableNames']
        except:
            pass

        for table in tables:
            items = []
            partition_key = None
            sort_key = None
            try:
                partition_key, sort_key, _, _ = get_keys(client, table)
                items = client.scan(
                    TableName=table
                )['Items']
            except:
                pass

            for item in items:
                attributes = []
                for key in item.keys():
                    attributes.append(
                        Name=key,
                        Value=item_property_to_attribute_value(item[key])
                    )
                model = ResourceModel(
                    TableName=table,
                    Attributes=attributes,
                    PartitionValue=item[partition_key].values()[0],
                    SortValue=item[sort_key].values()[0],
                )
                models.append(model)
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )
