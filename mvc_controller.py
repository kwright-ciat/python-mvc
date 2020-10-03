#!bin/python3
# customize the above shebang to your environment
import create_tables
import basic_model

def get_endpoints(endpoint='/'):
    if '/' in endpoint:
        endpoints = endpoint.split('/')
    else:
        endpoints = ['', endpoint[1:], '']
    
    if endpoints[1] == 'project': 
        if len(endpoints) < 3:
            project_name = '%'
            projects = '\r\n'.join(basic_model.get_projects(project_name=project_name))
        else:
            project_name = endpoints[2]
            if project_name.isalpha():
                projects = '\r\n'.join(basic_model.get_projects(project_name=project_name))
            else:
                projects = None 
        
        return projects
    
    elif endpoints[1] == 'task':
        if len(endpoints) < 3:
            task_id = '%'
        else:
            task_id = endpoints[2]
        tasks ='\r\n'.join(basic_model.get_tasks(task_id=task_id))
        return tasks

def get_endpoints_test():
    tests = ['/project', '/task', '/project/ciat', '/project/pymotw'
            '/task/1', '/task/3', '/bogus', '/bogus/1']
    for test in tests:
        print('Testing {}'.format(test))
        print(get_endpoints(test))

if __name__ == '__main__':
    get_endpoints_test()
