from django.test import TestCase


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        import os
        os.environ.setdefault(
            'DJANGO_SETTINGS_MODULE', 'ws_include.tests.settings'
        )
        import django
        django.setup()
        super(TestViews, cls).setUpClass()
