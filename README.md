# s3-event-writer

[![hourly queue dump to s3](https://github.com/futel/s3-event-writer/actions/workflows/hourly-queue-dump.yml/badge.svg)](https://github.com/futel/s3-event-writer/actions/workflows/hourly-queue-dump.yml)


Pulls futel raw asterisk event data from SQS and writes terse
daily event files to s3.

## What it does

All very stupid/synchronously:

* start reading messages from sqs
* for each message:
  * parse all the embedded/escaped json
  * drop messages if they are `Registry` or `PeerStatus` or not from `prod` env host
  * buffer the return SQS receipts for deletion in memory
  * transform message to a simplified scrubbed format
  * "buffer" these messages into date based files
* for each date based file:
  * download same date file from s3 (if exists)
  * merge the new contents and the existing contents into a new temp file
  * upload new temp file to s3 (overwriting any existing)
* remove temp files from local disk
* delete all queue messages in the in-memory buffer one at a time (slowly)

Downsides:
* The merging of new data files and existing all happens in memory. It is not expected that the number of messages in a given day will cause problems.
* Pretty inefficient
* Deletion is slow because one at a time (we should batch)
* Timestamp is currently coming from the message envelope and not event. This is being fixed, but for now we cannot backfill easily.

Upsides:
* Benefit of deleting from SQS at the end is a crash will leave the data around in the queue for later processing
* Should be idempotent (processing a message more than once is fine)

## Run locally

Care should be given if attempting to run this locally. If it is run against the
production queue at the same time as another consumer, there can be data loss
in the event of a failure.

You must define 3 environment variables:
* `QUEUE_URL` - The url to the s3 queue to read from
* `AWS_ACCESS_KEY_ID` - The aws access key
* `AWS_SECRET_ACCESS_KEY` - The aws secret key

```
$ pip install -r requirements.txt
$ python src/app.py
```

## Admin

Ok, you're setting this up for the first time? Ugh. There are a lot of clicking steps. Sorry.
Write some terraform and make this better.

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
* Carefully copy the access key and secret key and keep them in a safe place.

The GitHub action requires 3 secrets to be defined in the repo settings:
* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `QUEUE_URL` (shown in the aws console for the given SQS queue)
