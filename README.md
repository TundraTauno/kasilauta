# kasilauta
Attempt to make 8chan like imageboard in Django.

## Install
You need to have MySql/MariaDB with kasilauta/kasilauta as user/password combo in localhost:3306.
```
pip3 install -r requirements.txt --user
./manage.py makemigrations
./manage.py migrate
./manage.py createsuperuser
```
Rename `example.env` -> `.env`. Notice: it must be explicitly `.env`, not `my.env` for example.
```
./manage.py runserver
```
Go to `https://localhost:8000`

## Usage
At first, imageboard will be usable only through /admin panel, because there will be lots of changes and it doesn't make sense to design UI before most of the board functionality has been stabilized.

## Todo
- User is able to create boards (like in 8chan)
- Notifications between users
- Support for using Amazon S3 as media backend
- Add other media support: video, gif, etc
- Reporting, ban system and control between them
