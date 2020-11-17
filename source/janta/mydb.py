from collections import namedtuple
from django.db import connection


def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def execute_query(stmt, params):
    """"
    execute query and return this row  
    """
    with connection.cursor() as cursor:
        cursor.execute(stmt, params)
        row = namedtuplefetchall(cursor)
    return row


def execute_update(stmt, params):
    """"
    update query and return this row  
    """
    with connection.cursor() as cursor:
        return cursor.execute(stmt, params)


def create_schema():
    """"
    create Schema  
    """
    with connection.cursor() as cursor:
        print("\n\n########################################\n")
        print("Dropping projectjanta")
        cursor.execute("DROP DATABASE IF EXISTS projectjanta")
        print("Creating projectjanta")
        cursor.execute("CREATE DATABASE projectjanta")
        cursor.execute("USE projectjanta")
        print("Creating tables")
        for table_name in CREATE_TABLE:
            cursor.execute(CREATE_TABLE[table_name])
        print("Database Created Successfully")
        cursor.execute("INSERT INTO user VALUES ('admin', 'admin123', 'Admin', 'Admin name',"
                       " 'admin@iitb.ac.in', 'Male', 'working on lab project', '', '', NOW(), NOW());")
        print('\nAdmin handle: admin')
        print('Admin password: admin123\n')

    print("Now run Django command:> migrate sessions")


CREATE_TABLE = {
    'USER': 'CREATE TABLE user ('
            'handle varchar(45) not null unique ,'
            'password varchar (45) not null ,'
            'user_type varchar (45) not null ,'
            'name varchar (45) not null ,'
            'email_id varchar (45),'
            'gender varchar (45),'
            'about varchar (100),'
            'git_link varchar (100),'
            'linkedin_link varchar (100),'
            'last_login datetime,'
            'reg_time datetime,'
            'primary key(handle))',


    'TASK': 'CREATE TABLE task ('
            'task_id varchar(45) not null unique ,'
            'owner varchar(45) not null ,'
            'task_type varchar (45) not null ,'
            'description varchar (100) not null ,'
            'deadline datetime,'
            'creation_time datetime,'
            'primary key(task_id))',

    'USER_MODERATOR_MAP': 'CREATE TABLE user_moderator_map ('
                          'user varchar (45) not null ,'
                          'moderator varchar(45) not null ,'
                          'map_time datetime,'
                          'primary key(user, moderator))',

    'USER_TASK_MAP': 'CREATE TABLE user_task_map ('
                     'task_id varchar(45) not null ,'
                     'handle varchar (45) not null ,'
                     'completion_time datetime,'
                     'submission varchar(100) not null,'
                     'accepted int(10) not null ,'
                     'primary key(task_id, handle))',

    'MESSAGES': 'CREATE TABLE messages ('
                'id int(10) not null auto_increment,'
                'sender varchar (45) not null ,'
                'receiver varchar (45) not null ,'
                'text varchar(200) not null ,'
                'msg_time datetime,'
                'primary key(id))',

    'NOTIFICATIONS': 'CREATE TABLE notifications ('
                     'id int(10) not null auto_increment,'
                     'handle varchar (45) not null ,'
                     'noti_type varchar (45) not null ,'
                     'text varchar(200) not null ,'
                     'noti_time datetime,'
                     'marked int(10) not null, '
                     'primary key(id))',

}

