from unittest import TestCase
from unittest.mock import patch
from libevent.event import Event
from libevent.fields import Fields
from libevent.post_handler import PostHandler


class TestPostHandler(TestCase):
    @patch('libevent.post_handler.requests.post')
    def test_send(self, mock_request):
        data = {'field1': 'value1'}
        fields = Fields()
        fields.add_field('field2', 'value2')
        evt = Event(data, fields)
        url = 'http://www.myservice.com'
        ph = PostHandler(url)
        ph.send(evt)
        mock_request.assert_called_once_with(
            url,
            json=evt.to_dict()
        )


