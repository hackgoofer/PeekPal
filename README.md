

## ngrok instrctions

```bash
python server.py
# runs a server on 127.0.0.1:5002

# if first time running ngrok
ngrok config add-authtoken YOUR_AUTH_TOKEN # sign up for ngrok first
ngrok http 5002 # because https://stackoverflow.com/questions/70247195/flask-ngrok-access-to-subdomain-ngrok-io-was-denied-403-error

# or
ngrok http 5002 --domain chicken-regular-pigeon.ngrok-free.app # swyx's custom ngrok
```