from twilio.rest import Client
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
message = client.messages.create(
  from_='+15674853219',
  body='안녕 잘 지내?!',
  to='+821027555836'
)
print(message.sid)