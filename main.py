# aGrIk's StickBot v1
# Простейшая фигня, которая шлёт стикеры из подсказок

#
# Конфигурация
#

# access_token - ваш токен ВКонтакте. Обязательный параметр.
access_token = ""

# DELAY - задержка отправки сообений в миллисекундах. 0 по умолчанию.
DELAY = 0

#
# Конфигурация
#


from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from time import sleep

def sticker(sticker_id):
    vk.messages.send(peer_id=event.peer_id, sticker_id=sticker_id, random_id=0,)

vk_session = VkApi(token=access_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
print("Загрузка стикерпаков...")
stickers_raw = vk.store.getStickersKeywords(need_stickers=0)["dictionary"]
print("Парсинг...")
sticks = []
for stick in stickers_raw:
    curr_sticks = []
    for st in stick["stickers"]:
        curr_sticks.append(st["sticker_id"])
    sticks.append({"w": stick["words"], "s": curr_sticks})
del curr_sticks, stickers_raw, stick, st
print("Успешно. Запуск...")

while True:
    for event in longpoll.listen():
        if event.from_me and event.text != "":
            text = event.text.lower()
            print(f"\nНовое сообщение \"{event.text}\"")
            for x in sticks:
                if text in x["w"]:
                    print(f'Обнаружены следующие стикеры: {x["s"]}')
                    for y in x["s"]:
                        sticker(y)
                        sleep(DELAY / 1000)