#!bin/python3
'''
Test endpoints of the mvc_view

'''
from mvc_view import ip_default, port_default
import http.client
import mimetypes

def test_do_GET():
    payload = ''
    headers = {}
    endpoints = ['/project','/project/ciat','/project/pymotw','/project/bogus',
                 '/task', '/task/5','/task/1', '/task/0']
    global ip_default
    if ip_default == '0.0.0.0': ip_default = '127.0.0.1'
    for endpoint in endpoints:
        print(ip_default, port_default)
        conn = http.client.HTTPConnection(ip_default, port_default)
        conn.request("GET", endpoint, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

        
if __name__ == '__main__':
    test_do_GET()

# To test mvc_view.py, first execute that script, and then run this one.
'''
Command line testing
curl -D - http://localhost:8080/project
curl -D - http://localhost:8080/project/ciat
curl -D - http://localhost:8080/project/pymotw
curl -D - http://localhost:8080/project/bogus
curl -D - http://localhost:8080/task
curl -D - http://localhost:8080/task/5
curl -D - http://localhost:8080/task/1
curl -D - http://localhost:8080/task/0

'''
'''
Python 2.7 Code uses requests module

import requests

def test_do_GET():
    
    Test the do_GET function
    
    Use a list of urls to get for success and for failure.
    
  
    url_list = ["http://127.0.0.1:8080/project","http://127.0.0.1:8080/project/ciat", 
                "http://127.0.0.1:8080/task", "http://127.0.0.1:8080/task/1"]
    payload = {}
    headers= {}
    for url in url_list:
        response = requests.request("GET", url, headers=headers, data = payload)
        print(response.text.encode('utf8'))
'''