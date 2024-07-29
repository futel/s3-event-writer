# Production and local deployment

# Meta-requirements

AWS should be set up as described in aws.md.

GitHub should be set up as described in github.md.

# Deploy

Push to the origin/main branch on GitHub.

# Run locally

Care should be given if attempting to run this locally. If it is run against the
production queue at the same time as another consumer, there can be data loss
in the event of a failure.


# Local setup

Set these secrets in environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- QUEUE_URL (for the "asterisk-prod-events" queue)

```
$ pip install -r requirements.txt
$ python src/app.py
```
