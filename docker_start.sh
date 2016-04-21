#!/usr/bin/env bash

sleep 10
uwsgi --http 0.0.0.0:5000 --module api --callable app