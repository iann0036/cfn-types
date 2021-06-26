# Generic::Aurora::Execution

Uses the Aurora Data API to execute SQL within databases.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Generic::Aurora::Execution",
    "Properties" : {
        "<a href="#clusterarn" title="ClusterArn">ClusterArn</a>" : <i>String</i>,
        "<a href="#secretarn" title="SecretArn">SecretArn</a>" : <i>String</i>,
        "<a href="#databases" title="Databases">Databases</a>" : <i>[ <a href="database.md">Database</a>, ... ]</i>,
        "<a href="#sql" title="SQL">SQL</a>" : <i>[ String, ... ]</i>,
        "<a href="#users" title="Users">Users</a>" : <i>[ <a href="user.md">User</a>, ... ]</i>
    }
}
</pre>

### YAML

<pre>
Type: Generic::Aurora::Execution
Properties:
    <a href="#clusterarn" title="ClusterArn">ClusterArn</a>: <i>String</i>
    <a href="#secretarn" title="SecretArn">SecretArn</a>: <i>String</i>
    <a href="#databases" title="Databases">Databases</a>: <i>
      - <a href="database.md">Database</a></i>
    <a href="#sql" title="SQL">SQL</a>: <i>
      - String</i>
    <a href="#users" title="Users">Users</a>: <i>
      - <a href="user.md">User</a></i>
</pre>

## Properties

#### ClusterArn

The Amazon Resource Name (ARN) of the Aurora Serverless DB cluster.

_Required_: Yes

_Type_: String

_Pattern_: <code>^arn:.*:rds:.*:.*:cluster:.+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### SecretArn

The name or ARN of the secret that enables access to the DB cluster.

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Databases

An array of databases within the cluster.

_Required_: No

_Type_: List of <a href="database.md">Database</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SQL

An array of SQL statements to execute within the database.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Users

An array of users within the cluster.

_Required_: No

_Type_: List of <a href="user.md">User</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the ExecutionId.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### ExecutionId

A unique identifier to track this execution.

