# GitHub requirements

GitHub components which must be set up before deploying, and local setup for them.

# GitHub setup

Add secrets to the GitHub repository. Using the console, navigate to settings. On the left nav, select security... secrets and variables... actions. Define:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- QUEUE_URL (for the "asterisk-prod-events" queue)
