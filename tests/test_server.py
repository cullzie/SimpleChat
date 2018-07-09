import unittest
import server

from unittest import mock


class TestServer(unittest.TestCase):
    @mock.patch('server.render_template')
    def test_index(self, mock_render_template):
        server.index()
        mock_render_template.assert_called_once_with('index.html')
        self.assertEqual(mock_render_template.call_count, 1)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_user_name(self, mock_emit, mock_request, mock_logger):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        message = {'data': 'Yani'}
        server.set_user_name(message)
        self.assertEqual(mock_emit.call_count, 2)
        self.assertEqual(mock_logger.error.call_count, 0)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_user_name_empty(self, mock_emit, mock_request, mock_logger):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        message = {'data': ''}
        server.set_user_name(message)
        self.assertEqual(mock_emit.call_count, 1)
        self.assertEqual(mock_logger.error.call_count, 1)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_user_gender(self, mock_emit, mock_request, mock_logger):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        message = {'data': 'Male'}
        server.set_user_gender(message)
        self.assertEqual(mock_emit.call_count, 2)
        self.assertEqual(mock_logger.error.call_count, 0)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_user_gender_invalid(self, mock_emit, mock_request, mock_logger):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        p = mock.PropertyMock(side_effect=ValueError)
        type(user_mock).gender = p
        message = {'data': 'Invalid Gender'}
        server.set_user_gender(message)
        self.assertEqual(mock_emit.call_count, 1)
        self.assertEqual(mock_logger.error.call_count, 1)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_is_smoker(self, mock_emit, mock_request, mock_logger):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        message = {'data': 'Yes'}
        server.set_is_smoker(message)
        self.assertEqual(mock_emit.call_count, 2)
        self.assertEqual(mock_logger.error.call_count, 0)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_is_smoker_invalid(self, mock_emit, mock_request, mock_logger):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        p = mock.PropertyMock(side_effect=ValueError)
        type(user_mock).smoker = p
        message = {'data': 'I have never been a smoker'}
        server.set_is_smoker(message)
        self.assertEqual(mock_emit.call_count, 1)
        self.assertEqual(mock_logger.error.call_count, 1)

    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_date_of_birth(self, mock_emit, mock_request):
        user_mock = mock.Mock()
        user_mock.name = 'Orla'
        user_mock.smoker = 'No'
        user_mock.gender = 'Female'
        server.shared_dict[1] = user_mock

        mock_request.sid = 1
        message = {'data': '10-10-2000'}
        server.set_date_of_birth(message)
        self.assertEqual(mock_emit.call_count, 2)

    @mock.patch('server.logger')
    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_set_date_of_birth_value_error(self, mock_emit, mock_request, mock_logging):
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

    @mock.patch('server.request')
    @mock.patch('server.emit')
    def test_get_user_details(self, mock_emit, mock_request):
        user_mock = mock.Mock()
        server.shared_dict[1] = user_mock
        mock_request.sid = 1

        server.show_details()
        self.assertEqual(mock_emit.call_count, 1)



if __name__ == 'main':
    unittest.main()
