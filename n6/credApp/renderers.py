from rest_framework import renderers, status
import json


class UserJSONRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        If the response is an error, return the error message, otherwise return the data
        
        :param data: The data that was passed to the renderer
        :param accepted_media_type: The media type that the view is requesting
        :param renderer_context: This is a dictionary that contains the context of the request
        :return: The response is being returned as a JSON object.
        """
        errors = data.get('errors', None)
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps(
                {'errors': data, 'status': status.HTTP_401_UNAUTHORIZED})
        else:
            response = json.dumps(data)

        return response
