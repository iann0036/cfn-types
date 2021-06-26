# DO NOT modify this file by hand, changes will be overwritten
import sys
from dataclasses import dataclass
from inspect import getmembers, isclass
from typing import (
    AbstractSet,
    Any,
    Generic,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Type,
    TypeVar,
)

from cloudformation_cli_python_lib.interface import (
    BaseModel,
    BaseResourceHandlerRequest,
)
from cloudformation_cli_python_lib.recast import recast_object
from cloudformation_cli_python_lib.utils import deserialize_list

T = TypeVar("T")


def set_or_none(value: Optional[Sequence[T]]) -> Optional[AbstractSet[T]]:
    if value:
        return set(value)
    return None


@dataclass
class ResourceHandlerRequest(BaseResourceHandlerRequest):
    # pylint: disable=invalid-name
    desiredResourceState: Optional["ResourceModel"]
    previousResourceState: Optional["ResourceModel"]
    typeConfiguration: Optional["TypeConfigurationModel"]


@dataclass
class ResourceModel(BaseModel):
    Id: Optional[str]
    Quantity: Optional[float]
    Symbol: Optional[str]
    Notes: Optional[str]
    FilledQuantity: Optional[str]
    FilledValue: Optional[str]
    CurrentValue: Optional[str]
    FilledAt: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_ResourceModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_ResourceModel"]:
        if not json_data:
            return None
        dataclasses = {n: o for n, o in getmembers(sys.modules[__name__]) if isclass(o)}
        recast_object(cls, json_data, dataclasses)
        return cls(
            Id=json_data.get("Id"),
            Quantity=json_data.get("Quantity"),
            Symbol=json_data.get("Symbol"),
            Notes=json_data.get("Notes"),
            FilledQuantity=json_data.get("FilledQuantity"),
            FilledValue=json_data.get("FilledValue"),
            CurrentValue=json_data.get("CurrentValue"),
            FilledAt=json_data.get("FilledAt"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class TypeConfigurationModel(BaseModel):
    Credentials: Optional["_Credentials"]

    @classmethod
    def _deserialize(
        cls: Type["_TypeConfigurationModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TypeConfigurationModel"]:
        if not json_data:
            return None
        return cls(
            Credentials=Credentials._deserialize(json_data.get("Credentials")),
        )


# work around possible type aliasing issues when variable has same name as a model
_TypeConfigurationModel = TypeConfigurationModel


@dataclass
class Credentials(BaseModel):
    ApiKey: Optional[str]
    SecretKey: Optional[str]
    Environment: Optional[str]

    @classmethod
    def _deserialize(
        cls: Type["_Credentials"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Credentials"]:
        if not json_data:
            return None
        return cls(
            ApiKey=json_data.get("ApiKey"),
            SecretKey=json_data.get("SecretKey"),
            Environment=json_data.get("Environment"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Credentials = Credentials


