# IanMckay::S3::Object

The IanMckay::S3::Object resource creates an S3 object in the same AWS Region where you create the AWS CloudFormation stack.

To control how AWS CloudFormation handles the object when the stack is deleted, you can set a deletion policy for your object. You can choose to retain the object or to delete the object. For more information, see [DeletionPolicy attribute](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html).

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "IanMckay::S3::Object",
    "Properties" : {
        "<a href="#base64body" title="Base64Body">Base64Body</a>" : String,
        "<a href="#body" title="Body">Body</a>" : String,
        "<a href="#target" title="Target">Target</a>" : <a href="https://github.com/iann0036/cfn-types/blob/master/ianmckay-s3-object/prop-target.md" title="Target">Target</a>
    }
}
</pre>

### YAML

<pre>
Type: IanMckay::S3::Object
Properties:
    <a href="#base64body" title="Base64Body">Base64Body</a>: String
    <a href="#body" title="Body">Body</a>: String
    <a href="#target" title="Target">Target</a>: <a href="https://github.com/iann0036/cfn-types/blob/master/ianmckay-s3-object/prop-target.md" title="Target">Target</a>
</pre>

## Properties

#### Body

The content of the S3 object.

_Required_: No

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Target

The S3 location of the target object.

_Required_: Yes

_Type_: [Target](prop-target.md)

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns `ETag`.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### ETag

A hash of the object.

#### S3Url

The full path to the object, starting with s3://.
