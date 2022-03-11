import telebot, wikipedia, re


# Создаем экземпляр бота
bot = telebot.TeleBot('token')


# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang('ru')


# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(text):
    try:
        theme = wikipedia.page(text)
        # Получаем первую тысячу символов
        wikitext = theme.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем все после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходим по строкам, где нет знаков 'равно' (то есть все, кроме  заголовков)
        for string in wikimas:
            if not('==' in string):
                # Если в строке осталось больше трех символов, добавлем ее к нашей
                # переменной и возвращяем утерянные при разделении строк точки на место
                if(len((string.strip()))>3):
                    wikitext2 = wikitext2 + string + '.'
            else:
                break
        # При помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
        # Обрабатываем исключение, которое мог вернуть при запросе модуль wikipedia
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


# Фунция, обрабатывающая команду /start
@bot.message_handler(commads=['start'])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправь мне любое слово и я найду его значение')


# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))


# Запускаем бота
bot.polling(none_stop=True, interval=0)
