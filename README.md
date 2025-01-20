## Описание
В этой работе создается основной контейнер с инстансом docker и реплика. 

Далее к основному контейнеру подключается debezium, который данные из базы переносит в kafka. Далее dmp сервис читает данные из kafka и мапит данные от туда в dwh таблицу, построенную по модели data vault. 

Перед запуском надо убедиться, что порты, которые используют конейнеры, не заняты.

Запуск выполняется коммандой:

```
sh ./up-divide.sh
```
## Описание docker-compose

### Контейнеры postgres_master и postgres_slave
В параметре *volumes* мапим все локальные скрипты + конфиги внутрь докера. (кроме slave - конфига в мастер, ибо мастер не реплика и будут проблемы)

Порты мастера и реплики 5432 и 5433 соответвенно. Пробовал поставить мастера на другой порт, но реплика тогда не работает. Но по итогу так и не смог, что очень странно.

В фале postgresql.conf есть параметр *shared_buffers*. Могут возникать пробемы с нехваткой памяти, тогда ее можно умешать.

Дополнительно у postgres_master выполняется проверка здоровья, т.к остальные контейнеры зависят от него.

### Контейнеры zookeeper1 и broker1
Инициализируют kafka + базовые настройки.

### Контейнер debezium1 и debezium-ui1
Инициализирует debezium и debezium-ui1, где можно посмотреть соединения с БД-шками.

### Контейнер rest-proxy1
Через него мы обращаемся к kafka, чтобы узнать инфу про кластеры.

### Контейнер dmp_service
Образ контейнера создаем сами. Контейнер зависит от кафки и dmp базы. Читает сообщение из kafka и записывает в dmp базу.

### Контейнер postgres_dwh
Инициализирует БД со структурой data vault.

## Описание DWH базы
Каждая таблица представляет одну из трех сущностей: hub, satellite, link. Hub - базовая сущность с фиксироваными полями (Я выделил бронь, билет, аэропорт, самолет, перелет). Сущность человека (пользователя) выделять не стал, т.к явно определить человека и прописать БК для него нельзя (можно поемнять любые данные: серию и номер паспорта, имя и фамилию). Так что явно по данным нельзя инициализировать человека нельзя. Даже когда мы смотрим статус биета, мы вводим данные именно БИЛЕТА. Satellite - описание полей у хаба. У каждого хаба есть соответсвующий sattelite. Link - связь между хабами. Так, например, перелет имеет аэропорт отправления и назначения, билет привязан к брони, у самолета есть места и т.д.

Схема описана в файле https://github.com/klyshnikov/dwh-hw1/blob/main/dmp_service/dbdiagram.pdf

Скрипт заполнения (ddl) https://github.com/klyshnikov/dwh-hw1/blob/main/dwh-init/ddl_dwh.sql

Почему выбрана именно такая структура. На мой взгял она проще чем data vault 2.0, и использет интуитивно понятную модель базовых сущностей и связец между ними. (Плюс вариативность в том, что могут появиться новые поля и таблицы, источники данных, которые можно записать в новые сателиты).

 ## Описание dmp слоя
Dockerfile: https://github.com/klyshnikov/dwh-hw1/blob/main/dmp_service/Dockerfile

В нем инициализируется образ с питоном + устанавливаются нужные библиотеки. Основной исполняемый файл: https://github.com/klyshnikov/dwh-hw1/blob/main/dmp_service/dmp.py

В нем может и не лучшим образом, но происходит следующее: создаются подключение к разным топикам кафки (каждый отвечает за свою таблицу), читаются сообщения и вычленяются данные из json.

Т.е это данные из оригинальной таблицы. Далее создаются запросы в dwh. Затем коннектимся к нему и выполняем запросы. Т.к мы одновременно должны читать из разных топиков сообщения, будем каждую функцию выполнять в отдельном потоке.

## Порядок работы программы:
1. Останавливаем все контейнеры, чтобы начать работать с нуля.
2. Удаляем data и data-slave
3. Заходим в master и выполяем инициализацию внутри контейнера
4. Копируем конфиги в slave
5. Поднимаем slave, master
6. Выполняем скрипт, который инициализиет БД.
7. Поднимаем все остальные контейнеры.
8. Создаем подключение  db <-> debezuim <-> kafka

## Проверка

### Проверка работы реплики
Проверим, что репликация работает. Через любую IDE можно подключиться к 2 контейнерам и убедиться, что базы полностью совпадают

![alt text](https://github.com/klyshnikov/dwh-hw1/blob/main/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202024-11-04%2000-57-36.png)

### Проверка работы debezium

