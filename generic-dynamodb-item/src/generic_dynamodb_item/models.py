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
    TableName: Optional[str]
    Attributes: Optional[Sequence["_Attribute"]]
    PartitionValue: Optional[str]
    SortValue: Optional[str]

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
            TableName=json_data.get("TableName"),
            Attributes=deserialize_list(json_data.get("Attributes"), Attribute),
            PartitionValue=json_data.get("PartitionValue"),
            SortValue=json_data.get("SortValue"),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class Attribute(BaseModel):
    Name: Optional[str]
    Value: Optional["_AttributeValue"]

    @classmethod
    def _deserialize(
        cls: Type["_Attribute"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Attribute"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Value=AttributeValue._deserialize(json_data.get("Value")),
        )


# work around possible type aliasing issues when variable has same name as a model
_Attribute = Attribute


@dataclass
class AttributeValue(BaseModel):
    S: Optional[str]
    N: Optional[str]
    B: Optional[str]
    SS: Optional[Sequence[str]]
    NS: Optional[Sequence[str]]
    BS: Optional[Sequence[str]]
    M: Optional[Sequence["_Attribute2"]]
    L: Optional[Sequence[Sequence["_Attribute2"]]]
    NULL: Optional[bool]
    BOOL: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_AttributeValue"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AttributeValue"]:
        if not json_data:
            return None
        return cls(
            S=json_data.get("S"),
            N=json_data.get("N"),
            B=json_data.get("B"),
            SS=json_data.get("SS"),
            NS=json_data.get("NS"),
            BS=json_data.get("BS"),
            M=deserialize_list(json_data.get("M"), Attribute2),
            L=deserialize_list(json_data.get("L"), <ResolvedType(ContainerType.MODEL, Attribute2)>),
            NULL=json_data.get("NULL"),
            BOOL=json_data.get("BOOL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AttributeValue = AttributeValue


@dataclass
class Attribute2(BaseModel):
    Name: Optional[str]
    Value: Optional["_AttributeValue2"]

    @classmethod
    def _deserialize(
        cls: Type["_Attribute2"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Attribute2"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Value=AttributeValue2._deserialize(json_data.get("Value")),
        )


# work around possible type aliasing issues when variable has same name as a model
_Attribute2 = Attribute2


@dataclass
class AttributeValue2(BaseModel):
    S: Optional[str]
    N: Optional[str]
    B: Optional[str]
    SS: Optional[Sequence[str]]
    NS: Optional[Sequence[str]]
    BS: Optional[Sequence[str]]
    M: Optional[Sequence["_Attribute3"]]
    L: Optional[Sequence[Sequence["_Attribute3"]]]
    NULL: Optional[bool]
    BOOL: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_AttributeValue2"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AttributeValue2"]:
        if not json_data:
            return None
        return cls(
            S=json_data.get("S"),
            N=json_data.get("N"),
            B=json_data.get("B"),
            SS=json_data.get("SS"),
            NS=json_data.get("NS"),
            BS=json_data.get("BS"),
            M=deserialize_list(json_data.get("M"), Attribute3),
            L=deserialize_list(json_data.get("L"), <ResolvedType(ContainerType.MODEL, Attribute3)>),
            NULL=json_data.get("NULL"),
            BOOL=json_data.get("BOOL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AttributeValue2 = AttributeValue2


@dataclass
class Attribute3(BaseModel):
    Name: Optional[str]
    Value: Optional["_AttributeValue3"]

    @classmethod
    def _deserialize(
        cls: Type["_Attribute3"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Attribute3"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Value=AttributeValue3._deserialize(json_data.get("Value")),
        )


# work around possible type aliasing issues when variable has same name as a model
_Attribute3 = Attribute3


@dataclass
class AttributeValue3(BaseModel):
    S: Optional[str]
    N: Optional[str]
    B: Optional[str]
    SS: Optional[Sequence[str]]
    NS: Optional[Sequence[str]]
    BS: Optional[Sequence[str]]
    M: Optional[Sequence["_Attribute4"]]
    L: Optional[Sequence[Sequence["_Attribute4"]]]
    NULL: Optional[bool]
    BOOL: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_AttributeValue3"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AttributeValue3"]:
        if not json_data:
            return None
        return cls(
            S=json_data.get("S"),
            N=json_data.get("N"),
            B=json_data.get("B"),
            SS=json_data.get("SS"),
            NS=json_data.get("NS"),
            BS=json_data.get("BS"),
            M=deserialize_list(json_data.get("M"), Attribute4),
            L=deserialize_list(json_data.get("L"), <ResolvedType(ContainerType.MODEL, Attribute4)>),
            NULL=json_data.get("NULL"),
            BOOL=json_data.get("BOOL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AttributeValue3 = AttributeValue3


@dataclass
class Attribute4(BaseModel):
    Name: Optional[str]
    Value: Optional["_AttributeValue4"]

    @classmethod
    def _deserialize(
        cls: Type["_Attribute4"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Attribute4"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Value=AttributeValue4._deserialize(json_data.get("Value")),
        )


# work around possible type aliasing issues when variable has same name as a model
_Attribute4 = Attribute4


@dataclass
class AttributeValue4(BaseModel):
    S: Optional[str]
    N: Optional[str]
    B: Optional[str]
    SS: Optional[Sequence[str]]
    NS: Optional[Sequence[str]]
    BS: Optional[Sequence[str]]
    M: Optional[Sequence["_Attribute5"]]
    L: Optional[Sequence[Sequence["_Attribute5"]]]
    NULL: Optional[bool]
    BOOL: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_AttributeValue4"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AttributeValue4"]:
        if not json_data:
            return None
        return cls(
            S=json_data.get("S"),
            N=json_data.get("N"),
            B=json_data.get("B"),
            SS=json_data.get("SS"),
            NS=json_data.get("NS"),
            BS=json_data.get("BS"),
            M=deserialize_list(json_data.get("M"), Attribute5),
            L=deserialize_list(json_data.get("L"), <ResolvedType(ContainerType.MODEL, Attribute5)>),
            NULL=json_data.get("NULL"),
            BOOL=json_data.get("BOOL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AttributeValue4 = AttributeValue4


@dataclass
class Attribute5(BaseModel):
    Name: Optional[str]
    Value: Optional["_AttributeValue5"]

    @classmethod
    def _deserialize(
        cls: Type["_Attribute5"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Attribute5"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Value=AttributeValue5._deserialize(json_data.get("Value")),
        )


# work around possible type aliasing issues when variable has same name as a model
_Attribute5 = Attribute5


@dataclass
class AttributeValue5(BaseModel):
    S: Optional[str]
    N: Optional[str]
    B: Optional[str]
    SS: Optional[Sequence[str]]
    NS: Optional[Sequence[str]]
    BS: Optional[Sequence[str]]
    NULL: Optional[bool]
    BOOL: Optional[bool]

    @classmethod
    def _deserialize(
        cls: Type["_AttributeValue5"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_AttributeValue5"]:
        if not json_data:
            return None
        return cls(
            S=json_data.get("S"),
            N=json_data.get("N"),
            B=json_data.get("B"),
            SS=json_data.get("SS"),
            NS=json_data.get("NS"),
            BS=json_data.get("BS"),
            NULL=json_data.get("NULL"),
            BOOL=json_data.get("BOOL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_AttributeValue5 = AttributeValue5


@dataclass
class TypeConfigurationModel(BaseModel):

    @classmethod
    def _deserialize(
        cls: Type["_TypeConfigurationModel"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_TypeConfigurationModel"]:
        if not json_data:
            return None
        return cls(
        )


# work around possible type aliasing issues when variable has same name as a model
_TypeConfigurationModel = TypeConfigurationModel


