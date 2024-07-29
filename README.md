# s3-event-writer

Uses github actions to read events from an AWS SQS queue and write daily event files to an AWS S3 bucket.

# Actions

[![hourly queue dump to s3](https://github.com/futel/s3-event-writer/actions/workflows/hourly-queue-dump.yml/badge.svg)](https://github.com/futel/s3-event-writer/actions/workflows/hourly-queue-dump.yml)

[![and whatever this does](https://github.com/futel/s3-event-writer/actions/workflows/repo_keep_alive.yml/badge.svg)](https://github.com/futel/s3-event-writer/actions/workflows/repo_keep_alive.yml)

# Meta-requirements

AWS should be set up as described in aws.md.

GitHub should be set up as described in github.md.

# Setup

Push to the origin/main branch on GitHub.

# Notes

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

# Run locally

Care should be given if attempting to run this locally. If it is run against the
production queue at the same time as another consumer, there can be data loss
in the event of a failure.

```
$ pip install -r requirements.txt
$ python src/app.py
```
