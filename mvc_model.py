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
import sqlite3
import sys
import mvc_model_create

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

def get_tasks_test(task_id_value='%'):
    lines = get_tasks(task_id=task_id_value)
    if len(lines) > 0:
        for line in lines:
            print(line)
    else:
        print('no tasks with a task id of "{}"'.format(task_id_value))
    print()

def get_projects_test(project_name_value='pymotw'):
    lines = get_projects(project_name=project_name_value)
    if len(lines) > 0:
        for line in lines:
            print(line)
    else:
        print('no projects named "{}"'.format(project_name_value))
    print()

def run_all_test():
    get_projects_test('pymotw')
    get_projects_test('ciat')
    get_projects_test()
    get_tasks_test('1')
    get_tasks_test('15')
    get_tasks_test()   
    
    
if __name__ == '__main__':
    run_all_test()
