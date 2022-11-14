from unittest import TestCase
from unittest.mock import patch, Mock, ANY
from chatbot import Chatbot
from vk_api.bot_longpoll import VkBotMessageEvent


class test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1615580945, 'from_id': 641395208, 'id': 54, 'out': 0, 'peer_id': 641395208,
                            'text': 'ghdbtbn', 'conversation_message_id': 54, 'fwd_messages': [], 'important': False,
                            'random_id': 0,
                            'attachments': [], 'is_hidden': False}, 'group_id': 202826280,
                 'event_id': 'ac474ebaf833ae1df52c1b7664b41b7940380463'}

    def test_run(self):
        count = 5
        events = [{}] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch('chatbot.vk_api.VkApi'):
            with patch('chatbot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Chatbot("", "")
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        with patch('chatbot.vk_api.VkApi'):
            with patch('chatbot.VkBotLongPoll'):
                bot = Chatbot("", "")
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)

        send_mock.assert_called_once_with(peer_id=self.RAW_EVENT['object']['peer_id'],
                                          random_id=ANY,
                                          message='Привет я все перевел ghdbtbn')

# python -m unittest
# coverage run -m unittest
