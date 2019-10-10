# MyCorp::EC2::KeyPair

The MyCorp::EC2::KeyPair resource creates an [EC2 key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html) which is used to control login access to EC2 instances.

Currently this resource requires an existing user-supplied key pair. This key pair's public key will be registered with AWS to allow logging-in to EC2 instances.

When importing an existing key pair the public key material may be in any format supported by AWS. Supported formats (per the [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#how-to-generate-your-own-key-and-import-it-to-aws)) are:

* OpenSSH public key format (the format in ~/.ssh/authorized_keys)
* Base64 encoded DER format
* SSH public key file format as specified in RFC4716

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "MyCorp::EC2::KeyPair",
    "Properties" : {
        "<a href="#keyname" title="KeyName">KeyName</a>" : String,
        "<a href="#publickey" title="PublicKey">PublicKey</a>" : String
    }
}
</pre>

### YAML

<pre>
Type: MyCorp::EC2::KeyPair
Properties:
    <a href="#keyname" title="KeyName">KeyName</a>: String
    <a href="#publickey" title="PublicKey">PublicKey</a>: String
</pre>

## Properties

#### KeyName

The name of the key pair.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

#### PublicKey

The public key material of the key pair.

_Required_: Yes

_Type_: String

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the key name.

### Fn::GetAtt

The `Fn::GetAtt` intrinsic function returns a value for a specified attribute of this type. The following are the available attributes and sample return values.

For more information about using the `Fn::GetAtt` intrinsic function, see [Fn::GetAtt](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-getatt.html).

#### Fingerprint

The MD5 public key fingerprint as specified in section 4 of RFC 4716.