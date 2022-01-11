import os
import unittest.mock

from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from ws_include.tests.base_test import BaseTest


class TestTemplateTag(BaseTest):
    def setUp(self):
        super().setUp()

    @unittest.mock.patch(
        'ws_include.templatetags.ws_include.get_unique_template_id'
    )
    @unittest.mock.patch(
        'ws_include.templatetags.ws_include.slugify_template_path'
    )
    def test_ws_include(
            self, mock_slugify_template_path, mock_get_unique_template_id
    ):
        mock_slugify_template_path.return_value = 'test_template_path'
        mock_get_unique_template_id.return_value = 'test_uuid'

        test_ws_include_html = render_to_string('test_ws_include.html')

        test_dir_path = os.path.dirname(os.path.abspath(__file__))
        resources_dir_path = os.path.join(test_dir_path, 'resources')
        expected_test_ws_include_path = os.path.join(resources_dir_path, 'expected_test_ws_include.html')

        with open(expected_test_ws_include_path, 'r') as expected_test_ws_include_file:
            expected_test_ws_include_html = expected_test_ws_include_file.read()
            expected_test_ws_include_pretty_html = BeautifulSoup(
                expected_test_ws_include_html, features='html.parser'
            ).prettify()
            test_ws_include_pretty_html = BeautifulSoup(
                test_ws_include_html, features='html.parser'
            ).prettify()

            self.assertEqual(expected_test_ws_include_pretty_html, test_ws_include_pretty_html)
