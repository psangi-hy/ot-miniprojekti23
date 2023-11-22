#!/bin/bash

poetry run python3 src/run.py &

while ! curl -s http://localhost:5000/ping > /dev/null; do
  sleep 1
done

poetry run robot src/tests

status=$?

kill $(lsof -t -i:5000)

exit $status