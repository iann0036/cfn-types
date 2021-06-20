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
TYPE_NAME = "Generic::Transcribe::Vocabulary"

resource = Resource(TYPE_NAME, ResourceModel)
test_entrypoint = resource.test_entrypoint


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

    if callback_context.get('pending'):
        return read_handler(session, request, callback_context)
    
    try:
        client = session.client("transcribe")
        if model.Phrases is not None:
            client.create_vocabulary(
                VocabularyName=model.VocabularyName,
                LanguageCode=model.LanguageCode,
                Phrases=model.Phrases
            )
        else:
            client.create_vocabulary(
                VocabularyName=model.VocabularyName,
                LanguageCode=model.LanguageCode,
                VocabularyFileUri=model.VocabularyFileUri
            )
    except client.exceptions.ConflictException as e:
        raise exceptions.AlreadyExists(type_name=TYPE_NAME, identifier=model.VocabularyName)
    except Exception as e:
        raise exceptions.InternalFailure(f"{e}")

    return read_handler(session, request, callback_context)


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

    if callback_context.get('pending'):
        return read_handler(session, request, callback_context)
    
    try:
        client = session.client("transcribe")
        if model.Phrases is not None:
            client.update_vocabulary(
                VocabularyName=model.VocabularyName,
                LanguageCode=model.LanguageCode,
                Phrases=model.Phrases
            )
        else:
            client.update_vocabulary(
                VocabularyName=model.VocabularyName,
                LanguageCode=model.LanguageCode,
                VocabularyFileUri=model.VocabularyFileUri
            )
    except client.exceptions.NotFoundException as e:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.VocabularyName)
    except Exception as e:
        if "t be found" in str(e):
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.VocabularyName)
        raise exceptions.InternalFailure(f"{e}")
    
    return read_handler(session, request, callback_context)


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
    
    try:
        client = session.client("transcribe")
        client.get_vocabulary(
            VocabularyName=model.VocabularyName
        )
        client.delete_vocabulary(
            VocabularyName=model.VocabularyName
        )
        progress.status = OperationStatus.SUCCESS
    except client.exceptions.NotFoundException as e:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.VocabularyName)
    except Exception as e:
        if "t be found" in str(e):
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.VocabularyName)
        raise exceptions.InternalFailure(f"{e}")

    return progress


@resource.handler(Action.READ)
def read_handler(
    session: Optional[SessionProxy],
    request: ResourceHandlerRequest,
    callback_context: MutableMapping[str, Any],
) -> ProgressEvent:
    model = request.desiredResourceState

    model.Phrases = None
    model.VocabularyFileUri = None
    
    try:
        client = session.client("transcribe")
        resp = client.get_vocabulary(
            VocabularyName=model.VocabularyName
        )

        if resp['VocabularyState'] == "PENDING":
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resourceModel=model,
                callbackContext={
                    "pending": True
                }
            )
        elif resp['VocabularyState'] == "FAILED":
            return ProgressEvent(
                status=OperationStatus.FAILED,
                message=resp['FailureReason'],
                resourceModel=model,
            )
        else:
            model.LanguageCode = resp['LanguageCode']
    except client.exceptions.NotFoundException as e:
        raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.VocabularyName)
    except Exception as e:
        if "t be found" in str(e):
            raise exceptions.NotFound(type_name=TYPE_NAME, identifier=model.VocabularyName)
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

    client = session.client("transcribe")
    resp = client.list_vocabularies(
        MaxResults=100,
        StateEquals='READY'
    )
    if 'Vocabularies' in resp:
        for vocabulary in resp['Vocabularies']:
            model = ResourceModel(
                VocabularyName=vocabulary['VocabularyName'],
                LanguageCode=vocabulary['LanguageCode'],
                Phrases=None,
                VocabularyFileUri=None
            )
            models.append(model)

    return ProgressEvent(
        status=OperationStatus.SUCCESS,
        resourceModels=models,
    )
