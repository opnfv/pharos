#!/bin/bash
PIDS=$(ps -ef | grep laas/source/ | grep python | awk '{print $2}')

kill ${PIDS[*]}
