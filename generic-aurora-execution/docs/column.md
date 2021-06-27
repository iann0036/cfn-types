# Generic::Aurora::Execution Column

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#type" title="Type">Type</a>" : <i>String</i>,
    "<a href="#nullable" title="Nullable">Nullable</a>" : <i>Boolean</i>,
    "<a href="#default" title="Default">Default</a>" : <i>String</i>
}
</pre>

### YAML

<pre>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#type" title="Type">Type</a>: <i>String</i>
<a href="#nullable" title="Nullable">Nullable</a>: <i>Boolean</i>
<a href="#default" title="Default">Default</a>: <i>String</i>
</pre>

## Properties

#### Name

The name of the column. Creates the column if it doesn't exist.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9-_]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Type

The type of the column.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9-_]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Nullable

Whether the column is nullable.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Default

The default value of the column.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

