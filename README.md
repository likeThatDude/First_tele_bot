# Телеграм-Бот для поиска ресторанов, отелей и прогноза погоды

<u> Описание проекта</u>
-


Этот проект представляет собой телеграм-бота, разработанного с использованием <u>Python</u> и API
различных сервисов,   
таких как:  [Rapid API](https://rapidapi.com/hub), [OpenWeatherMap](https://openweathermap.org/),
чтобы выполнять следующие функции:

* Поиск ресторанов в указанном
  местоположении. [Worldwide Restaurants](https://rapidapi.com/ptwebsolution/api/worldwide-restaurants)
* Поиск отелей и бронирование номеров. [Booking.com](https://rapidapi.com/tipsters/api/booking-com)
* Предоставление актуальной информации о погоде для выбранного города. [OpenWeatherMap](https://openweathermap.org/)
* Ведение истории запросов пользователей.

<u> Установка и запуск</u>
-

1. **Клонирование репозитория**
    ```
    git clone https://github.com/likeThatDude/first_tele_bot.git
    cd telegram-bot
    ```
2. **Установка зависимостей**  
   Убедитесь, что у вас установлен Python 3 и pip. Затем установите необходимые библиотеки:
    ```
    pip install -r requirements.txt
    ```
3. **Настройка API ключей**   
   Получите API ключи для сервисов, используемых в боте
   и добавьте их в файл [.env](.env).
   > Для этого вам нужно зарегистрировваться на сайте [Rapid API](https://rapidapi.com/hub).  
   для получения ключей:   
   [Booking.com](https://rapidapi.com/tipsters/api/booking-com)   
   [Worldwide Restaurants](https://rapidapi.com/ptwebsolution/api/worldwide-restaurants)   
   [Telegram](https://t.me/BotFather) ссылка на бота для получения токена.
   >
   > Пример файла [.env](.env):
   >> BOT_TOKEN='Токен полученный у @BotFather в телеграм'  
   WEATHER_TOKEN='ключ от [OpenWeatherMap](https://openweathermap.org/)'   
   HOTEL_KEY='ключ от [Booking.com](https://rapidapi.com/tipsters/api/booking-com)'   
   REST_KET='ключ от [Worldwide Restaurants](https://rapidapi.com/ptwebsolution/api/worldwide-restaurants)'

4. **Запуск бота**   
   Запуск бота производится с файла [main.py](main.py)

<u> Использование</u>
-

1. **Добавление бота в Telegram**  
   Перейдите в Telegram и найдите бота по его имени. Начните чат с ботом и следуйте инструкциям.


2. **Команды бота**   
   Бот поддерживает следующие команды:
    * _**Стартовые команды:**_
      > **/start** - запуск бота     
      **/help** - вывод справки
    * _**Основыные команды:**_
      > **/Отель** - Поиск отелей и получение информации    
      **/Рестораны** - Поиск ресторанов в указанном местоположении   
      **/Погода** - Получение актуальной информации о погоде для выбранного города  
      **/История_запросов** - Отображение истории запросов пользователя.

<u> База данных</u>
-

База данных реализована при помощи **_SQLite_**.   
Сама база данных состоит из двух таблиц **_users_** и **_request_history_**.   
В **_users_** сохраняется информация о пользователях (регистрация происходит автоматически при запуске бота).   
В **_request_history_** сохраняется вся история взаимодействия с ботом.   
Сама база данных: [bot_database.db](bot_database.db)

<u> Разработчик</u>
-

* __Горбатенко Иван__
  > [GitHub](https://github.com/likeThatDude)  
  **Email**: 1995van95@gmail.com
