#!/bin/bash
gunicorn backtv_django.wsgi:application --bind=0.0.0.0:8080 --log-level=info --log-file -