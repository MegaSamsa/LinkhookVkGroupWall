================================================
Сбор ссылок на посты сообщества ВК
================================================

Скрипт осуществляет сбор ссылок на новые посты в заданной группе ВК. Собранные ссылки записываются в Excel таблицу.

Файл конфигурации config.json имеет параметры:
    group_id        | str   |   id ВК группы
    access_token    | str   |   токен доступа
    version         | str   |   версия API
    check_interval  | int   |   время таймера

Структура проекта:
LinkhookVkGroupWall | Корневая папка проекта
    __pychache__    | Программная папка для оптимизации кода
    .gitignore      | Игнорирование публикации config.json и links.xlsx в репозитории
    config.json     | Файл конфигурации
    init.py         | Файл с импортом библиотек
    links.xlsx      | Таблица с собранными ссылками
    main.py         | Главый исполняемый файл
    readme.txt      | Информация о проекте в формате txt
    run.bat         | Пакетный файл для быстрого запуска

Заполнение config.json:
    Получение id группы (group_id):
    Перейти в нужную группу и скопировать id. Если у группы есть маска id, можно скопировать ссылку на любой пост в группе и оттуда достать id;
    Запрос access токена (access_token):
    Перейти по ссылке: https://oauth.vk.com/authorize?client_id=YOUR_APP_ID&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall,groups&response_type=token&v=5.131, где YOUR_APP_ID - id вашего ВК приложения. Далее нужно перейти по получившейся ссылке, разрешить доступ к данным, взять из ссылки token - это и будет access_token в config.json (более подробная инструкция здесь: https://www.pandoge.com/socialnye-seti-i-messendzhery/poluchenie-klyucha-dostupa-access_token-dlya-api-vkontakte);
    version = "5.131";
    check_interval = 60.

При разработке использовался язык Python версии 3.10.5
Используемые библиотеки:
    requests;
    time;
    json;
    os;
    pandas.