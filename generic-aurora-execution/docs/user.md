# Generic::Aurora::Execution User

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#secretid" title="SecretId">SecretId</a>" : <i>String</i>,
    "<a href="#superuser" title="SuperUser">SuperUser</a>" : <i>Boolean</i>,
    "<a href="#grants" title="Grants">Grants</a>" : <i>[ <a href="grant.md">Grant</a>, ... ]</i>
}
</pre>

### YAML

<pre>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#secretid" title="SecretId">SecretId</a>: <i>String</i>
<a href="#superuser" title="SuperUser">SuperUser</a>: <i>Boolean</i>
<a href="#grants" title="Grants">Grants</a>: <i>
      - <a href="grant.md">Grant</a></i>
</pre>

## Properties

#### Name

The username of the user. Creates the user/role.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9-_]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SecretId

The Secrets Manager secret ID or ARN of the credentials to set for the user ('password' field of the JSON secret value).

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SuperUser

Whether to give the user rds_superuser privileges.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Grants

An array of grants to assign to the user.

_Required_: No

_Type_: List of <a href="grant.md">Grant</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

