# Generic::Database::Schema Grant

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#database" title="Database">Database</a>" : <i><a href="database.md">Database</a></i>,
    "<a href="#table" title="Table">Table</a>" : <i><a href="table.md">Table</a></i>,
    "<a href="#privileges" title="Privileges">Privileges</a>" : <i>[ String, ... ]</i>
}
</pre>

### YAML

<pre>
<a href="#database" title="Database">Database</a>: <i><a href="database.md">Database</a></i>
<a href="#table" title="Table">Table</a>: <i><a href="table.md">Table</a></i>
<a href="#privileges" title="Privileges">Privileges</a>: <i>
      - String</i>
</pre>

## Properties

#### Database

_Required_: Yes

_Type_: <a href="database.md">Database</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Table

_Required_: No

_Type_: <a href="table.md">Table</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Privileges

An array of privileges to grant (CONNECT, SELECT, etc.).

_Required_: Yes

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

