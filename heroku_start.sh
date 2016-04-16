#!/usr/bin/env bash

node node_modules/gulp/bin/gulp build

touch /tmp/app-initialized
uwsgi --http-socket /tmp/nginx.socket --module api --callable app