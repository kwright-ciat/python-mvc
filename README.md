# python-mvc
* Demonstrate MVC design pattern 
* Use Test Driven Development to facilitate the design
* Use Python 3.7 in a virtual environment
* Use SQLite3 for a serverless database
* Use Dockerfile to implement a container

# Application Testing
## To start the application execute:

#### ./mvc_app.sh

## To test the application execute:

#### ./mvc_view_test.sh

## To test each of the mvc components except the mvc_view.py, you can execute them, instead of importing them:

#### ./mvc_model.py
#### ./mvc_controller.py

## To test the mvc_view.py use the script that tests the applicaton: 

#### ./mvc_view_test.sh

# Docker Testing
## To build image with a tag of "pymvc:latest" for an image name of pymvc with a version of latest:

#### docker build -t pymvc:lastest .

## To run a container named "mvc1" using the "pymvc" image which maps the host port 8080 to the container 8080:

#### docker run -p 8080:8080 --name mvc1 pymvc 

## To test the "mvc1" container from the host computer:

#### curl http://localhost:8080/project
#### curl http://localhost:8080/project/ciat
#### curl http://localhost:8080/task
#### curl http://localhost:8080/task/5

# Windows Docker Issues
* Docker on Windows 10 connects to the container differently than Linux.
* Using the docker-machine.exe  ip will show your IP usually, 192.168.99.101.
* Use the curl command to test the app
* curl 192.168.99.101:8080/project
* curl 192.168.99.101:8080/project/ciat
* curl 192.168.99.101:8080/task
* curl 192.168.99.101:8080/task/5
