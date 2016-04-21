#!/usr/bin/env bash

sleep 3
uwsgi --http 0.0.0.0:5000 --module api --callable flask_app