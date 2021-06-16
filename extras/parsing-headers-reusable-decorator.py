from flask import Flask, request, abort
from functools import wraps

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
  
  return headers_parts[1] # token

def requires_auth(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    jwt = get_token_auth_header()
    return f(jwt, *args, **kwargs)
  return wrapper

@app.route('/headers')
@requires_auth
def get_authorization_header(jwt):
  print(jwt)
  return jwt