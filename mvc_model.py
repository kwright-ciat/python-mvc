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
import os
import random
import sqlite3
import sys

db_filename_default='todo.db'
schema_filename = 'todo_schema.sql'

def exists_db(db_filename=db_filename_default):
    db_exists = os.path.exists(db_filename)
    return db_exists
    
def create_db(db_filename=db_filename_default):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        if exists_db():
            print('Creating schema')
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            cursor.executescript(schema)
    
            print('Inserting initial data')
    
            conn.executescript("""
            insert into project (name, description, deadline)
            values ('pymotw', 'Python Module of the Week',
                    '2016-11-01');
    
            insert into project (name, description, deadline)
            values ('ciat', 'CIS280A Cisco DevNet',
                    '2020-10-01');
    
            insert into task (details, status, deadline, project)
            values ('Create python-mvc Git Repository', 'done', '2020-10-02',
                    'ciat');
    
            insert into task (details, status, deadline, project)
            values ('Get basic /project and /task API endpoints working', 'wip', '2020-10-03',
                    'ciat');
    
     
            insert into task (details, status, deadline, project)
            values ('write about select', 'done', '2016-04-25',
                    'pymotw');
    
            insert into task (details, status, deadline, project)
            values ('write about random', 'waiting', '2016-08-22',
                    'pymotw');
    
            insert into task (details, status, deadline, project)
            values ('write about sqlite3', 'active', '2017-07-31',
                    'pymotw');
            """)
        else:
            print('Database exists, assume schema does, too.')
        
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
            print(query)
            cursor.execute(query)
    
            rows = []
            for row in cursor.fetchall():
                task_id, priority, details, status, deadline = row
                rows.append('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
                    task_id, priority, details, status, deadline))
            # print(rows) # disable later
            return rows

def get_projects(db_filename=db_filename_default, project_name='%'):

        with sqlite3.connect(db_filename) as conn:
            cursor = conn.cursor()
            if project_name == '%':
                query = """
                select name, description, deadline
                from project
                order by name
                """
            else:
                query = """
                select name, description, deadline
                from project where name = "{}"
                """.format(project_name)
        
            print (query)
            cursor.execute(query)
        
            rows = []
        
            for row in cursor.fetchall():
                print(row)
                name, description, deadline = row
                rows.append('{} {:<25} ({})'.format(
                    name, description, deadline))
            # print(rows) # disable later
            return rows

def add_project(fields, db_filename=db_filename_default):
    ''' 
    Add a new project to the project table.
    
    Validate the fields and values before performing operations.
    
    '''
    print('add_project fields', fields)
    try:
        project_name = fields['project_name']
        description = fields['description']
        deadline = fields['deadline']
    except KeyError:
        print ('add_project Required field missing')
        return 400
    
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        if project_name.isalnum(): ## double check after the controller
            query = """
            insert into project (name, description, deadline)
            values ('{}', '{}', '{}');
            """.format(fields['project_name'], 
                fields['description'], fields['deadline']) 
        else:
            query = ""
    
        print (query)
        cursor.execute(query)
     
        if query:
            query = """
            select name, description, deadline
            from project 
            where name = '{}' 
            """.format(project_name)
    
            print (query)
            result = cursor.execute(query)
            print (result)
            return result

def test_add_project(db_filename=db_filename_default):
    ''' test adding a project 

        insert into project (name, description, deadline)
        values ('ciat', 'CIS280A',
                '2020-10-01');
    '''
     
    project_name = str(random.randint(1,10000))
    description = 'Test add project'
    deadline = '2020-10-31'
    
    fields = { 'project_name': project_name, 'description': description, 'deadline': deadline }
    print (fields)
    add_project(fields)
    
def test_get_tasks(task_id_value='%'):
    lines = get_tasks(task_id=task_id_value)
    if len(lines) > 0:
        for line in lines:
            print(line)
    else:
        print('no tasks with a task id of "{}"'.format(task_id_value))
    print()

def test_get_projects(project_name_value='pymotw'):
    lines = get_projects(project_name=project_name_value)
    if len(lines) > 0:
        for line in lines:
            print(line)
    else:
        print('no projects named "{}"'.format(project_name_value))
    print()

def test_all():
    test_get_projects('pymotw')
    test_get_projects('ciat')
    test_get_tasks('1')
    test_get_tasks('15')
    test_get_tasks()   
    test_add_project(db_filename_default)
    test_get_projects()
        
if __name__ == '__main__':
    if not exists_db(db_filename_default): create_db()
    random.seed()
    test_all()

