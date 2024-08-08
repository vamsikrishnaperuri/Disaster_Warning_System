# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "YOUR_ACCOUNT_SID"
auth_token = "YOUR_AUTH_TOKEN"
client = Client(account_sid, auth_token)


def call(audio_url, to_number="TO_NUMBER"):
    call = client.calls.create(
        url=audio_url,
        to=to_number,
        from_="FROM_GIVEN_NUMBER")
    print(call.sid)

# call(to_number="+916281462828")
