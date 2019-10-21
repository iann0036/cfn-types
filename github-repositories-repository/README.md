# GitHub::Repositories::Repository

The GitHub::Repositories::Repository resource creates a GitHub personal or organizational repository.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "GitHub::Repositories::Repository",
    "Properties" : {
        "<a href="#username" title="Username">Username</a>" : String,
        "<a href="#password" title="Password">Password</a>" : String,
        "<a href="#name" title="Name">Name</a>" : String,
        "<a href="#owner" title="Owner">Owner</a>" : String,
        "<a href="#description" title="Description">Description</a>" : String,
        "<a href="#isprivate" title="IsPrivate">IsPrivate</a>" : Boolean,
        "<a href="#homepage" title="Homepage">Homepage</a>" : String,
        "<a href="#haswiki" title="HasWiki">HasWiki</a>" : Boolean,
        "<a href="#hasissues" title="HasIssues">HasIssues</a>" : Boolean
    }
}
</pre>

### YAML

<pre>
Type: GitHub::Repositories::Repository
Properties:
    <a href="#username" title="Username">Username</a>: String
    <a href="#password" title="Password">Password</a>: String
    <a href="#name" title="Name">Name</a>: String
    <a href="#owner" title="Owner">Owner</a>: String
    <a href="#description" title="Description">Description</a>: String
    <a href="#isprivate" title="IsPrivate">IsPrivate</a>: Boolean
    <a href="#homepage" title="Homepage">Homepage</a>: String
    <a href="#haswiki" title="HasWiki">HasWiki</a>: Boolean
    <a href="#hasissues" title="HasIssues">HasIssues</a>: Boolean
</pre>

## Properties

#### Username

The username of the authenticating user.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Password

The password or personal access token of the authenticating user.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Name

The name of the repository.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Owner

The organization in which the repository is located. This is required to make the repository organizational.

_Required_: No

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Description

A description of the repository.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### IsPrivate

Whether the repository is a private repository. Repositories are created as public (e.g. open source) by default.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Homepage

A URL of a page describing the project.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### HasWiki

Whether the Wiki feature is enabled in the repository.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### HasIssues

Whether the Issues feature is enabled in the repository.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the short path (_owner_/_name_) of the repository.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### RepoPath

The short path (_owner_/_name_) of the repository.
