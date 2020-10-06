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
# sqlite3_argument_named.py
import random
import sqlite3
import sys
import mvc_model_create

db_filename='todo.db'

def get_tasks(db_filename='todo.db', task_id='%'):

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

def get_projects(db_filename='todo.db', project_name='%'):

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

def add_project(fields):
    ''' Add a new project
    '''
    
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        if project_name.isalnum():
            query = """
            insert into project (name, description, deadline)
            values ('{}', '{}', '{}');
            """.format(project_name, description, deadline) 
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
            cursor.execute(query)
            row = cursor.fetchall()
            print (row)
            return row

def test_add_project():
    ''' test adding a project 

        insert into project (name, description, deadline)
        values ('ciat', 'CIS280A',
                '2020-10-01');
    '''
     
    project_name = str(random.randint(1,10000))
    description = 'Test add project'
    deadline = '2020-10-31'
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        if project_name.isalnum:
            query = """
            insert into project (name, description, deadline)
            values ('{}', '{}', '{}');
            """.format(project_name, description, deadline) 
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
            cursor.execute(query)
            row = cursor.fetchall()
            print (row)
            return row

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
    test_get_projects()
    test_get_tasks('1')
    test_get_tasks('15')
    test_get_tasks()   
    test_add_project()
        
if __name__ == '__main__':
    random.seed()
    test_all()

