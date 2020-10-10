#!bin/python
'''
This module implements the Model in the MVC design pattern 

MVC Models only communicate with the Controller.
To use the module, it should be imported by the Controller module
and when the MVC View module makes requests through function calls,
the Controller will make function calls to this Model module.

This Controller imports a module named mvc_module_create, so that the 
database with db_filename gets created.  
'''

from datetime import datetime
import os
import random
import sqlite3
import sys

from mvc_app import ISO_8601_DATE, db_filename_default, schema_filename_default, testing

def exists_db(db_filename=db_filename_default):
    db_exists = os.path.exists(db_filename)
    return db_exists
    
def create_db(db_filename=db_filename_default, schema_filename=schema_filename_default):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
            
        if testing:
            print('Schema file: {}'.format(schema))
            print('Inserting initial data')
        cursor.executescript(schema)
        


#         conn.executescript("""
#         insert into project (name, description, deadline)
#         values ('pymotw', 'Python Module of the Week',
#                 '2016-11-01');
# 
#         insert into project (name, description, deadline)
#         values ('ciat', 'CIS280A Cisco DevNet',
#                 '2020-10-01');
# 
#         insert into task (details, status, deadline, project)
#         values ('Create python-mvc Git Repository', 'done', '2020-10-02',
#                 'ciat');
# 
#         insert into task (details, status, deadline, project)
#         values ('Get basic /project and /task API endpoints working', 'wip', '2020-10-03',
#                 'ciat');
# 
#         insert into task (details, status, deadline, project)
#         values ('write about select', 'done', '2016-04-25',
#                 'pymotw');
# 
#         insert into task (details, status, deadline, project)
#         values ('write about random', 'waiting', '2016-08-22',
#                 'pymotw');
# 
#         insert into task (details, status, deadline, project)
#         values ('write about sqlite3', 'active', '2017-07-31',
#                 'pymotw');
#         """)

        
def get_tasks(db_filename=db_filename_default, task_id='%'):

        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()

            if task_id == '%':
                query = """
                select id, priority, details, status, deadline from task
                order by deadline, priority
                """
            else:
                query = """
                select id, priority, details, status, deadline from task
                where id = {}
                order by deadline, priority
                """.format(task_id)
            
            if testing:
                print ('\nmvc_model.py get_task query "{}"\n'.format(query))
            cursor.execute(query)
    
            print ('\nmvc_model.py get_task query results:\n')
            rows = []
            for row in cursor.fetchall():
                task_id, priority, details, status, deadline = row
                rows.append('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
                    task_id, priority, details, status, deadline))
                if testing:
                    print(rows) 
            
            return rows

def get_projects(db_filename=db_filename_default, project_name='%'):

        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            if project_name == '%':
                query = """
                select name, description, deadline
                from project
                order by deadline
                """
            else:
                query = """
                select name, description, deadline
                from project where name = "{}"
                """.format(project_name)
        
            if testing:
                print ('mvc_model.py get_projects query: \n{}\n'.format(query))
            cursor.execute(query)
        
            rows = []
        
            print ('mvc_model.py get_projects query rows: \n\n')
            for row in cursor.fetchall():
                print(row)
                name, description, deadline = row
                rows.append('{} {:<25} ({})'.format(
                    name, description, deadline))
            # print(rows) # disable later
            return rows

def delete_project(fields, db_filename=db_filename_default):
    ''' 
    Delete one new project from the project table.
    
    Validate that the field value is a valid string without "%" or "?".
    In first sprint attempt without checking list of projects.
    
    7122
    '''
    print('\nmvc_model.py delete_project fields\n{}\n'.format(fields))
    try:
        project_name = fields['project_name']
        print ('\nmvc_model.py delete_project project: {}\n'.format(project_name))
    except KeyError:
        print ('\nmvc_model.py delete_project project_name field required')
        return 400
    
    with sqlite3.connect(db_filename) as conn:
        banned_chars = ('\'', '"', '\\', '//', '%', '?', '+', '-')
        cursor = conn.cursor()
        
        for char in banned_chars:
            if char in project_name:
                print ('\nmvc_model.py delete_project project_name banned character.\n') 
                return 400    
               
        if project_name.isalnum() or '_' in project_name  or ' ' in project_name: ## double check after the controller
            query = """
            DELETE FROM project
            WHERE name = '{}';
            """.format(project_name) 
        else:
            query = ""
    
        print ('\nmvc_model.py delete_project query: \n{}\n'.format(query))
        try:
            cursor.execute(query)
        except sqlite3.IntegrityError:
            print ('\nmvc_model.py add_project sqlite3 IntegrityError: Duplicate project name\n')
            return 'IntegrityError',
     
        if query:
            query = """
            select name, description, deadline
            from project 
            where name = '{}' 
            """.format(project_name)
    
            print ('\nmvc_model.py delete_project query project deleted: \n{}\n'.format(query))
            result = cursor.execute(query)
            row = result.fetchone()
            return row
def add_project(fields, db_filename=db_filename_default):
    ''' 
    Add a new project to the project table.
    
    Validate the fields and values before performing operations.
    
    '''
    print('\nmvc_model.py add_project fields\n{}\n'.format(fields))
    try:
        project_name = fields['project_name']
        description = fields['description']
        deadline = fields['deadline']      
        print ('\nmvc_model.py adding project: {}\n'.format(project_name, description, deadline))
    except KeyError:
        print ('\nmvc_model.py add_project Required field missing')
        return 400
    
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        if project_name.isalnum(): ## double check after the controller
            query = """
            insert into project (name, description, deadline)
            values ('{}', '{}', '{}');
            """.format(project_name, description, deadline) 
        else:
            query = ""
    
        print ('\nmvc_model.py add_project query: \n{}\n'.format(query))
        try:
            cursor.execute(query)
        except sqlite3.IntegrityError:
            print ('\nmvc_model.py add_project sqlite3 IntegrityError: Duplicate project name\n')
            return 'IntegrityError',
     
        if query:
            query = """
            select name, description, deadline
            from project 
            where name = '{}' 
            """.format(project_name)
    
            print ('\nmvc_model.py add_project query: \n{}\n'.format(query))
            result = cursor.execute(query)
            row = result.fetchone()
            return row

def test_add_project(db_filename=db_filename_default):
    ''' test adding a project 

        insert into project (name, description, deadline)
        values ('ciat', 'CIS280A',
                '2020-10-01');
    '''
    
    testing = True
     
    project_name = str(random.randint(1,10000))
    description = 'Test add project'
    deadline = datetime.strftime( datetime.now(), ISO_8601_DATE)
    #deadline = '2112-12-12'
    #deadline = '2112-12-12T12:12:12Z'
    
    #deadline = datetime.strftime( datetime.now(), ISO_8601_DATE)
    
    fields = { 'project_name': project_name, 'description': description, 'deadline': deadline }
    if testing:
        print ('\nmvc_model.py add_project fields: \n{}\n'.format(fields))
    return add_project(fields)
    
def test_get_tasks(task_id_value='%'):
    ''' Test getting tasks ''' 
    
    testing = True
        
    print ('\nmvc_model.py test_get_task results  with a task id of "{}":\n'.format(task_id_value))
    lines = get_tasks(task_id=task_id_value)
    if len(lines) > 0:
        for line in lines:
            print(line)
    else:
        print('\nmvc_model.py test_get_task no tasks with a task id of "{}"'.format(task_id_value))
    print()

def test_get_projects(project_name_value='%'):
    ''' Test getting projects ''' 
    
    testing = True
        
    lines = get_projects(project_name=project_name_value)
    if len(lines) > 0:
        print ('\nmvc_model.py test_get_projects named "{}"\n'.format(project_name_value))
        for line in lines:
            
            print(line)
    else:
        print ('\nmvc_model.py test_get_projects: no projects named "{}"\n'.format(project_name_value))
    print()
    
def test_delete_project():
    ''' Delete a sample project '''
    fields = {'project_name': 'pymotw'}
    delete_project(fields)

def test_all():
    ''' Perform all tests for this module. '''
    test_get_projects('pymotw')
    test_get_projects('ciat')
    test_get_tasks('1')
    test_get_tasks('15')
    test_get_tasks()   
    test_add_project()
    test_delete_project()
    test_get_projects()
    test_get_projects('%')
    test_get_projects('ciat')
        
if __name__ == '__main__':
    ''' Execute statements below if run directly, but not when module is imported '''
    if not exists_db(db_filename_default): 
        create_db()
    random.seed()
    test_all()



