#!/usr/bin/bash
# To test mvc_view.py, first execute that script, and then run this one.
'''
curl -D - http://localhost:8080/project
curl -D - http://localhost:8080/project/ciat
curl -D - http://localhost:8080/project/pymotw
curl -D - http://localhost:8080/project/bogus
curl -D - http://localhost:8080/task
curl -D - http://localhost:8080/task/5
curl -D - http://localhost:8080/task/1
curl -D - http://localhost:8080/task/0

'''
#import requests
import http.client
import mimetypes
conn = http.client.HTTPConnection("127.0.0.1", 8080)
payload = ''
headers = {}
conn.request("GET", "/project", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
'''
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
        
# if __name__ == '__main__':
#     test_do_GET()
