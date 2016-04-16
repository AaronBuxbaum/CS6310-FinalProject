#!/usr/bin/env bash

# Build local
npm install --dev
npm install gulp
gulp build

touch /tmp/app-initialized
uwsgi --http-socket /tmp/nginx.socket --module api --callable app