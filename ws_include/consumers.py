import ast
import json

import jsonpickle
from channels.generic.websocket import WebsocketConsumer
from django.apps import apps
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import translation

from . import checksum
from . import crypto


class TemplateGetter(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data: str = None, bytes_data=None):
        json_body = jsonpickle.loads(text_data)
        block_id: str = json_body.get('block_id')
        path: str = json_body.get('path')

        # Remote context
        # The caller has sent the model objects and
        # safe values (strings, numbers, etc.) as a dict with
        # the app_labels, model and id
        context = json_body.get('context')

        # language
        language_code = json_body.get('language_code')

        replacements = {}

        # For each remote context value, we load it again
        for context_object_name, context_object_load_params in json.loads(context).items():
            # Type of the value
            object_type = context_object_load_params['type']

            # If the value is a model, we load the model object and
            # include it in the template replacements
            if object_type == 'model':
                app_name = context_object_load_params['app_name']
                model_name = context_object_load_params['model']
                object_id = context_object_load_params['id']
                # Loading the model
                model = apps.get_model(app_name, model_name)
                # Loading the object and including it as a replacement
                model_object = model.objects.get(id=object_id)
                # Checking if JSON has been tampered
                model_object_as_str = '{0}-{1}-{2}'.format(
                    app_name, model_name, object_id
                )
                if (
                        context_object_load_params['__checksum__'] !=
                        checksum.make(model_object_as_str)
                ):
                    raise ValueError(
                        'JSON tampering detected when loading object'
                    )

                replacements[context_object_name] = model_object

            # If the value is a QuerySet we include it in
            # the template replacements
            elif object_type == 'QuerySet':
                # Loading the model
                app_name = context_object_load_params['app_name']
                model_name = context_object_load_params['model']
                model = apps.get_model(app_name, model_name)
                query_size = int(context_object_load_params['query_size'])
                nonce = context_object_load_params['nonce']
                tag = context_object_load_params['tag']

                try:
                    # Decryption of the data
                    raw_query_with_params = crypto.decrypt_from_base64_str(
                        key=settings.SECRET_KEY[:16],
                        nonce=nonce,
                        encrypted_data=context_object_load_params['query_with_params'],
                        tag=tag
                    )
                    raw_query = raw_query_with_params[:query_size]
                    params = raw_query_with_params[query_size:]
                    # Loading the object and including it as a replacement
                    replacements[context_object_name] = model.objects.raw(
                        raw_query, ast.literal_eval(params)
                    )
                except ValueError:
                    raise

            # If the value is a safe value,
            # we include it in the template replacements
            elif object_type == 'safe_value':
                value = context_object_load_params['value']
                value_as_str = context_object_load_params['value_as_str']
                # Checking if JSON has been tampered
                if (
                        context_object_load_params['__checksum__'] !=
                        checksum.make(value_as_str)
                ):
                    raise ValueError(
                        'JSON tampering detected when loading safe value ' +
                        'for attribute \'{0}\'. Value: \'{1}\''.format(
                            context_object_name, value_as_str
                        )
                    )

                # Including the safe value as a replacement
                replacements[context_object_name] = value

        # Activate the language
        translation.activate(language_code)

        # Response
        response = {
            'blockId': block_id,
            'html': render_to_string(path, replacements)
        }
        json_response = json.dumps(response)
        self.send(json_response)
