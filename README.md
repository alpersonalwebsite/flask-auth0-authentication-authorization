# Flask: Authentication and Authorization with Auth0

**THIS IS UNDER DEVELOPMENT**

## Overview

This is an easy, basic and raw example of **HOW to** implement a Flask application with `Authentication` and `Authorization` using `Auth0`.

---

Before you proceed, you should understand the difference between `Authentication` and `Authorization`.

* **Authentication** confirms that users are who they say they are. (Answers the WHO?)
* **Authorization** gives those users permission to access a resource. (Answers the WHAT?)

---

## Requirements

* Python 3.6+
* pip
* Auth0 account

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

### Create the roles and assign permissions

1. Go to the `Dashboard` -> `Applications` -> `APIs` -> `bar` and **activate** `Enable RBAC` and also `Add Permissions in the Access Token`. Then, **Save**

2. Go to `Dashboard` -> `Applications` -> `bar` and click on the `Permissions` tab.
Add the following permissions/scope and descriptions

```
post:drinks	          Creates a new drink	
get:drinks-detail	    Gets drink detail	
patch:drinks	        Updates drink	
delete:drinks	        Delete drink
```

3. Go to `Dashboard` -> `Management` -> `Roles` and click on `Create Role`
Click on the `Permissions` tab, select the proper API (in our case `bar`) and add the permissions you want for this role.

4. Go to `Dashboard` -> `Management` -> `Users`
You will need an effective user. You can create it here, or through the `Auth0 Sign Up Flow`: https://dev-fv10k111.us.auth0.com/authorize?audience=bar&response_type=token&client_id=11111111111111111111111111111111&redirect_uri=http://127.0.0.1:8080/login-results
If you go this path, you can also use `Single Sign-On`.

Once you have your user, click on the `...` next to his/her name and `assign` the roles(s).

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
https://dev-fv10k111.us.auth0.com/authorize?audience=bar&response_type=token&client_id=11111111111111111111111111111111&redirect_uri=http://127.0.0.1:8080/login-results
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
cd extras

python jwt-encode-decode.py
```

If you don't have the `jwt` library, please, install it first:
```
pip install PyJWT==1.7.1
```

You can find more information of `WHY we are using this specific version` (at the moment of writing this guide) in the following thread: https://github.com/watson-developer-cloud/assistant-dialog-skill-analysis/issues/37

### Validating JWts

If you want to practice `how to validate JWTs` execute the attached file:

```
cd extras

python validate-jwt.py
```

Before executing, install the imported libraries and update the following variables with your values

```py
AUTH0_DOMAIN = 'dev-fv10k111.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'bar'

TOKEN = '222222222_etc_etc_etc' # From Auth0 Login Flow 
```

### Accessing Authorization Headers

If you want to practice `how to access authorization headers` within a Flask app...

#### Option 1

```shell
cd extras

export FLASK_APP=parsing-headers.py 
export FLASK_ENV=development
flask run --reload
```

Before executing, install the imported libraries.

Once you Flask app is running, make a request with the Authorization header, Bearer as type and a token.
```
curl http://127.0.0.1:5000/headers -H "Authorization: Bearer 111"
```

#### Option 2

If you want to check for a token (note: we are not performing validation) you can extract the logic to a function and use it within several routes.

```shell
cd extras

export FLASK_APP=parsing-headers-reusable-function.py 
export FLASK_ENV=development
flask run --reload
```

#### Option 3

Same as the previous one but using a decorator.

```shell
cd extras

export FLASK_APP=parsing-headers-reusable-decorator.py 
export FLASK_ENV=development
flask run --reload
```

### Authorization with Auth0

Until now, we were just retrieving the `token` that the user was passing through the `Authorization` headers.
We are going to start taking the token and validate it against our Auth0 API.

Before executing, install the imported libraries and update the following variables with your values

```py
AUTH0_DOMAIN = 'dev-fv10k111.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'bar'
```

Then, run your Flask app...

```shell
cd extras

export FLASK_APP=authorization-auth0.py
export FLASK_ENV=development
flask run --reload
```

You will need a valid token. 
Generate it from: https://dev-fv10k111.us.auth0.com/authorize?audience=bar&response_type=token&client_id=2222&redirect_uri=http://127.0.0.1:8080/login-results

*Note:* Replace the tenant domain, audience and client id with yours.

If you make a request with a valid token...

```
curl http://127.0.0.1:5000/headers -H "Authorization: Bearer eyJhbGciO******"
```

Result:

```
Access Granted
```

### Flask and Role Base Access Control (RBAC)

We are going to validate the token against our Auth0 API and check for a particular permission.

In our example, the user that hits the route `/headers` must pass a valid token that contains on its payload the following permission: `get:drinks-detail`

Before executing, install the imported libraries and update the following variables with your values

```py
AUTH0_DOMAIN = 'dev-fv10k111.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'bar'
```

Then, run your Flask app...

```shell
cd extras

export FLASK_APP=rbac.py
export FLASK_ENV=development
flask run --reload
```

If you make a request with a valid token...

```
curl http://127.0.0.1:5000/headers -H "Authorization: Bearer eyJhbGciO******"
```

Result:

```
{'iss': 'https://dev-fv10k111.us.auth0.com/', 'sub': 'auth0|***', 'aud': 'bar', 'iat': 1623858021, 'exp': 1623865221, 'azp': '***', 'scope': '', 'permissions': ['get:drinks-detail']}
```

### Handling the token in the frontend
Ref: https://stackoverflow.com/questions/38552003/how-to-decode-jwt-token-in-javascript

Since JWT are encoded using base64 wen can unpack the token.

```js
function parseJwt(token) {
   const base64Url = token.split('.')[1];
   const base64 = decodeURIComponent(atob(base64Url).split('').map((c)=>{
       return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
   }).join(''));

   return JSON.parse(base64);
}

const user = parseJwt('eyJhbGciO******')

console.log(user)

if (user.permissions.indexOf('get:drinks-detail') === -1) throw 'User does not have the proper permission'
```

Output:

```
{
  iss: 'https://dev-fv10k111.us.auth0.com/',
  sub: 'auth0|***',
  aud: 'bar',
  iat: 1623858021,
  exp: 1623865221,
  azp: '***',
  scope: '',
  permissions: [ 'get:drinks-detail' ]
}
```

