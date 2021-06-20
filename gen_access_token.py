import boto3
import random
import requests
import string

client = boto3.client('ssm')

# Copy the client ID, and redirect URI in the fields below
CLIENT_ID = client.get_parameter(
    Name='devopstar-linkedin-client-id')['Parameter']['Value']
REDIRECT_URI = 'http://localhost:8000'


def create_user_code():
    # Generate a random string to protect against cross-site request forgery
    letters = string.ascii_lowercase
    CSRF_TOKEN = ''.join(random.choice(letters) for i in range(24))

    # Request authentication URL
    auth_params = {'response_type': 'code',
                   'client_id': CLIENT_ID,
                   'redirect_uri': REDIRECT_URI,
                   'state': CSRF_TOKEN,
                   'scope': 'r_liteprofile,r_emailaddress,w_member_social'}

    html = requests.get(
        "https://www.linkedin.com/oauth/v2/authorization", params=auth_params)

    # Print the link to the approval page
    print(html.url)


def get_access_token():
    AUTH_CODE = client.get_parameter(
        Name='devopstar-linkedin-auth-code')['Parameter']['Value']
    CLIENT_SECRET = client.get_parameter(
        Name='devopstar-linkedin-client-secret')['Parameter']['Value']
    ACCESS_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

    qd = {'grant_type': 'authorization_code',
          'code': AUTH_CODE,
          'redirect_uri': REDIRECT_URI,
          'client_id': CLIENT_ID,
          'client_secret': CLIENT_SECRET}

    response = requests.post(ACCESS_TOKEN_URL, data=qd, timeout=60)
    response = response.json()
    access_token = response['access_token']

    print("Access Token:", access_token)
    print("Expires in (seconds):", response['expires_in'])
    client.put_parameter(
        Name='devopstar-linkedin-access-token',
        Type='String',
        Value=access_token,
        Overwrite=True
    )


def get_linkedin_profile_id():
    ACCESS_TOKEN = client.get_parameter(
        Name='devopstar-linkedin-access-token')['Parameter']['Value']
    params = {'oauth2_access_token': ACCESS_TOKEN}
    response = requests.get('https://api.linkedin.com/v2/me', params=params)
    client.put_parameter(
        Name='devopstar-linkedin-profile-id',
        Type='String',
        Value=response.json()['id'],
        Overwrite=True
    )


if __name__ == "__main__":
    # Run me first
    # create_user_code()

    # Run me second
    # get_access_token()

    # Run me to test
    get_linkedin_profile_id()
