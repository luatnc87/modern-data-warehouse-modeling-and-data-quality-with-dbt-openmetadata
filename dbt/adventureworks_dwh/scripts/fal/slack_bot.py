"""Send Slack messages from your dbt project.

You can use fal to send Slack messages.
A Slack App needs to be properly set up first:

1. Create a Slack App

Follow instructions on this page in order to create an organization-specific
Slack app:

https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace

Add following OAuth Scopes:

- `channels:join`
- `chat:write`
- `files:write`
- `app_mentions:read`
- `groups:read`

2. Install the app and get the bot token

On the same "OAuth & Permissions" page, click on "Install to Workspace" button,
proceed with installation and take note of the provided Bot User OAuth Token.

3. Get channel ID

In Slack, right click on the channel that you want fal to publish to, click on
"Open channel details" and copy the Channel ID on the bottom of the modal.

4. Add your bot to your channel

In your Slack channel, type following message:

/add @your_bot_name

5. Set environment variables

In terminal set following two environment variable: SLACK_BOT_TOKEN and
SLACK_BOT_CHANNEL. This can be done with export command:

export SLACK_BOT_TOKEN=your-bot-token
export SLACK_TARGET_CHANNEL=your-target-channel
"""

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

CHANNEL_ID = os.getenv("SLACK_BOT_CHANNEL")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")

client = WebClient(token=SLACK_TOKEN)

message_text = f"Model: {context.current_model.name}. Status: {context.current_model.status}."
print("Message: " + message_text)

try:
    response = client.chat_postMessage(
        channel=CHANNEL_ID,
        text=message_text
    )
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["error"]