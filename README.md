# CloudFormation Custom Resource Type Examples

Below are some example CloudFormation Resource Type examples.

### (Post Launch)

- [*DynamoDB Item*](https://github.com/iann0036/cfn-types/blob/master/generic-dynamodb-item/README.md) - Creates a DynamoDB Item.
- [*Database Schema*](https://github.com/iann0036/cfn-types/blob/master/generic-database-schema/README.md) - Uses the Aurora Data API to execute SQL and enforce a schema within a database cluster
- [*Stock Order*](https://github.com/iann0036/cfn-types/blob/master/stocks-orders-marketorder/README.md) - Creates a market order to buy or sell a security at the currently available market price
- [*Transcribe Custom Vocabulary*](https://github.com/iann0036/cfn-types/blob/master/generic-transcribe-vocabulary/README.md) - Creates a Transcribe Custom Vocabulary

### (Original Launch)

- [*Imported Key Pair*](https://github.com/iann0036/cfn-types/blob/master/mycorp-ec2-keypair/README.md) - Imports an EC2 key pair with existing key material (used in the walkthrough blog)
- [*S3 Object*](https://github.com/iann0036/cfn-types/blob/master/ianmckay-s3-object/README.md) - Creates and manages an S3 object from user-defined content
- [*GitHub Repo*](https://github.com/iann0036/cfn-types/blob/master/github-repositories-repository/README.md) - Creates a personal or organizational GitHub repo
- [*PagerDuty Service*](https://github.com/iann0036/cfn-types/blob/master/pagerduty-resources-service/README.md) - (incomplete) Creates and manages a PagerDuty service, which represents a monitored resource

For a walkthrough on how to create and use the new CloudFormation Custom Resource Types, check out [this walkthrough blog post](https://onecloudplease.com/blog/aws-cloudformation-custom-resource-types-a-walkthrough).
