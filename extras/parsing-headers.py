from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/headers')
def get_authorization_header():

  print(request.headers)

  if 'Authorization' not in request.headers:
    abort(401)

  auth_header = request.headers['Authorization']
  headers_parts = auth_header.split(' ')

  # we expect to be Bearer Token
  # example: Bearer 111
  if len(headers_parts) != 2:
    abort(401)

  elif headers_parts[0].lower() != 'bearer':
    abort(401)

  print(headers_parts) # Bearer
  print(headers_parts[1]) # 111
  return headers_parts[1]