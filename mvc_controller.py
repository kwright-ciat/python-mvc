#!bin/python
'''
This module implements the Controller in the MVC design pattern 

MVC Controllers only communicate with the Model and the View.
To use the module, it should be imported by the View module,
and when the MVC View module makes requests through function calls,
this Controller will respond to the View.

This Controller imports the MVC module, so that it can make 
requests of the functions of the MVC Model module.  
'''

from pprint import pprint
from datetime import datetime
import random

from mvc_app import testing, ISO_8601_DATE
import mvc_model
from _sqlite3 import IntegrityError



def validate_project_fields(fields):
    '''
    Return only valid project fields
    
    Ensure no invalid fields or values are used
    '''
    
    valid_project = ['project_name','description','deadline']
    valid_fields = []
    invalid_fields = []
    for field in fields:
        if field not in valid_project:
            print('Invalid field {}\n'.format(field))
            invalid_fields.append(field)
        else:
            print('Valid field {}\n'.format(field))
            valid_fields.append(field)
            
        if field == valid_project[0]:
            project_name = fields[field]
            if not project_name.isalnum():
                print('Invalid project_name\n')
                invalid_fields.append(field)
        elif field == valid_project[1]:
            description = fields[field]
            if not description.isprintable():
                print('Invalid description\n')
                invalid_fields.append(field)
        elif field == valid_project[2]:
            deadline = fields[field]
            if not deadline.isprintable():
                print('Invalid deadline\n')
                invalid_fields.append(field)
    else: # this is executed when the for loop reaches the end of the fields list
        if len(invalid_fields) > 0:
            print('Invalid fields {}\n'.format(invalid_fields))
            return 400, invalid_fields
        else:
            print('Return valid fields {}\n'.format(invalid_fields))
            return 200, valid_fields
            
def post_endpoints(fields, endpoint='/'):
    print('mvc_controller.py post_endpoints endpoint {}, fields {}\n'.format(endpoint,fields))
    if '?' in endpoint:
        qm = endpoint.index('?')
        endpoint = endpoint[:qm] # delete the question mark and everything after it
    if '/' in endpoint:
        endpoints = endpoint.split('/')
    else:
        endpoints = ['', endpoint[1:], '']
    
    if endpoints[1].lower() == 'project':
        if endpoints[2].lower() == 'create': 
            print ('\nmvc_controller.py post_endpoint Validate_project_fields: {}\n'.format(fields))
            status_code, valid_fields = validate_project_fields(fields)
            print (status_code, fields)
            if status_code == 400:
                print ('\nmvc_controller.py post_endpoint Invalid_project_fields: {}\n'.format(fields))
                return 400
            else:
                project_name = fields['project_name']
                print ('\nmvc_controller.py post_endpoint project_name: {}'.format(project_name))
                new_project = mvc_model.add_project(fields)
                if new_project[0] == 'IntegrityError':
                    print('Duplicate project name')
                    return new_project
            return new_project
        elif endpoints[2].lower() == 'delete': 
            print ('\nmvc_controller.py post_endpoint Validate_project_fields: {}\n'.format(fields))
            status_code, valid_fields = validate_project_fields(fields)
            print (status_code, fields)
            if status_code == 400:
                print ('\nmvc_controller.py post_endpoint Invalid_project_fields: {}\n'.format(fields))
                return 400
            else:
                project_name = fields['project_name']
                print ('\nmvc_controller.py post_endpoint project_name: {}'.format(project_name))
                deleted_project = mvc_model.delete_project(fields)
            return deleted_project  
        elif endpoints[2].lower() == 'update': 
            print ('\nmvc_controller.py post_endpoint Validate_project_fields: {}\n'.format(fields))
            status_code, valid_fields = validate_project_fields(fields)
            print (status_code, fields)
            if status_code == 400:
                print ('\nmvc_controller.py post_endpoint Invalid_project_fields: {}\n'.format(fields))
                return 400
            else:
                project_name = fields['project_name']
                print ('\nmvc_controller.py post_endpoint project_name: {}'.format(project_name))
                updated_project = mvc_model.update_project(fields)
            return updated_project                    

def get_endpoints(endpoint='/'):
    if '/' in endpoint:
        endpoints = endpoint.split('/')
    else:
        endpoints = ['', endpoint[1:], '']
    
    if endpoints[1] == 'project': 
        if len(endpoints) < 3:
            project_name = '%'
            projects = '\r\n'.join(mvc_model.get_projects(project_name=project_name))
        else:
            project_name = endpoints[2]
            if project_name.isalpha():
                projects = '\r\n'.join(mvc_model.get_projects(project_name=project_name))
            else:
                projects = 400 
        
        return projects
    
    elif endpoints[1] == 'task':
        if len(endpoints) < 3:
            task_id = '%'
        else:
            task_id = endpoints[2]
        tasks ='\r\n'.join(mvc_model.get_tasks(task_id=task_id))
        return tasks
    else:
        return 500
    

def test_get_endpoints():
    tests = ['/project', '/task', '/project/ciat', '/project/pymotw'
            '/task/1', '/task/3', '/bogus', '/bogus/1']
    for test in tests:
        print('Testing get_endpoints {}'.format(test))
        result = get_endpoints(test)
        if result == 400:
            exit(400)
            

def test_post_endpoints():
    fields = {'project_name': 'Create', 'description': 'mvc_controller.py test_post_endpoints', 'deadline':'2012-12-12'}
    
    project_name = str(random.randint(1,10000))
    description = 'Test project {}'.format(project_name)
    deadline = datetime.strftime( datetime.now(), ISO_8601_DATE)
    random_fields = {'project_name': project_name, 'description': description, 'deadline': deadline}
    tests = ['/project/create', '/project/update', '/project/delete']
    for test in tests:
        print('Testing with fields: {}\nfor post_endpoints: {}.'.format(fields,test))
        print(post_endpoints(fields,test))
        print(post_endpoints(random_fields,test))
        
def test_validate_project_fields():
    field_list =[ {'project_name': 'Create', 'description': 'test_post_endpoints', 'deadline':'2112-12-12'},
                   {'project_name': '*', 'description': 'test_post_endpoints', 'deadline':'2112-12-12'}]
    print('Testing test_validate_project_fields(fields)') 
    pprint(field_list) 
    for field in field_list:
        print('Testing test_validate_project_fields({})'.format(field))
        print('Result of test', validate_project_fields(field))

if __name__ == '__main__':
    # test_validate_project_fields()
    # test_get_endpoints()
    test_post_endpoints()

