# Scavenger

This is the repository for all scavenger web infrastructure.

## Quick Start

    cd app/cms/scavenger
    pip install -r requirements.txt
    cp scavenger/settings/local.example.py scavenger/settings/local.py
    ./manage.py --settings scavenger.settings.local migrate
    ./manage.py --settings scavenger.settings.local runserver 127.0.0.1:8000

You will then be able to access the server at http://127.0.0.1:8000
