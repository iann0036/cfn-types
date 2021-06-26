import logging
import uuid
import time
import json
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
        secretsmanagerclient = session.client("secretsmanager")
        ddbclient = session.client('dynamodb')

        for database in model.Databases:
            rdsdataclient.execute_statement(
                continueAfterTimeout=True,
                database='postgres',
                includeResultMetadata=True,
                parameters=[
                    {
                        'name': 'name',
                        'value': {
                            'stringValue': database.Name
                        }
                    },
                ],
                resourceArn=model.ClusterArn,
                resultSetOptions={
                    'decimalReturnType': 'STRING'
                },
                secretArn=model.SecretArn,
                sql='CREATE DATABASE :name;'
            )

        transactionid = rdsdataclient.begin_transaction(
            database='postgres',
            resourceArn=model.ClusterArn,
            secretArn=model.SecretArn
        )['transactionId']
        for user in database.Users:
            parameters = [
                {
                    'name': 'username',
                    'value': {
                        'stringValue': user.Name
                    }
                },
            ]
            sql = """
            DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = ':username') THEN
      CREATE ROLE :username LOGIN{};
   END IF;
END
$do$;
""".format(" PASSWORD ':password'" if user.SecretId else '')
            if user.SecretId:
                secret = json.loads(secretsmanagerclient.get_secret_value(
                    SecretId=user.SecretId
                )['SecretString'])
                parameters.append({
                    'name': 'password',
                    'value': {
                        'stringValue': secret['password']
                    }
                })

            rdsdataclient.execute_statement(
                continueAfterTimeout=True,
                database='postgres',
                includeResultMetadata=True,
                parameters=parameters,
                resourceArn=model.ClusterArn,
                resultSetOptions={
                    'decimalReturnType': 'STRING'
                },
                secretArn=model.SecretArn,
                sql='{};'.format(sql),
                transactionId=transactionid
            )

            for grant in user.Grants:
                rdsdataclient.execute_statement(
                    continueAfterTimeout=True,
                    database='postgres',
                    includeResultMetadata=True,
                    parameters=[
                        {
                            'name': 'database',
                            'value': {
                                'stringValue': grant.Database
                            }
                        },
                        {
                            'name': 'user',
                            'value': {
                                'stringValue': user.Name
                            }
                        },
                    ],
                    resourceArn=model.ClusterArn,
                    resultSetOptions={
                        'decimalReturnType': 'STRING'
                    },
                    secretArn=model.SecretArn,
                    sql="GRANT {} ON DATABASE ':database' TO ':user';".format(', '.join(grant.Privileges)),
                    transactionId=transactionid
                )
            if user.SuperUser:
                rdsdataclient.execute_statement(
                    continueAfterTimeout=True,
                    database='postgres',
                    includeResultMetadata=True,
                    parameters=[
                        {
                            'name': 'user',
                            'value': {
                                'stringValue': user.Name
                            }
                        },
                    ],
                    resourceArn=model.ClusterArn,
                    resultSetOptions={
                        'decimalReturnType': 'STRING'
                    },
                    secretArn=model.SecretArn,
                    sql="GRANT rds_superuser TO ':user';",
                    transactionId=transactionid
                )
        for database in model.Databases:
            for extension in database.Extensions:
                rdsdataclient.execute_statement(
                    continueAfterTimeout=True,
                    database=database.Name,
                    includeResultMetadata=True,
                    parameters=[
                        {
                            'name': 'extension',
                            'value': {
                                'stringValue': extension
                            }
                        },
                    ],
                    resourceArn=model.ClusterArn,
                    resultSetOptions={
                        'decimalReturnType': 'STRING'
                    },
                    secretArn=model.SecretArn,
                    sql='CREATE EXTENSION IF NOT EXISTS :extension;',
                    transactionId=transactionid
                )
            for sql in database.SQL:
                rdsdataclient.execute_statement(
                    continueAfterTimeout=True,
                    database=database.Name,
                    includeResultMetadata=True,
                    resourceArn=model.ClusterArn,
                    resultSetOptions={
                        'decimalReturnType': 'STRING'
                    },
                    secretArn=model.SecretArn,
                    sql=sql,
                    transactionId=transactionid
                )
        rdsdataclient.commit_transaction(
            resourceArn=model.ClusterArn,
            secretArn=model.SecretArn,
            transactionId=transactionid
        )
        
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
        raise e

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
    models = []

    ensure_tracking_table_exists(session)

    try:
        ddbclient = session.client('dynamodb')
        
        items = ddbclient.scan(
            TableName=TRACKING_TABLE_NAME
        )['Items']

        for item in items:
            model = ResourceModel(ExecutionId=item['executionId']['S'])
            models.append(model)
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )
