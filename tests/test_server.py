import unittest
import server

from unittest import mock


class TestServer(unittest.TestCase):
    @mock.patch('server.render_template')
    @mock.patch('server.SocketIO')
    @mock.patch('server.Flask')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_date_of_birth(self, mock_emit, mock_request, *_):
        user_mock = mock.Mock()
        user_mock.name = 'Orla'
        user_mock.smoker = 'No'
        user_mock.gender = 'Female'
        server.shared_dict[1] = user_mock

        mock_request.sid = 1
        message = {'data': '10-10-2000'}
        server.set_date_of_birth(message)
        self.assertEqual(mock_emit.call_count, 2)

    @mock.patch('server.render_template')
    @mock.patch('server.SocketIO')
    @mock.patch('server.Flask')
    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_date_of_birth_value_error(self, mock_emit, mock_request, mock_logging, *_):
        user_mock = mock.Mock()
        user_mock.name = 'Matt'
        user_mock.smoker = 'No'
        user_mock.gender = 'Male'
        p = mock.PropertyMock(side_effect=ValueError)
        type(user_mock).date_of_birth = p
        server.shared_dict[1] = user_mock
        mock_request.sid = 1
        message = {'data': '10/10/2000'}

        server.set_date_of_birth(message)
        self.assertEqual(mock_emit.call_count, 1)
        self.assertEqual(mock_logging.error.call_count, 1)
        mock_emit.assert_any_call(server.USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'users_date_of_birth',
                                                                 'error_message': 'Please pass date in correct format dd-mm-yyyy',
                                                                 'error': True})

    @mock.patch('server.render_template')
    @mock.patch('server.SocketIO')
    @mock.patch('server.Flask')
    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_date_of_birth_unhandled_error(self, mock_emit, mock_request, mock_logging, *_):
        user_mock = mock.Mock()
        user_mock.name = 'Jenny'
        user_mock.smoker = 'Yes'
        user_mock.gender = 'Female'
        p = mock.PropertyMock(side_effect=TypeError)
        type(user_mock).date_of_birth = p
        server.shared_dict[1] = user_mock
        mock_request.sid = 1
        message = {'data': '09/10/1967'}

        server.set_date_of_birth(message)
        self.assertEqual(mock_emit.call_count, 1)
        self.assertEqual(mock_logging.error.call_count, 1)
        mock_emit.assert_any_call(server.USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'users_date_of_birth',
                                                                 'error_message': 'Please pass date in correct format dd-mm-yyyy',
                                                                 'error': True})


if __name__ == 'main':
    unittest.main()
