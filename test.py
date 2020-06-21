from unittest import TestCase
from unittest.mock import patch, Mock, ANY
from copy import deepcopy

from pony.orm import db_session, rollback

import settings
from generate_ticket import generate_ticket
from project_bot import ChatBot
from vk_api.bot_longpoll import VkBotMessageEvent


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class Test1(TestCase):
    RAW_EVENTS = {'type': 'message_new',
                  'object': {'date': 1583788217, 'from_id': 18326436, 'id': 112, 'out': 0, 'peer_id': 18326436,
                             'text': 'тест', 'conversation_message_id': 82, 'fwd_messages': [], 'important': False,
                             'random_id': 0, 'attachments': [], 'is_hidden': False}, 'group_id': 192040882,
                  'event_id': '9b0acbfc8e23f5f5b89534473ba1aecc7870d627'}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('project_bot.vk_api.VkApi'):
            with patch('project_bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = ChatBot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    INPUTS = [
        'Привет',
        'А когда?',
        'Где будет конференция?',
        "Зарегистрируй меня",
        "Василий",
        "почта error@error",
        "email@gmail.com",
    ]
    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Василий', email='email@gmail.com')
    ]

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENTS)
            event['object']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('project_bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = ChatBot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        with open('files/avatar.png', 'rb') as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()

        with patch('requests.get', return_value=avatar_mock):
            ticket_file = generate_ticket('Lesha', 'poshta@gmai.com')

        with open('files/base2.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file.read() == expected_bytes

