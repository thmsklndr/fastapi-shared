from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from jose.exceptions import JWSSignatureError, JOSEError, JWKError, ExpiredSignatureError, JWTClaimsError, JWTError

import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode

import logging

logger = logging.getLogger(__name__)

class AWSCognito:

    def __init__(self, region, userpool_id, app_client_id):
        self.region = region
        self.userpool_id = userpool_id
        self.app_client_id = app_client_id

        self.keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region, userpool_id)

        logging.info(f"loading jwks from {self.keys_url}")
        with urllib.request.urlopen(self.keys_url) as f:
            response = f.read()
            self.keys = json.loads(response.decode('utf-8'))['keys']

    def _verify_token(self, token: str):
        headers = jwt.get_unverified_headers(token)
        kid = headers.get('kid', None)

        if not kid:
            raise JWTError('kid field not found in token')

        key_index = -1
        for i in range(len(self.keys)):
            if kid == self.keys[i]['kid']:
                key_index = i
                break
        if key_index == -1:
            raise JWKError('Public key not found in jwks.json')

        public_key = jwk.construct(self.keys[key_index])

        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit('.', 1)

        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise JWSSignatureError('Signature verification failed')

        # since we passed the verification, we can now safely
        # use the unverified claims

        claims = jwt.get_unverified_claims(token)
        logger.debug(claims)
        # additionally we can verify the token expiration
        if time.time() > claims['exp']:
            raise ExpiredSignatureError('Token is expired')

        # and the Audience  (use claims['client_id'] if verifying an access token)
        if claims['aud'] != self.app_client_id:
            raise JWTClaimsError('Token was not issued for this audience')

        # now we can use the claims
        return claims

    def verify_token(self, token) -> dict:
        try:
            return self._verify_token(token)
        except JOSEError:
            raise
        except Exception as excp:
            raise JWTError(f"Unknown Error occurred: {excp}")

