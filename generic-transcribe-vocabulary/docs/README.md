# Generic::Transcribe::Vocabulary

A custom vocabulary that you can use to change the way Amazon Transcribe handles transcription of an audio file.

## Syntax

To declare this entity in your AWS CloudFormation template, use the following syntax:

### JSON

<pre>
{
    "Type" : "Generic::Transcribe::Vocabulary",
    "Properties" : {
        "<a href="#languagecode" title="LanguageCode">LanguageCode</a>" : <i>String</i>,
        "<a href="#phrases" title="Phrases">Phrases</a>" : <i>[ String, ... ]</i>,
        "<a href="#vocabularyfileuri" title="VocabularyFileUri">VocabularyFileUri</a>" : <i>String</i>,
        "<a href="#vocabularyname" title="VocabularyName">VocabularyName</a>" : <i>String</i>
    }
}
</pre>

### YAML

<pre>
Type: Generic::Transcribe::Vocabulary
Properties:
    <a href="#languagecode" title="LanguageCode">LanguageCode</a>: <i>String</i>
    <a href="#phrases" title="Phrases">Phrases</a>: <i>
      - String</i>
    <a href="#vocabularyfileuri" title="VocabularyFileUri">VocabularyFileUri</a>: <i>String</i>
    <a href="#vocabularyname" title="VocabularyName">VocabularyName</a>: <i>String</i>
</pre>

## Properties

#### LanguageCode

The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/what-is-transcribe.html).

_Required_: Yes

_Type_: String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### Phrases

An array of strings that contains the vocabulary entries.

_Required_: No

_Type_: List of String

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### VocabularyFileUri

The S3 location of the text file that contains the definition of the custom vocabulary. The URI must be in the same region as the API endpoint that you are calling.

_Required_: No

_Type_: String

_Pattern_: <code>(s3://|http(s*)://).+</code>

_Update requires_: [No interruption](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-no-interrupt)

#### VocabularyName

The name of the vocabulary. The name must be unique within an AWS account. The name is case sensitive.

_Required_: Yes

_Type_: String

_Minimum_: <code>1</code>

_Maximum_: <code>200</code>

_Pattern_: <code>^[0-9a-zA-Z._-]+</code>

_Update requires_: [Replacement](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement)

## Return Values

### Ref

When you pass the logical ID of this resource to the intrinsic `Ref` function, Ref returns the VocabularyName.
