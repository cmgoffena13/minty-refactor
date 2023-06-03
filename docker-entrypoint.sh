#!/bin/bash
flask db upgrade
exec gunicorn -b :5000 --access-logfil - --error-logfile - minty:app