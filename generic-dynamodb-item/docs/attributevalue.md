# Generic::DynamoDB::Item AttributeValue

The value of the attribute.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#s" title="S">S</a>" : <i>String</i>,
    "<a href="#n" title="N">N</a>" : <i>String</i>,
    "<a href="#b" title="B">B</a>" : <i>String</i>,
    "<a href="#ss" title="SS">SS</a>" : <i>[ String, ... ]</i>,
    "<a href="#ns" title="NS">NS</a>" : <i>[ String, ... ]</i>,
    "<a href="#bs" title="BS">BS</a>" : <i>[ String, ... ]</i>,
    "<a href="#m" title="M">M</a>" : <i>[ <a href="attribute2.md">Attribute2</a>, ... ]</i>,
    "<a href="#l" title="L">L</a>" : <i>[ <a href="attribute3.md">Attribute3</a>, ... ]</i>,
    "<a href="#null" title="NULL">NULL</a>" : <i>Boolean</i>,
    "<a href="#bool" title="BOOL">BOOL</a>" : <i>Boolean</i>
}
</pre>

### YAML

<pre>
<a href="#s" title="S">S</a>: <i>String</i>
<a href="#n" title="N">N</a>: <i>String</i>
<a href="#b" title="B">B</a>: <i>String</i>
<a href="#ss" title="SS">SS</a>: <i>
      - String</i>
<a href="#ns" title="NS">NS</a>: <i>
      - String</i>
<a href="#bs" title="BS">BS</a>: <i>
      - String</i>
<a href="#m" title="M">M</a>: <i>
      - <a href="attribute2.md">Attribute2</a></i>
<a href="#l" title="L">L</a>: <i>
      - <a href="attribute3.md">Attribute3</a></i>
<a href="#null" title="NULL">NULL</a>: <i>Boolean</i>
<a href="#bool" title="BOOL">BOOL</a>: <i>Boolean</i>
</pre>

## Properties

#### S

A string value.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### N

A number value.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### B

A binary value, encoded as a Base64 string.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### SS

A string set value.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NS

A number set value.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### BS

A binary set value, encoded as Base64 strings.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### M

A map value.

_Required_: No

_Type_: List of <a href="attribute2.md">Attribute2</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### L

_Required_: No

_Type_: List of <a href="attribute3.md">Attribute3</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### NULL

A null value.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### BOOL

A boolean value.

_Required_: No

_Type_: Boolean

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

