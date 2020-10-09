-- todo_schema.sql
-- Schema for to-do application examples.

-- Projects are high-level activities made up of tasks
create table project (
    name        text primary key,
    description text,
    deadline    date
);

-- Tasks are steps that can be taken to complete a project
create table task (
    id           integer primary key autoincrement not null,
    priority     integer default 1,
    details      text,
    status       text,
    deadline     date,
    completed_on date,
    project      text not null references project(name)
);

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
