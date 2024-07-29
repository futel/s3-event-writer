# Production and local deployment

# Meta-requirements

AWS should be set up as described in aws.md.

GitHub should be set up as described in github.md.

# Setup

Push to the origin/main branch on GitHub.

# Run locally

Care should be given if attempting to run this locally. If it is run against the
production queue at the same time as another consumer, there can be data loss
in the event of a failure.

```
$ pip install -r requirements.txt
$ python src/app.py
```
