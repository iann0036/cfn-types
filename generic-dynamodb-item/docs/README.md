# Generic::DynamoDB::Item

Manages a single DynamoDB item.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Generic::DynamoDB::Item",
    "Properties" : {
        "<a href="#tablename" title="TableName">TableName</a>" : <i>String</i>,
        "<a href="#attributes" title="Attributes">Attributes</a>" : <i>[ <a href="attribute.md">Attribute</a>, ... ]</i>,
    }
}
</pre>

### YAML

<pre>
Type: Generic::DynamoDB::Item
Properties:
    <a href="#tablename" title="TableName">TableName</a>: <i>String</i>
    <a href="#attributes" title="Attributes">Attributes</a>: <i>
      - <a href="attribute.md">Attribute</a></i>
</pre>

## Properties

#### TableName

The name of the DynamoDB table to write the item into.

_Required_: Yes

_Type_: String

_Minimum_: <code>3</code>

_Maximum_: <code>255</code>

_Pattern_: <code>^[a-zA-Z0-9-_\.]+$</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Attributes

An array of attributes for the item. This must include the key attribute(s).

_Required_: Yes

_Type_: List of <a href="attribute.md">Attribute</a>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

## Return Values

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### PartitionValue

Returns the <code>PartitionValue</code> value.

#### SortValue

Returns the <code>SortValue</code> value.

