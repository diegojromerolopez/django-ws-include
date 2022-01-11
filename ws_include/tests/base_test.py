from django.test import TestCase


class BaseTest(TestCase):
    def setUp(self):
        import os
        os.environ.setdefault(
            'DJANGO_SETTINGS_MODULE', 'ws_include.tests.settings'
        )
        import django
        django.setup()
        super().setUp()
