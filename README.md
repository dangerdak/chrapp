[![Build Status](https://travis-ci.org/dangerdak/chrapp.svg?branch=master)](https://travis-ci.org/dangerdak/chrapp)
Secret Santa

Setup
=====

Postgres
--------
    sudo pacman -S postgresql
    sudo -u postgres -c "initdb --locale en_US.UTF-8 -E UTF8 -D '/var/lib/postgres/data'"
    sudo systemctl start postgresql.service
    sudo -u postgres -c "createuser --interactive"
    suto -u postgres -c "createdb chrapp"

Python
------
    pacman -S python python-virtualenv
    git clone https://github.com/dangerdak/chrapp
    cd chrapp
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt 

Chrapp
------
    export SECRET_KEY=42 DJANGO_SETTINGS_MODULE=chrapp.settings.local DB_USER=chrapp DB_PASSWORD=chrapp
    python manage.py migrate
    python manage.py runserver --settings=chrapp.settings.local
    python manage.py runserver shell_plug
    >>> from django.contrib.sites.models import Site
    >>> one = Site.objects.all()[0]
    >>> one.domain = 'chrappy.com'
    >>> one.name = 'chrappy'
    >>> one.save()
