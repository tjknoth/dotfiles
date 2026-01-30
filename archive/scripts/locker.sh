#!/bin/bash

exec xautolock -detectsleep -corners -000 -time 10 -locker "lock -n -- scrot -z" &
