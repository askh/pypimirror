# Конфигурационные файлы для запуска зеркала пакетов pip

Конфигурационные файлы предназначены для развёртывания зеркала pypi для
локального применения, например, на случай, если доступ к серверам pypi
окажется заблокирован. Используется модуль devpi, который запускается
используя docker-compose.

Пакеты при установке будут сохраняться в локальном репозитории, что позволит
не скачивать повторно те же файлы через Интернет.

Полное зеркало pypi.org не создаётся, сохраняются только пакеты, которые вы
будете скачивать через своё зеркало.

В данном примере используется протокол HTTP, если вам необходимо использовать
защищённое соединение, то реализовать это можно, например, при помощи Apache или
nginx в качестве обратного прокси-сервера, используя приложение certbot для
получения бесплатного сертификата, в этом случае вам возможно потребуется
изменить значение параметра --host в инструкции CMD в файле Dockerfile (чтобы
сервер принимал запросы по незащищённому соединению только с локального адреса).

## Установка

### Клонируйте репозиторий

```
git clone https://github.com/askh/devpisrv.git
```

### Соберите сервис

```
cd devpisrv
docker-compose build
```

### Запустите сервис

```
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
