#!/usr/bin/bash
# To test mvc_view.py, first execute that script, and then run this one.

curl http://localhost:8080/project
curl http://localhost:8080/project/ciat
curl http://localhost:8080/project/pymotw
curl http://localhost:8080/project/bogus
curl http://localhost:8080/task
curl http://localhost:8080/task/5
curl http://localhost:8080/task/1
curl http://localhost:8080/task/0


