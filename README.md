# LinkedIn Professional

LinkedIn Professional is a POC program that helps you boost your career by automatically updating your LinkedIn profile with the hottest new skills in tech based on the [Technology Radar](https://www.thoughtworks.com/radar)

## Setup Serverless

```bash
npm install -g serverless
serverless create --template aws-python3
serverless config credentials --provider aws --key <ACCESS KEY ID> --secret <SECRET KEY>
```

### Python & Domain Requirements

```bash
serverless plugin install -n serverless-python-requirements
```

Add the following to the `serverless.yml` file

```yaml
plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: true
```

## LinkedIn Auth Flow

Create a set of secret values using the client ID and client secret from the LinkedIn developer console

```bash
aws ssm put-parameter --overwrite --name devopstar-linkedin-client-id       --type String --value $CLIENT_ID
aws ssm put-parameter --overwrite --name devopstar-linkedin-client-secret   --type String --value $CLIENT_SECRET
aws ssm put-parameter --overwrite --name devopstar-linkedin-auth-code       --type String --value $AUTH_CODE
aws ssm put-parameter --overwrite --name devopstar-deep-ai-token            --type String --value $DEEP_AI_TOKEN
```

## Deploy

```bash
npm install
serverless deploy
```

### Invoke Function

You can invoke your deployed functions using the following

```bash
# Activate a python envirionment locally
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Test locally
serverless invoke local -f skills

# Test Deployed version
serverless invoke -f skills
```
