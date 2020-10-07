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

import mvc_model

def validate_project_fields(fields):
    '''
    Return only valid project fields
    
    Ensure no invalid fields or values are used
    '''
    
    valid_project = ['project_name','description','deadline']
    valid_fields = []
    for field in fields:
        if field not in valid_project:
            return 400
        else:
            valid_fields.append(field)
            
        if field == valid_project[0]:
            project_name = fields[field]
            if not project_name.isalnum():
                return 400
        elif field == valid_project[1]:
            description = fields[field]
            if not description.isprintable():
                return 400
        elif field == valid_project[2]:
            description = fields[field]
            if not description.isprintable():
                return 400
        return valid_fields
            
def post_endpoints(fields, endpoint='/'):
    print(fields, endpoint)
    if '?' in endpoint:
        qm = endpoint.index('?')
        endpoint = endpoint[:qm] # delete the question mark and everything after it
    if '/' in endpoint:
        endpoints = endpoint.split('/')
    else:
        endpoints = ['', endpoint[1:], '']
    
    print (test_validate_project_fields(fields))
    if endpoints[1] == 'project' and endpoints[2] == 'create': 
        if len(endpoints) < 4:
            projects = 400
        else:
            project_name = endpoints[3]
            print (project_name)
            if project_name.isalnum():
                projects = '\r\n'.join(mvc_model.add_project(fields))
            else:
                projects = 400 
        
        return projects

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

def test_get_endpoints():
    tests = ['/project', '/task', '/project/ciat', '/project/pymotw'
            '/task/1', '/task/3', '/bogus', '/bogus/1']
    for test in tests:
        print('Testing get_endpoints {}'.format(test))
        print(get_endpoints(test))

def test_post_endpoints():
    tests = ['/project/create?project_name=CREATE','/project/create?project_name=C4CREATE']
    for test in tests:
        print('Testing post_endpoints {}'.format(test))
        print(post_endpoints({'project_name': 'Create'},test))
        
def test_validate_project_fields(fields):
    print('Testing test_validate_project_fields({}', test_validate_project_fields({})) 
    return validate_project_fields()

if __name__ == '__main__':
    test_get_endpoints()
    test_post_endpoints()
    test_validate_project_fields({})
