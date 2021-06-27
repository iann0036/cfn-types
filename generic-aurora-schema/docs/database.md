# Generic::Database::Schema Database

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#name" title="Name">Name</a>" : <i>String</i>,
    "<a href="#tables" title="Tables">Tables</a>" : <i>[ <a href="table.md">Table</a>, ... ]</i>,
    "<a href="#extensions" title="Extensions">Extensions</a>" : <i>[ String, ... ]</i>,
    "<a href="#sql" title="SQL">SQL</a>" : <i>[ String, ... ]</i>
}
</pre>

### YAML

<pre>
<a href="#name" title="Name">Name</a>: <i>String</i>
<a href="#tables" title="Tables">Tables</a>: <i>
      - <a href="table.md">Table</a></i>
<a href="#extensions" title="Extensions">Extensions</a>: <i>
      - String</i>
<a href="#sql" title="SQL">SQL</a>: <i>
      - String</i>
</pre>

## Properties

#### Name

The name of the database. Creates the database if it doesn't exist.

_Required_: Yes

_Type_: String

_Pattern_: <code>^[a-zA-Z0-9-_]+$</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Tables

An array of tables to manage within the database.

_Required_: No

_Type_: List of <a href="table.md">Table</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Extensions

An array of extensions to enable within the database.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SQL

An array of SQL statements to execute within the database.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

