from flask import Flask, request, abort

app = Flask(__name__)


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    headers_parts = auth_header.split(' ')

    # we expect to be Bearer Token
    if len(headers_parts) != 2:
        abort(401)

    elif headers_parts[0].lower() != 'bearer':
        abort(401)

    return headers_parts[1]  # token


@app.route('/headers')
def get_authorization_header():

    jwt = get_token_auth_header()
    print(jwt)
    return jwt
