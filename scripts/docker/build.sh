#!/bin/bash

docker build --build-arg UID=$(id -u) --build-arg USER_GID=$(id -g) -t ratatai .
