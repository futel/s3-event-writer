
# backfilling data

There is a tool `src/backfill.py` that can be used to backfill
missing/lost/skipped/damaged data. It only reads from stdin,
and takes lines from the "metrics" logs that look like this:

```
2022-04-04 22:45:55,436 UNIQUEID=1833323238.399, CHANNEL=SIP/630-0000011f, CALLERID(number)=+12345678901, name=filterdial
```

The backfill transforms these "metrics" lines into messages that contain
just the interesting fields that we carry forward to sqs and then s3.
This backfill process only publishes to SNS, and it is assumed that a
downstream process will read them from SQS later.

You must have a profile in `~/.aws/credentials` with permissions to
publish to SNS. Alternatively, you can export `AWS_ACCESS_KEY_ID` and
`AWS_SECRET_ACCESS_KEY` to your environment (should work, untested).

You must also know the AWS ARN of the SNS topic to publish to.

To run, put the missing metrics in a file (in this example `metrics.txt`)
and run the tool like this:

```
cat metrics.txt | \
  python src/backfill.py -a <arn> -p my-aws-profile
```
