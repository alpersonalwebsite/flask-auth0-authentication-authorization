# Import Python Package
import jwt
import base64

# Init our Data
payload = {'message':'Hello World!'}
algo = 'HS256' #HMAC-SHA 256
secret = 'this is the secret'

# Encode a JWT
encoded_jwt = jwt.encode(payload, secret, algorithm=algo)
print(encoded_jwt)

'''
b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJtZXNzYWdlIjoiSGVsbG8gV29ybGQhIn0.NsAcREB4bbZv_MoGs8aL8K-ukzb0I3M4Do1tgtwfNjc'
'''

# Decode a JWT
decoded_jwt = jwt.decode(encoded_jwt, secret, verify=True)
print(decoded_jwt)

'''
{'message': 'Hello World!'}
'''

# Decode with Simple Base64 Encoding
decoded_base64 = base64.b64decode(str(encoded_jwt).split(".")[1]+"==")
print(decoded_base64)

'''
b'{"message":"Hello World!"}'
'''