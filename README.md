# Flask: Authentication and Authorization with Auth0

**THIS IS UNDER DEVELOPMENT**

## Overview

This is an easy, basic and raw example of **HOW to** containerize and deploy a a flask app to `Kubernetes` using `EKS`.

Every change in your repository (??? is this right or just some changes) will trigger a new build in Code Build which will result in a new docker image deployed as a container in our EKS cluster. 

## Requirements

* Python 3.6+
* pip
* Auth0 account


You will also need an AWS account (??? both console and programmatic access)

## Auth0

### Create application

1. Log in, go to the `Dashboard` and then click on `Applications` -> `Applications`
2. You are going to create a new application. Click on `Create Application`
  1. Set a name (example: `Bar`) and select `Regular Web Application`
3. Click on the new application and go to `Settings`
  1. In `Application Login URI`type: `https://127.0.0.1:8100/login`
  1. In `Allowed Callback URLs` type: `http://127.0.0.1:8100/login-results, http://127.0.0.1:8100/tabs/user-page, http://localhost:8100/tabs/user-page`
  1. In `Allowed Logout URLs` type: `http://127.0.0.1:8100/logout`

### Create API

1. Go to the `Dashboard` and then click on `Applications` -> `API`
2. You are going to crate a new API. Click on `Create API`
  1. Set a name (example: `Bar`), an identifier (example: `bar`) and a signing algorithm (for our example, select `RS256`)


## Local development

### Install dependencies

```
pip install -r requirements.txt
```

### Run Flask App

```
cd src
export FLASK_APP=api.py;

flask run --reload
```
---

## Notes:

### Auth0 Authorization Code Flow

If you want to add a `frontend` and use `Auth0 Authorization Code Flow`, you can build an `authorization page`. Here's a basic example:

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```

Replace the placeholders with your values.

Example:

```
https://dev-fv10k111.us.auth0.com/authorize?audience=app&response_type=token&client_id=11111111111111111111111111111111&redirect_uri=http://127.0.0.1:8080/login-results
```

You are going to be redirected to the `login` screen.
If you inspect the URI...

```
http://127.0.0.1:8080/login-results#access_token=222222222_etc_etc_etc&expires_in=7200&token_type=Bearer
```

You can copy the `access token` and take a look of the 3 parts of the `JWT` (Header, Payload and Signature) in: https://jwt.io/

**REMEMBER, never store sensitive data in a JWT**

For more information: https://auth0.com/docs/flows/add-login-auth-code-flow

### Encoding and decoding JWTs

If you want to practice `how to encode and decode JWTs` execute the attached file:
```
python jwt-encode-decode.py
```

If you don't have the `jwt` library, please, install it first:
```
pip install PyJWT==1.7.1
```

You can find more information of `WHY we are using this specific version` (at the moment of writing this guide) in the following thread: https://github.com/watson-developer-cloud/assistant-dialog-skill-analysis/issues/37
