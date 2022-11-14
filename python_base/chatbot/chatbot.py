# from token import token
import vk_api

# from token import token
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import random
from googletrans import Translator
import logging

log = logging.getLogger("chat_bot_log")


def log_configure():
    log.setLevel(logging.DEBUG)
    stream_hand = logging.StreamHandler()
    stream_hand.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_hand.setLevel(logging.INFO)
    log.addHandler(stream_hand)

    file_hand = logging.FileHandler("chat_bot_log.log")
    file_hand.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%d-%m-%Y %H:%M"))
    file_hand.setLevel(logging.DEBUG)
    log.addHandler(file_hand)


def import_sets():
    try:
        from settings import TOKEN
        from settings import GROUP_ID
        return GROUP_ID, TOKEN
    except ImportError:
        settings = None  # Для того, чтобы убрать замечание среду разработки.
        log.exception('Для работы бота не получается произвести импорт настроек')
        exit()


class Chatbot:
    """
    echo bot for vk.com
    use python 3.7
    """

    def __init__(self, group_id, token):
        """group_id - group_id from group vk.com, token - secret token from vk.com"""
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.translator = Translator()

    def run(self):
        """Запуск бота"""
        for event in self.long_poll.listen():
            try:
                self.on_event(event)
            except Exception as err:
                log.exception("Ошибка в обработке события")
                # print(err)

    def on_event(self, event: VkBotEventType):
        """отправляет сообщение назад"""
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug(event.object.text)
            result = self.translator.translate(event.object.text, src='ru', dest='en')
            log.debug(result.text)
            nid = random.randint(1, 2 ** 32)
            log.debug("Отправляем сообщение назад")
            self.api.messages.send(peer_id=event.object.peer_id, random_id=nid,
                                   message="Привет я все перевел " + result.text)
        else:
            log.info("Не обрабатываем событие типа %s", event.type)
            # print()


if __name__ == "__main__":
    log_configure()
    group_id, token = import_sets()
    bot = Chatbot(group_id, token)
    bot.run()
