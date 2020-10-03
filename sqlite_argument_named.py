#!bin/python3

# sqlite3_argument_named.py
import sqlite3
import sys

#db_filename = 'todo.db'
#project_name = sys.argv[1]

def get_project_id(db_filename='todo.db', project_id='1'):

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        query = """
        select id, priority, details, status, deadline from task
        where project = :project_name
        order by deadline, priority
        """

        cursor.execute(query, {'project_name': project_name})

        rows = []
        for row in cursor.fetchall():
            task_id, priority, details, status, deadline = row
            rows.append('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
                task_id, priority, details, status, deadline))
        # print(rows) # disable later
        return rows

def get_project_name(db_filename='todo.db', project_name='pymotw'):

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()

        query = """
        select id, priority, details, status, deadline from task
        where project = :project_name
        order by deadline, priority
        """

        cursor.execute(query, {'project_name': project_name})

        rows = []
        for row in cursor.fetchall():
            task_id, priority, details, status, deadline = row
            rows.append('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
                task_id, priority, details, status, deadline))
        # print(rows) # disable later
        return rows

def project_name_test(project_name_value):
    lines = get_project_name(project_name=project_name_value)
    for line in lines:
       print(line)
    else:
       print('no projects named "{}"'.format(project_name_value)
 
if __name__=='__main__':
    project_name_test('pymotw')
    project_name_test('ciat')
