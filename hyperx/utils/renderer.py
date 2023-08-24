from rest_framework import renderers
import json


class CustomAPIResponseRenderer(renderers.JSONRenderer):
    """
        Render the response data.

        Args:
            data (Any): The data to be rendered.
            accepted_media_type (str): The accepted media type.
            renderer_context (dict): Additional context for rendering.

        Returns:
            str: The rendered response data.

    """

    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''

        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})
        return response
