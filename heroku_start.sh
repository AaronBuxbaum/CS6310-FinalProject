#!/usr/bin/env bash

touch /tmp/app-initialized
uwsgi --http-socket /tmp/nginx.socket --module api --callable app