import game
import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


# token = 'da6532b279b252e0950f614d2f2f17868759c0466a8bbaf2050272231d06a7bfc1622ab7c60a73742c414'

class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.games = list()

    def write_msg(self, user_id, s):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': s})

    def write_keyboard(self, user_id, message, keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'keyboard': keyboard})

    def get_last_msg_text(self, peer_id):
        dictionary = self.vk_session.method('messages.getHistory', {'offset': 1, 'count': 1, 'peer_id': peer_id})
        items = dictionary['items']
        return items[0]['text']

    def parse_message(self, message):
        if message.from_me:
            return
        elif message.text == 'Начать':
            self.message_help(message)
            return
        elif message.text == 'Создать игру':
            self.message_make_game(message)
            return
        else:
            last_text = self.get_last_msg_text(message.peer_id)
            if last_text == 'Отлично!\nВведите название игры.':
                self.message_entered_name(message)
            elif last_text == 'Теперь введите место игры.':
                self

    def make_positive_keyboard(self, message):
        keyboard = json.dumps(
            {'one_time': True,
             'buttons':
                 [[{'action': {
                     'type': 'text',
                     'label': 'makegame'
                 },
                     'color': 'positive'
                 }],
                     [{'action': {
                         'type': 'text',
                         'label': 'deletegame'
                     },
                         'color': 'negative'
                     }]]})
        keyboard = keyboard.replace('makegame', message)
        return keyboard

    def message_help(self, message):
        keyboard = json.dumps(
            {'one_time': True,
             'buttons':
                 [
                     [{'action': {
                         'type': 'text',
                         'label': 'makegame'
                     },
                         'color': 'positive'
                     }],
                     [{'action': {
                         'type': 'text',
                         'label': 'deletegame'
                     },
                         'color': 'negative'
                     }],
                     [{'action': {
                         'type': 'text',
                         'label': 'listgame'
                     },
                         'color': 'primary'
                     }]
                 ]})
        keyboard = keyboard.replace('makegame', 'Создать игру').replace('deletegame', 'Удалить игру')\
            .replace('listgame', 'Просмотреть список игр')
        self.write_keyboard(message.user_id, 'Выберите один из вариантов', keyboard)

    def message_make_game(self, message):
        self.write_msg(message.user_id, 'Отлично!\nВведите название игры.')

    def message_entered_name(self, message):
        temp = game.Game(message.user_id, name=message.text)
        self.games.insert(message.user_id, temp)
        self.write_msg(message.user_id, "Теперь введите место игры.")

    def message_entered_place(self, message):
        temp = self.games.pop(message.user_id)

    def bot_processing(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self.parse_message(event)
                print('Новое сообщение:')

                if event.from_me:
                    print('От меня для: ', end='')
                elif event.to_me:
                    print('Для меня от: ', end='')

                if event.from_user:
                    print(event.user_id)
                elif event.from_chat:
                    print(event.user_id, 'в беседе', event.chat_id)
                elif event.from_group:
                    print('группы', event.group_id)

                print('Текст: ', event.text)
                print()

            elif event.type == VkEventType.USER_TYPING:
                print('Печатает ', end='')

                if event.from_user:
                    print(event.user_id)
                elif event.from_group:
                    print('администратор группы', event.group_id)

            elif event.type == VkEventType.USER_TYPING_IN_CHAT:
                print('Печатает ', event.user_id, 'в беседе', event.chat_id)

            elif event.type == VkEventType.USER_ONLINE:
                print('Пользователь', event.user_id, 'онлайн', event.platform)

            elif event.type == VkEventType.USER_OFFLINE:
                print('Пользователь', event.user_id, 'оффлайн', event.offline_type)

            else:
                print(event.type, event.raw[1:])


vk_bot = VkBot(token='da6532b279b252e0950f614d2f2f17868759c0466a8bbaf2050272231d06a7bfc1622ab7c60a73742c414')
vk_bot.bot_processing()
