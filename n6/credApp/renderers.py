from rest_framework import renderers, status
import json


class UserJSONRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = data.get('errors', None)
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps(
                {'errors': data, 'status': status.HTTP_401_UNAUTHORIZED})
        else:
            response = json.dumps(data)

        return response
