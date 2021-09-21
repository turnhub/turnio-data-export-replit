import os
import pytz
from datetime import datetime, timedelta
import requests


TOKEN = os.environ['TOKEN']
HOST = os.environ.get('HOST', 'https://whatsapp.turn.io')

# Get the date range in the UTC timezone, for this
# example we're looking at messages sent & received in the last 24 hours
today = datetime.utcnow().replace(tzinfo=pytz.utc)
yesterday = today - timedelta(hours=24)

# Request a cursor from the API for the given date range
# and specify the scrubbing rules we want
cursor_response = requests.post(url=f'{HOST}/v1/data/messages/cursor', headers={
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.v1+json'
  }, json={
    "from": yesterday.isoformat(),
    "until": today.isoformat(),
    "ordering": "asc",
    "page_size": 10,
    "scrubbing_rules": {
        "inbound": {
            # Convert any received text mentioning the word `world` with `XXX`
            "messages.text.body": {
                "type": "regex",
                "search": "world",
                "replace": "XXXX"
            },
            # Hash the from-addr for messages received to anonymise them
            "messages.from": {
                "type": "hash"
            },
            # Also has the profile name
            "contacts.profile.name": {
                "type": "hash"
            }
        },
        # For any sent messages do the same
        "outbound": {
            "text.body": {
                "type": "regex",
                "search": "world",
                "replace": "XXXX"
            },
            "from": {
                "type": "hash"
            }
        }
    }
  })

# Request a cursor and unpack it
cursor_data = cursor_response.json()
cursor = cursor_data['cursor']
cursor_expires_at = cursor_data['expires_at']

print(f"Cursor expires at {cursor_expires_at}")

# Request any data for the given cursor
first_page_response = requests.get(url=f'{HOST}/v1/data/messages/cursor/{cursor}', headers={
  'Authorization': f'Bearer {TOKEN}',
  'Accept': 'application/vnd.v1+json',
})
first_page_data = first_page_response.json()

messages = first_page_data['data']
paging = first_page_data['paging']

# Loop over the messages received
for m in messages:
  # If the entry is in the format
  # {messages: [message], contacts: [contact]} 
  # then it was a message received from the user and we're using the format
  # as per the WhatsApp Business API documentation
  if 'messages' in m:
    [message] = m['messages']
    print('Received "{text}" from "{sender}"'.format(
      text=message['text']['body'], 
      sender=message['from']))
  # If the format isn't the above then we're using the format as used
  # for sending outbound messages from the WhatsApp Business API as 
  # per the documentation for sending messages at /v1/messages
  else:
    print('Sent: {text} from {sender}'.format(
      text=m['text']['body'],
      sender=m['from']
    ))

# If we have a paging entry then it means there were more results can provided
# and we can page through the results with the `next` cursor supplied.
if paging:
  print('This cursor has more results than printed, request more with the following cursor:')
  print(paging['next'])
else:
  print('These are all the results, there are no more messages to display')