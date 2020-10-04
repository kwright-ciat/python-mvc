#!/bin/env bash
# Keith Wright
# Start the application properly by activating the Python 3.7 virtual environment
bin/activate
# Before the first time application is run the database and tables must be created
python3 mvc_model_create.py
# After the first time it is run the application can be started with creating the tables
python3 mvc_view.py
