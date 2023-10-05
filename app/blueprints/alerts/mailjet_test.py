from mailjet_rest import Client
import os
api_key = 'c9eca1827846532217327c879f5ba636'
api_secret = 'fe1731f0514e91727c33519cbdeedb6f'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "help@ogwholesaling.com",
        "Name": "og"
      },
      "To": [
        {
          "Email": "tomevuelo@gmail.com",
          "Name": "tome"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())
