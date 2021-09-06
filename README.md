# Рандомайзер Ютуб видосов

Скрипт получает все видики из плейлиста и рандомизирует их прямо в плейлисте

## Предыстория

У меня есть [плейлист с ебанутыми клипами](https://www.youtube.com/playlist?list=PLdb8DVmvU9i5bGINNz10f-ga_bqD41O4q), их
там штук 200. Соответственно, хочется иметь возможность запускать их в рандомном порядке.

Ютуб не умеет рандомизировать видосы нормально: те видосы, которые ты посмотрел, могут выпасть ещё раз. Причем может
случиться ситуация, когда ты попадешь в петлю рандома, где рандом будет показывать тебе одни и те же видосы.

Есть [решение](https://youtube-playlist-randomizer.bitbucket.io/) этой проблемы - этот сервис нормально рандомит видосы,
но например, нельзя смотреть видео с ограничением по возрасту.

Есть мысль, что будучи авторизованным, такие видео можно будет
смотреть ([видимо незя](https://www.reddit.com/r/youtube/comments/k536y3/any_way_to_play_age_restricted_youtube_videos))

Ещё мысль, что в апишке есть [возможность менять порядок плейлиста](https://developers.google.com/youtube/v3/docs/playlistItems) => приложуха будет перемешивать плейлист и все заебок будет


## Apps Script

- Спустя какое-то время скрипт перестал работать, выводится 403 ошибка
- Я переписал [скрипт на Apps Script](https://github.com/potykion/yt-shuffle/blob/master/yt-shuffle.gs) и проблемы с кредами решились

## Детали

- У Youtube Data API есть [квота](https://developers.google.com/youtube/v3/getting-started#quota) в 10к юнитов в день
- 1 запрос `playlistItems/update` стоит 50 юнитов - в день можно ~200 видосов зарандомить


## Сетап

1. Создаем проект в Google Cloud Platform
2. Включаем Youtube Data API в https://console.cloud.google.com/apis/library
3. Переходим в Credentials + создаем OAuth client ID с типом Desktop
4. Качаем client_secret.json

   ![client secret download](img.png)

5. Закидываем в папку с проектом, создаем `.env`-файл с названием client_secret.json файла:

   ```
   CLIENT_SECRET_JSON=client_secret_843289797199-ac7kigb3b8qv3rmu3eis7rr93dfl0k4u.apps.googleusercontent.com.json
   ```

6. Ставим зависимости: `poetry install`

7. Запускаем скрипт: `python main.py`

8. При запуске будет предожено перейти по гугл-ссылке, там может быть такое:

   ![takoe](img_1.png)

   В таком случаем прожимаем `Advanced > Go to project...`

9. Все принимаем, в конце будет предложено скопировать код, типа `4/1AY0e-g5MsByqd2EJ6fCg...` - его вставляем
   в `Enter the authorization code:` из пункта 7

10. Скрипт должен начать грузить инфу о видиках и рандомизировать их

