#!/bin/bash

exec xautolock -detectsleep -time 5 -locker "lock -- scrot -z" &
