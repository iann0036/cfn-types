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
TYPE_NAME = "Generic::Database::Schema"
TRACKING_TABLE_NAME = "database-schema-tracking-table"

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


def execute_changes(session, model, sqlhistory):
    try:
        region = model.ClusterArn.split(":")[3]
        rdsclient = session.client("rds", region_name=region)
        rdsdataclient = session.client("rds-data", region_name=region)
        secretsmanagerclient = session.client("secretsmanager", region_name=region)

        clusterinfo = rdsclient.describe_db_clusters(
            DBClusterIdentifier=model.ClusterArn.split(":").pop()
        )
        if clusterinfo['DBClusters'][0]['Engine'] != "aurora-postgresql":
            raise Exception("Invalid engine - only aurora-postgresql is supported")

        if model.Databases:
            for database in model.Databases:
                try:
                    rdsdataclient.execute_statement(
                        continueAfterTimeout=True,
                        database='postgres',
                        includeResultMetadata=True,
                        resourceArn=model.ClusterArn,
                        resultSetOptions={
                            'decimalReturnType': 'STRING'
                        },
                        secretArn=model.SecretArn,
                        sql='CREATE DATABASE {};'.format(database.Name)
                    )
                except rdsdataclient.exceptions.BadRequestException:
                    pass

        transactionid = rdsdataclient.begin_transaction(
            database='postgres',
            resourceArn=model.ClusterArn,
            secretArn=model.SecretArn
        )['transactionId']
        if model.Users:
            for user in model.Users:
                pwd = ''
                if user.SecretId:
                    secret = json.loads(secretsmanagerclient.get_secret_value(
                        SecretId=user.SecretId
                    )['SecretString'])
                    pwd = " PASSWORD '{}'".format(secret['password'].replace("\\", "\\\\").replace("'", "\\'"))
                sql = """
DO
$do$
BEGIN
IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles
    WHERE rolname = '{username}') THEN
    CREATE ROLE {username} LOGIN{pwd};
END IF;
END
$do$;
    """.format(username=user.Name, pwd=pwd)

                rdsdataclient.execute_statement(
                    continueAfterTimeout=True,
                    database='postgres',
                    includeResultMetadata=True,
                    resourceArn=model.ClusterArn,
                    resultSetOptions={
                        'decimalReturnType': 'STRING'
                    },
                    secretArn=model.SecretArn,
                    sql='{};'.format(sql),
                    transactionId=transactionid
                )

                if user.Grants:
                    for grant in user.Grants:
                        if not grant.Table:
                            rdsdataclient.execute_statement(
                                continueAfterTimeout=True,
                                database='postgres',
                                includeResultMetadata=True,
                                resourceArn=model.ClusterArn,
                                resultSetOptions={
                                    'decimalReturnType': 'STRING'
                                },
                                secretArn=model.SecretArn,
                                sql="GRANT {} ON DATABASE {} TO {};".format(', '.join(grant.Privileges), grant.Database, user.Name),
                                transactionId=transactionid
                            )
                if user.SuperUser:
                    rdsdataclient.execute_statement(
                        continueAfterTimeout=True,
                        database='postgres',
                        includeResultMetadata=True,
                        resourceArn=model.ClusterArn,
                        resultSetOptions={
                            'decimalReturnType': 'STRING'
                        },
                        secretArn=model.SecretArn,
                        sql="GRANT rds_superuser TO {};".format(user.Name),
                        transactionId=transactionid
                    )
        if model.SQL:
            for sql in model.SQL:
                if 'postgres' in sqlhistory and model.SQLIdempotency != "RUN_ONCE":
                    if sql in sqlhistory['postgres']['SS']:
                        continue

                rdsdataclient.execute_statement(
                    continueAfterTimeout=True,
                    database='postgres',
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
        if model.Databases:
            for database in model.Databases:
                transactionid = rdsdataclient.begin_transaction(
                    database=database.Name,
                    resourceArn=model.ClusterArn,
                    secretArn=model.SecretArn
                )['transactionId']
                if database.Extensions:
                    for extension in database.Extensions:
                        rdsdataclient.execute_statement(
                            continueAfterTimeout=True,
                            database=database.Name,
                            includeResultMetadata=True,
                            resourceArn=model.ClusterArn,
                            resultSetOptions={
                                'decimalReturnType': 'STRING'
                            },
                            secretArn=model.SecretArn,
                            sql='CREATE EXTENSION IF NOT EXISTS "{}";'.format(extension),
                            transactionId=transactionid
                        )
                if database.Tables:
                    for table in database.Tables:
                        primarykey = ''
                        if table.PrimaryKey:
                            primarykey = '{} {} PRIMARY KEY{}'.format(table.PrimaryKey.Name, table.PrimaryKey.Type, (' DEFAULT {}'.format(table.PrimaryKey.Default) if table.PrimaryKey.Default else ''))
                        rdsdataclient.execute_statement(
                            continueAfterTimeout=True,
                            database=database.Name,
                            includeResultMetadata=True,
                            resourceArn=model.ClusterArn,
                            resultSetOptions={
                                'decimalReturnType': 'STRING'
                            },
                            secretArn=model.SecretArn,
                            sql='CREATE TABLE IF NOT EXISTS {tablename}({primarykey});'.format(tablename=table.Name, primarykey=primarykey),
                            transactionId=transactionid
                        )
                        if table.Columns:
                            for column in table.Columns:
                                rdsdataclient.execute_statement(
                                    continueAfterTimeout=True,
                                    database=database.Name,
                                    includeResultMetadata=True,
                                    resourceArn=model.ClusterArn,
                                    resultSetOptions={
                                        'decimalReturnType': 'STRING'
                                    },
                                    secretArn=model.SecretArn,
                                    sql='ALTER TABLE {tablename} ADD COLUMN IF NOT EXISTS {columnname} {typ}{nullable}{default};'.format(tablename=table.Name, columnname=column.Name, typ=column.Type, nullable=("" if column.Nullable else " NOT NULL"), default=(" DEFAULT {}".format(column.Default) if column.Default else "")),
                                    transactionId=transactionid
                                )
                if model.Users:
                    for user in model.Users:
                        if user.Grants:
                            for grant in user.Grants:
                                if grant.Database == database.Name and grant.Table:
                                    rdsdataclient.execute_statement(
                                        continueAfterTimeout=True,
                                        database=grant.Database,
                                        includeResultMetadata=True,
                                        resourceArn=model.ClusterArn,
                                        resultSetOptions={
                                            'decimalReturnType': 'STRING'
                                        },
                                        secretArn=model.SecretArn,
                                        sql="GRANT {} ON TABLE {} TO {};".format(', '.join(grant.Privileges), grant.Table, user.Name),
                                        transactionId=transactionid
                                    )
                if database.SQL:
                    for sql in database.SQL:
                        if database.Name in sqlhistory and model.SQLIdempotency != "RUN_ONCE":
                            if sql in sqlhistory[database.Name]['SS']:
                                continue
                        
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
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")


def generate_sql_history_block(model):
    ret = {
        'M': {}
    }

    if model.SQL:
        ret['M']['postgres'] = {
            'SS': list(model.SQL)
        }

    if model.Databases:
        for database in model.Databases:
            if database.SQL:
                ret['M'][database.Name] = {
                    'SS': list(database.SQL)
                }

    return ret


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
        execute_changes(session, model, {})

        ddbclient = session.client('dynamodb')

        ddbclient.put_item(
            TableName=TRACKING_TABLE_NAME,
            Item={
                'executionId': {
                    'S': executionId
                },
                'lastUpdated': {
                    'N': str(int(time.time()))
                },
                'clusterArn': {
                    'S': model.ClusterArn
                },
                'sqlHistory': generate_sql_history_block(model)
            }
        )
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    model.ClusterArn = None
    model.SecretArn = None
    model.Databases = None
    model.SQL = None
    model.Users = None
    model.SQLIdempotency = None

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

    print(model)

    ensure_tracking_table_exists(session)
    if not model.ExecutionId:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)

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

        model.ClusterArn = item['Item']['clusterArn']['S']

        execute_changes(session, model, item['Item']['sqlHistory']['M'])
        
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
                },
                'sqlHistory': {
                    'Value': generate_sql_history_block(model),
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
    model.SQLIdempotency = None

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

    ensure_tracking_table_exists(session)
    if not model.ExecutionId:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
    
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
    if not model.ExecutionId:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.ExecutionId)
    
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
            model = ResourceModel(ExecutionId=item['executionId']['S'], ClusterArn=None, SecretArn=None, Databases=None, SQL=None, Users=None, SQLIdempotency=None)
            models.append(model)
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )
