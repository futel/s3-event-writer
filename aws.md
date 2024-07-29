# AWS requirements

AWS components which must be set up before deploying.

# AWS setup

Have AWS configuration as described in asteriskserver README-aws:
- SQS queue "asterisk-prod-events"
Note the queue URL.

Set up users, groups, policies:
* Go to the aws console
* [Go to IAM](https://console.aws.amazon.com/iamv2/home) for access controls
* We are going to be using user groups to control permissions. Create a user group called `s3-writers` and another group called `sqs-queue-consumer` (these both exist today)
* We need to create a policy that permits reading and deleting SQS messages. Click Policies and create a policy that `Allow`s these actions: `sqs:GetQueueAttributes`, `sqs:GetQueueUrl`, `sqs:ListDeadLetterSourceQueues`, `"sqs:ListQueues`, `"sqs:DeleteMessage` (full instructions not included here). Call it something like `queue-message-delete` (what we have today). Save it.
* We need to assign a group to this new policy. Go to the `Policy usage` tab for this policy and click `Attach`. Find the `sqs-queue-consumer` group in the list, check the box, and then click `Attach policy` to save.
* We need to create a policy that allows reading and putting/overwriting S3 bucket content. Create a policy that `Allow`s these actions: `s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`. Call it something like `s3-get-put-delete` (what we have today)
*We need to assign a group to this new policy. Go to the `Policy usage` tab for this policy and
click `Attach`. Find the `s3-writers` group in the list, check the box, and then click `Attach policy` to save.
* Ok, phew, two groups, two policies. Now to create a user. Click `Users` and then `New User`.
* Give this user a name and choose the `Access key` credential type, and then `Next: Permissions`
* We need this new user to belong to the `s3-writers` and `sqs-queue-consumers` groups. Check those boxes.
* Click `Next: Tags` then `Next: Review` then `Create user`
* Note the AWS access key and secret access key.
