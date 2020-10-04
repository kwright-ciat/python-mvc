#!bin/python3
'''
This module implements the Controller in the MVC design pattern 

MVC Controllers only communicate with the Model and the View.
To use the module, it should be imported by the View module,
and when the MVC View module makes requests through function calls,
this Controller will respond to the View.

This Controller imports the MVC module, so that it can make 
requests of the functions of the MVC Model module.  
'''
# customize the above shebang to your environment
import mvc_model

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
                projects = None 
        
        return projects
    
    elif endpoints[1] == 'task':
        if len(endpoints) < 3:
            task_id = '%'
        else:
            task_id = endpoints[2]
        tasks ='\r\n'.join(mvc_model.get_tasks(task_id=task_id))
        return tasks

def get_endpoints_test():
    tests = ['/project', '/task', '/project/ciat', '/project/pymotw'
            '/task/1', '/task/3', '/bogus', '/bogus/1']
    for test in tests:
        print('Testing {}'.format(test))
        print(get_endpoints(test))

if __name__ == '__main__':
    get_endpoints_test()
