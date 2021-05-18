# LinkedIn Professional

LinkedIn Professional is a POC program that helps you boost your career by automatically updating your LinkedIn profile with the hottest new skills in tech based on the [Technology Radar](https://www.thoughtworks.com/radar)

## Setup Serverless

```bash
npm install -g serverless
serverless create --template aws-python3
serverless config credentials --provider aws --key <ACCESS KEY ID> --secret <SECRET KEY>
```

## Python & Domain Requirements

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

## Deploy

```bash
npm install
serverless deploy
```

## Invoke Function

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
