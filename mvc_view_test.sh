#!/usr/bin/env bash
# To test mvc_view.py, first execute that script, and then run this one.

curl -D - http://localhost:8080/project
curl -D - http://localhost:8080/project/ciat
curl -D - http://localhost:8080/project/pymotw
curl -D - http://localhost:8080/project/bogus
curl -D - http://localhost:8080/task
curl -D - http://localhost:8080/task/5
curl -D - http://localhost:8080/task/1
curl -D - http://localhost:8080/task/0


