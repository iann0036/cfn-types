# IanMckay::S3::Object Target

Specifies the S3 location of the object.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "<a href="#bucket" title="Bucket">Bucket</a>" : String,
    "<a href="#key" title="Key">Key</a>" : String,
    "<a href="#acl" title="ACL">ACL</a>" : String
}
</pre>

### YAML

<pre>
<a href="#bucket" title="Bucket">Bucket</a>: String
<a href="#key" title="Key">Key</a>: String
<a href="#acl" title="ACL">ACL</a>: String
</pre>

## Properties

#### Bucket

The name of the bucket where the object is to be stored.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### Key

The path of within the bucket where the object is to be stored.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### ACL

The canned ACL to apply to the stored object.

_Required_: No

_Type_: String

_Allowed Values_: `private | public-read | public-read-write | aws-exec-read | authenticated-read | bucket-owner-read | bucket-owner-full-control`

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)
