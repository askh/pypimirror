# Конфигурационные файлы для запуска частичного зеркала PyPi используя docker-compose

Конфигурационные файлы предназначены для развёртывания зеркала PyPi для
локального применения, например, на случай, если доступ к серверам PyPi окажется
заблокирован. Используется [devpi](https://devpi.net/), который запускается
используя docker-compose.

Пакеты при установке будут сохраняться в локальном репозитории, что позволит не
скачивать повторно те же файлы через Интернет.

Полное зеркало pypi.org не создаётся, сохраняются только пакеты, которые вы
будете скачивать через своё зеркало.

В данном примере используется протокол HTTP, если вам необходимо использовать
защищённое соединение, то реализовать это можно, например, при помощи Apache или
nginx в качестве обратного прокси-сервера, используя приложение certbot для
получения бесплатного сертификата, в этом случае вам возможно потребуется
ограничить работу сервера только на локальном интерфейсе, для чего можно создать
в каталоге настроек файл .env (образец находится в файле .env.example), который
будет содержать следующую строку:

```
SERVER_IP=127.0.0.1
```

Естественно после этого нужно пересобрать образ.

## Установка

### Клонируйте репозиторий

```
git clone https://github.com/askh/pypimirror.git
```
### Укажите настройки зеркала

При необходимости изменить настройки создаваемого образа, скопируйте файл
.env.example под именем .env и отредактируйте его. В первую очередь обратите
внимание на переменную ROOT_PASSWORD, если её не установить, то по умолчанию
пароль для пользователя root в devpi-server будет пустым (вряд ли это то, чего
бы вы хотели).

### Соберите образ и запустите сервис

```
cd pypimirror
docker-compose up -d
```

## Использование

Чтобы при установке приложение pip подключалось к вашему зеркалу, нужно или
передать ему его адрес через опции командной строки, либо создать
конфигурационный файл, в котором будут указаны соответствующие значения.

Далее предполагается, что адрес вашго зеркала — http://mirror.example.com:3141,
для примера будем устанавливать пакет virtualenv.

### Использование опций командной строки

```
pip install -v --timeout 120 --trusted-host mirror.example.com -U -i http://mirror.example.com:3141/root/pypi/+simple/ virtualenv
```

### Использовние конфигруационного файла

Создайте файл ~/.config/pip/pip.conf следующего содержания (замените адреес
mirror.expample.com на адрес вашего зеркала):

```
[global]
index-url=http://mirror.example.com:3141/root/pypi/+simple/
trusted-host=mirror.example.com
timeout=120
```

После этого устанавливайте пакеты обычным образом, например:

```
pip install virtualenv
```
