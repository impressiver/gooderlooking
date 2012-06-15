# -*- coding:utf-8 -*-

from tests import BaseTestCase as TestCase
from flask import url_for

class TestTimelineViews(TestCase):
    def test_index_view(self):
        url_path = url_for('timeline.views.index_view')
        self.client.get(url_path)
