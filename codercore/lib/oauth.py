import base64
import json
import requests


class OAuthClient(object):
    def __init__(self, access_token_url, client_id, client_secret):
        self.encoded_string = base64.b64encode("{}:{}".format(
            client_id, client_secret).encode("utf-8")).decode("utf-8")
        self.url = access_token_url

    def get_access_token(self):
        headers = {'Authorization': 'Basic {}'.format(self.encoded_string),
                   'Content-Type': 'application/json'}
        request_body = {'grant_type': 'client_credentials'}

        response_body = requests.post(
            "{}/oauth/token".format(self.url),
            data=json.dumps(request_body), headers=headers).json()

        access_token = "{} {}".format(
            response_body['token_type'],
            response_body['access_token'])

        return access_token
