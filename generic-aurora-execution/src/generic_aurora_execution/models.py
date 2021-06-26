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
    ExecutionId: Optional[str]
    ClusterArn: Optional[str]
    SecretArn: Optional[str]
    Databases: Optional[Sequence["_Database"]]
    SQL: Optional[Sequence[str]]
    Users: Optional[Sequence["_User"]]

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
            ExecutionId=json_data.get("ExecutionId"),
            ClusterArn=json_data.get("ClusterArn"),
            SecretArn=json_data.get("SecretArn"),
            Databases=deserialize_list(json_data.get("Databases"), Database),
            SQL=json_data.get("SQL"),
            Users=deserialize_list(json_data.get("Users"), User),
        )


# work around possible type aliasing issues when variable has same name as a model
_ResourceModel = ResourceModel


@dataclass
class Database(BaseModel):
    Name: Optional[str]
    Extensions: Optional[Sequence[str]]
    SQL: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_Database"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Database"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            Extensions=json_data.get("Extensions"),
            SQL=json_data.get("SQL"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Database = Database


@dataclass
class User(BaseModel):
    Name: Optional[str]
    SecretId: Optional[str]
    SuperUser: Optional[bool]
    Grants: Optional[Sequence["_Grant"]]

    @classmethod
    def _deserialize(
        cls: Type["_User"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_User"]:
        if not json_data:
            return None
        return cls(
            Name=json_data.get("Name"),
            SecretId=json_data.get("SecretId"),
            SuperUser=json_data.get("SuperUser"),
            Grants=deserialize_list(json_data.get("Grants"), Grant),
        )


# work around possible type aliasing issues when variable has same name as a model
_User = User


@dataclass
class Grant(BaseModel):
    Database: Optional[str]
    Privileges: Optional[Sequence[str]]

    @classmethod
    def _deserialize(
        cls: Type["_Grant"],
        json_data: Optional[Mapping[str, Any]],
    ) -> Optional["_Grant"]:
        if not json_data:
            return None
        return cls(
            Database=json_data.get("Database"),
            Privileges=json_data.get("Privileges"),
        )


# work around possible type aliasing issues when variable has same name as a model
_Grant = Grant


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


