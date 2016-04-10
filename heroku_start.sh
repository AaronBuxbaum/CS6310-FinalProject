#!/usr/bin/env bash

touch /tmp/app-initialized
uwsgi --socket /tmp/nginx.socket --module api --callable app