# Generic::Aurora::Execution Table

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#columns" title="Columns">Columns</a>" : <i>[ <a href="column.md">Column</a>, ... ]</i>,
    "<a href="#primarykey" title="PrimaryKey">PrimaryKey</a>" : <i><a href="primarykey.md">PrimaryKey</a></i>
}
</pre>

### YAML

<pre>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#columns" title="Columns">Columns</a>: <i>
      - <a href="column.md">Column</a></i>
<a href="#primarykey" title="PrimaryKey">PrimaryKey</a>: <i><a href="primarykey.md">PrimaryKey</a></i>
</pre>

## Properties

#### Name

The name of the table. Creates the table if it doesn't exist.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9-_]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Columns

An array of columns to manage within the database.

_Required_: No

_Type_: List of <a href="column.md">Column</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### PrimaryKey

_Required_: No

_Type_: <a href="primarykey.md">PrimaryKey</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

