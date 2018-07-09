import logging

from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

from dtos.User import User

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretchatappkey'
socketio = SocketIO(app)

shared_dict = dict()
# TODO: Shared dict can be a multiprocessing dict or something like a redis key/value pair based on the users session
# TODO: in order to maintain the state of the users actions.
BOT_RESPONSE_CHANNEL = 'bot_response'
USER_RESPONSE_CHANNEL = 'user_response'


@app.route('/')
def index():
    """
    Returns the index page of the application.

    :return:
    """
    return render_template('index.html')


@socketio.on('users_name', namespace='/user_details')
def set_user_name(message):
    """
    Takes in the users name and adds it to User object in the cache.
    It also emits the next Question in the sequence

    :param message: Websocket message containing the users name
    :return:
    """
    if message.get('data'):
        shared_dict.get(request.sid).name = message['data']
        emit(USER_RESPONSE_CHANNEL, {'data': message['data']})
        emit(BOT_RESPONSE_CHANNEL, {'data': 'Are you Female or Male?', 'display': 'users_gender'})
    else:
        logger.error('User didn\'t pass a name')
        emit(USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'users_name',
                                     'error_message': 'Please pass a value for name', 'error': True})


@socketio.on('users_gender', namespace='/user_details')
def set_user_gender(message):
    """
    Takes in the users gender and adds it to User object in the cache.
    It also emits the next Question in the sequence

    :param message: Websocket message containing the users name
    :return:
    """
    try:
        shared_dict.get(request.sid).gender = message['data']
        emit(USER_RESPONSE_CHANNEL, {'data': message['data']})
        emit(BOT_RESPONSE_CHANNEL, {'data': 'When were you born?', 'display': 'users_date_of_birth'})
    except ValueError as e:
        logger.error('Handled exception while setting Gender: {0}'.format(str(e)))
        emit(USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'users_gender',
                                     'error_message': 'Please stick to the available genders', 'error': True})


@socketio.on('users_date_of_birth', namespace='/user_details')
def set_date_of_birth(message):
    """
    Takes in the users date of birth and adds it to User object in the cache.
    It also emits the next Question in the sequence

    :param message: Websocket message containing the users name
    :return:
    """
    try:
        shared_dict.get(request.sid).date_of_birth = message['data']
    except ValueError as e:
        logger.error('Handled exception while setting date of Birth: {0}'.format(str(e)))
        emit(USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'users_date_of_birth',
                                     'error_message': 'Please pass date in correct format dd-mm-yyyy', 'error': True})
    except Exception as e:
        logger.error('Unknown exception while setting date of Birth: {0}'.format(str(e)))
        emit(USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'users_date_of_birth',
                                     'error_message': 'Please pass date in correct format dd-mm-yyyy', 'error': True})
    else:
        emit(USER_RESPONSE_CHANNEL, {'data': message['data']})
        emit(BOT_RESPONSE_CHANNEL, {'data': 'Are you a smoker?', 'display': 'user_is_smoker'})


@socketio.on('user_is_smoker', namespace='/user_details')
def set_is_smoker(message):
    """
    Takes in the if the user is a smoker and adds it to User object in the cache.
    It also emits the next Question in the sequence

    :param message: Websocket message containing the users name
    :return:
    """
    try:
        shared_dict.get(request.sid).smoker = message['data']
        emit(USER_RESPONSE_CHANNEL, {'data': message['data']})
        emit(BOT_RESPONSE_CHANNEL, {'data': 'Thank you. Press "Done" for results.', 'display': 'show_details'})
    except ValueError as e:
        logger.error('Handled exception while setting is Smoker flag: {0}'.format(str(e)))
        emit(USER_RESPONSE_CHANNEL, {'data': 'Error', 'display': 'user_is_smoker',
                                     'error_message': 'Please stick to Yes or No', 'error': True})


@socketio.on('show_details', namespace='/user_details')
def show_details():
    """
    Prints the User str response to the wesocket output.

    :return:
    """
    user_details = str(shared_dict[request.sid])
    if user_details:
        emit(BOT_RESPONSE_CHANNEL, {'data': user_details})
    else:
        emit(BOT_RESPONSE_CHANNEL, {'data': 'Missing some details. Please try again'})
    # TODO: Another step here would be to persist the data into a sql db or this could be implemented on each step


@socketio.on('connect', namespace='/user_details')
def on_connect():
    """
    Takes in the users name and adds it to the cache.
    It also emits the result to the websocket along with the next Question in the sequence

    :return:
    """
    logger.info('Client connected')
    shared_dict[request.sid] = User()  # On initial connection add the empty user object to the cache
    emit(BOT_RESPONSE_CHANNEL,
         {'data': 'Hello, I am going to ask you few questions that will help me know you better?'})
    emit(BOT_RESPONSE_CHANNEL, {'data': 'What is your name?', 'display': 'users_name'})
    # We emit the display argument here which determines the next button to display on the UI


@socketio.on('disconnect', namespace='/user_details')
def on_disconnect():
    """
    Takes in the users name and adds it to the cache. 
    It also emits the result to the websocket along with the next Question in the sequence

    :return: 
    """

    logger.info('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
