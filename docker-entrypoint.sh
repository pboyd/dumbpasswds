#!/bin/sh

python /app/dbsetup.py &&
    exec flask run
