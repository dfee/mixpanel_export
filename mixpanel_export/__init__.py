import hashlib
import logging
import sys
import time
try:
    import simplejson as json
except ImportError:
    import json

import requests
from requests.compat import urlencode


API_ENDPOINT = 'http://mixpanel.com/api'
RAW_ENDPOINT = 'http://data.mixpanel.com/api'
VERSION = '2.0'

# Prepare logging
log = logging.getLogger('mixpanel')
hdlr = logging.StreamHandler(sys.stdout)
fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdlr.setFormatter(fmt)
log.addHandler(hdlr)


def _coerce_str(chars):
    return str(chars) if isinstance(chars, str) else chars.encode('utf-8')


class Exporter(object):
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def __repr__(self):
        return "<{} [Key: {}, Secret{}]>".format(
            self.__class__.__name__,
            self.key,
            self.secret)

    def execute(self, endpoint, version, path_sequence, qs_params):
        path = '/'.join([endpoint, version] + path_sequence)
        querystring = urlencode(qs_params)
        request_url = "{}/?{}".format(path, querystring)

        log.info('Endpoint Request: {}'.format(request_url))
        resp = requests.get(request_url)
        log.info('Response ({}s): {} / {}'.format(
            resp.status_code,
            resp.reason,
            resp.elapsed.total_seconds()))
        log.debug('Response Body: {}'.format(resp.content))
        return resp.content

    def export_raw(self, params, time_delta=600):
        """
        Generate a Mixpanel Raw Export request. A signature will automatically
        attached.

        :param params: extra parameters associated with method
        :param time_delta: amount of time request is live (TTL)
        """
        signed = self._sign_params(params, time_delta)
        content = self.execute(RAW_ENDPOINT, VERSION, ['export'], signed)
        return [json.loads(obj) for obj in content.splitlines()]

    def export(self, path_sequence, params=None, time_delta=600):
        """
        Generate a Mixpanel Export request. A signature will automatically
        attached.

        :param path_sequence: sequence of resource paths used to construct url:
            e.g. ['events', 'properties', 'values'] ->
                 http://mixpanel.com/api/2.0/events/properties/values/
        :param params: extra parameters associated with method
        :param time_delta: amount of time request is live (TTL)

        Note: ``format`` was removed as an argument input as it wasn't used.
        """
        params = params or {}
        signed = self._sign_params(params, time_delta)
        content = self.execute(API_ENDPOINT, VERSION, path_sequence, signed)
        return json.loads(content)

    def _clean_params(self, params):
        cleaned = {}
        for k, v in params.items():
            if isinstance(v, list):
                v = json.dumps(v)
            elif isinstance(v, unicode):
                v = _coerce_str(v)
            cleaned[_coerce_str(k)] = v
        return cleaned

    def _sign_params(self, params, time_delta):
        """Signs params by joining key=value pairs, and appends a secret."""

        params.update({
            'api_key': self.key,
            'expire': int(time.time()) + time_delta,
            'format': 'json'
        })

        cleaned = self._clean_params(params)

        pieces = ''.join(['{}={}'.format(k, cleaned[k])
                          for k in sorted(cleaned)])
        sig = hashlib.md5(''.join(pieces))
        sig.update(self.secret)
        cleaned['sig'] = sig.hexdigest()
        return cleaned
