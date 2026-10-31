#!/usr/bin/env bash
# Render 빌드 스크립트
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
