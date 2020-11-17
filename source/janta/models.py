from django.db import models
from django.db import connection
import os
from janta import mydb

# Create your models here.

# the following lines added:
from datetime import date

# first datetime is module name second one is class
from datetime import datetime
from django.utils import timezone


def reset_db():
    mydb.create_schema()

# ##############################  User ##############################################
class User:  
    """ 
    this class for User Attributes:
        :user_handle: user's handle
        :user_type: user's type
        :user_name: user's name
        :user_email: eamil address
        :user_gender: gender
        :user_about:  user profile
   
    """
    # DO NOT CHANGE THE FIELD'S NAME
    def __init__(self):
        self.user_handle = None
        self.user_type = None
        self.user_name = None
        self.user_email = None
        self.user_gender = None
        self.user_about = None
        self.git_link = None
        self.linkedin_link = None
        self.last_login = None
        self.reg_time = None
    ##############################

    def set_user(self, row):
        self.user_handle = row.handle
        self.user_type = row.user_type
        self.user_name = row.name
        self.user_email = row.email_id
        self.user_gender = row.gender
        self.user_about = row.about
        self.git_link = row.git_link
        self.linkedin_link = row.linkedin_link
        self.last_login = row.last_login
        self.reg_time = row.reg_time


def validate_credentials(handle, password):
    """ validate Credentials"""
    stmt = "SELECT * FROM user WHERE handle=%s and password=%s"
    params = (handle, password)
    row = mydb.execute_query(stmt, params)
    if len(row) == 1:
        stmt = "UPDATE user SET last_login=NOW() WHERE handle=%s"
        params = handle
        mydb.execute_update(stmt, params)
        return True
    return False


def user_register(handle, password, user_type, name, emailid, gender):
    """ User Register"""
    stmt = 'INSERT INTO user (handle, password, user_type, name, email_id, gender, last_login, reg_time)' \
           'values(%s, %s, %s, %s, %s, %s, NOW(), NOW())'
    params = (handle, password, user_type, name, emailid, gender)
    mydb.execute_update(stmt, params)


def profile_edit(handle, name, emailid, gender, about, git_link, linkedin_link):
    """ Edit Profile"""
    stmt = 'UPDATE user SET name=%s, email_id=%s, gender=%s, about=%s, git_link=%s, linkedin_link=%s WHERE handle=%s'
    params = (name, emailid, gender, about, git_link, linkedin_link, handle)
    mydb.execute_update(stmt, params)


def change_password(handle, old_password, new_password):
    """ change password"""
    stmt = 'SELECT * FROM user WHERE handle=%s AND password=%s'
    params = (handle, old_password)
    row = mydb.execute_query(stmt, params)
    if len(row) == 0:
        return False
    stmt = 'UPDATE user SET password=%s WHERE handle=%s AND password=%s'
    params = (new_password, handle, old_password)
    mydb.execute_update(stmt, params)
    return True


def get_user(handle):
    """ get user"""
    stmt = "SELECT * FROM user WHERE handle=%s"
    params = handle
    row = mydb.execute_query(stmt, params)
    if len(row) == 0:
        return None
    user = User()
    user.set_user(row[0])
    return user


def get_user_by_type(handle, user_type):
    """ get user by type"""
    stmt = "SELECT * FROM user WHERE handle=%s and user_type=%s"
    params = (handle, user_type)
    row = mydb.execute_query(stmt, params)
    if len(row) == 0:
        return None
    user = User()
    user.set_user(row[0])
    return user

# ##############################  Task #################################################
class Task:  
    """
    this class for task Attributes: 
        :task_id: task id
        :owner: task owner
        :task_type: task type
        :description: task description
        :deadline: task deadline
        :creation_time: time of task creation

    """
    def __init__(self):
        self.task_id = None
        self.owner = None
        self.task_type = None
        self.description = None
        self.deadline = None
        self.creation_time = None

    def set_task(self, row):
        self.task_id = row.task_id
        self.owner = row.owner
        self.task_type = row.task_type
        self.description = row.description
        self.deadline = row.deadline
        self.creation_time = row.creation_time


def get_task(task_id):
    """ get task"""
    stmt = "SELECT * FROM task WHERE task_id=%s"
    params = task_id
    row = mydb.execute_query(stmt, params)
    if len(row) == 0:
        return None
    task = Task()
    task.set_task(row[0])
    return task


def get_my_tasks(owner, recent=False):
    """ get my task"""
    stmt = "SELECT * FROM task WHERE owner=%s"
    if recent:
        stmt = "SELECT * FROM task WHERE owner=%s ORDER BY creation_time DESC LIMIT 5"
    params = owner
    rows = mydb.execute_query(stmt, params)

    tasks = []
    for row in rows:
        task = Task()
        task.set_task(row)
        tasks.append(task)
    return tasks


def insert_task(task_id, owner, description, task_type, deadline):
    """ insert task"""
    deadline_datetime = datetime.combine(deadline, datetime.min.time())
    # now = datetime.now()
    # formatted_now = now.strftime('%Y-%m-%d %H:%M:%S')
    formatted_deadline = deadline_datetime.strftime('%Y-%m-%d %H:%M:%S')
    stmt = "INSERT INTO task (task_id, owner, task_type, description, deadline, creation_time)" \
           "values(%s, %s, %s, %s, %s, NOW())"
    params = (task_id, owner, task_type, description, formatted_deadline)
    mydb.execute_update(stmt, params)

    # send notification to all mapped user
    noti_type = "Task Created"
    text = "Task Id:"+task_id+" has been created by moderator:"+owner
    notify_mapped_users(moderator=owner, noti_type=noti_type, text=text)


# send notifications to all users who submitted the task.
def modify_task(task_id, owner, description, task_type, deadline):
    """ modify task"""
    task = get_task(task_id)
    deadline_datetime = datetime.combine(deadline, datetime.min.time())
    formatted_deadline = deadline_datetime.strftime('%Y-%m-%d %H:%M:%S')
    stmt = "UPDATE task SET task_type=%s, description=%s, deadline=%s WHERE task_id=%s"
    params = (task_type, description, formatted_deadline, task_id)
    mydb.execute_update(stmt, params)

    if task.task_type != task_type or task.description != description:
        stmt = "DELETE FROM user_task_map WHERE task_id=%s"
        params = task_id
        mydb.execute_update(stmt, params)

    # send notification to all mapped user
    noti_type = "Task Modified"
    text = "Task Id:"+task_id+" has been modified by moderator:"+owner
    notify_mapped_users(moderator=owner, noti_type=noti_type, text=text)


def delete_task(task_id):
    """ delete task"""
    task = get_task(task_id)
    stmt = "DELETE FROM task WHERE task_id=%s"
    params = task_id
    mydb.execute_update(stmt, params)

    # delete files
    if task.task_type == "Upload":
        path = "janta/static/uploaded-files/"
        stmt = "SELECT * FROM user_task_map WHERE task_id=%s"
        params = task_id
        rows = mydb.execute_query(stmt, params)
        for row in rows:
            path += row.submission
            if os.path.exists(path):
                os.remove(path)

    stmt = "DELETE FROM user_task_map WHERE task_id=%s"
    params = task_id
    mydb.execute_update(stmt, params)

    # send notification to all mapped user
    noti_type = "Task Deleted"
    text = "Task Id:"+task_id+" has been deleted by moderator:"+task.owner
    notify_mapped_users(moderator=task.owner, noti_type=noti_type, text=text)


def notify_mapped_users(moderator, noti_type, text):
    """send notification to all mapped user"""
    stmt = "SELECT user FROM user_moderator_map WHERE moderator=%s"
    params = moderator
    rows = mydb.execute_query(stmt, params)
    for row in rows:
        sent_notification(handle=row.user, noti_type=noti_type, text=text)


#  for user
def get_ongoing_tasks(handle):
    """ get ongoing tasks"""
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    formatted_datetime = today_datetime.strftime('%Y-%m-%d %H:%M:%S')
    stmt = "SELECT * FROM task WHERE deadline >= %s AND owner IN (SELECT moderator FROM user_moderator_map WHERE user=%s)" \
           " AND task_id NOT IN (SELECT task_id FROM user_task_map WHERE handle=%s) ORDER BY deadline ASC"
    params = (formatted_datetime, handle, handle)
    rows = mydb.execute_query(stmt, params)

    ongoing_tasks = []
    for row in rows:
        task = Task()
        task.set_task(row)
        ongoing_tasks.append(task)

    return ongoing_tasks


# for user not submitted (overdue) tasks
def get_overdue_tasks(handle):
    """ get overdue tasks"""
    stmt = "SELECT * FROM task WHERE deadline < CURDATE() AND owner IN (SELECT moderator FROM user_moderator_map WHERE user=%s)" \
           " AND task_id NOT IN (SELECT task_id FROM user_task_map WHERE handle=%s) ORDER BY deadline DESC"
    params = (handle, handle)
    rows = mydb.execute_query(stmt, params)

    overdue_tasks = []
    for row in rows:
        task = Task()
        task.set_task(row)
        overdue_tasks.append(task)

    return overdue_tasks


# for user home page
def get_recent_ongoing_tasks(handle):
    """ get recent ongoing tasks"""
    today = date.today()
    today_datetime = datetime.combine(today, datetime.min.time())
    formatted_datetime = today_datetime.strftime('%Y-%m-%d %H:%M:%S')
    stmt = "SELECT * FROM task WHERE deadline >= %s AND owner IN (SELECT moderator FROM user_moderator_map WHERE user=%s)" \
           " AND task_id NOT IN (SELECT task_id FROM user_task_map WHERE handle=%s) ORDER BY deadline DESC LIMIT 5"
    params = (formatted_datetime, handle, handle)
    rows = mydb.execute_query(stmt, params)

    recent_ongoing_tasks = []
    for row in rows:
        task = Task()
        task.set_task(row)
        recent_ongoing_tasks.append(task)

    return recent_ongoing_tasks


def get_submitted_tasks(handle):
    """ get submitted tasks """
    stmt = "SELECT task.task_id AS task_id, task.owner AS owner, task.description AS description,task.creation_time AS creation_time," \
           " task.task_type AS task_type, task.deadline AS deadline, user_task_map.completion_time AS completion_time" \
           " FROM task INNER JOIN user_task_map ON task.task_id = user_task_map.task_id WHERE user_task_map.handle=%s" \
           " ORDER BY completion_time DESC"
    params = handle
    rows = mydb.execute_query(stmt, params)

    submitted_tasks = []
    for row in rows:
        task = Task()
        task.set_task(row)
        submitted_tasks.append(task)

    return submitted_tasks


class UserModeratorMap:  # ##############################  User Moderator Map ##############################################################################

    """
    this class for User to Moderator Map Attributes:
        :user:user
        :moderator: moderator
        :map_time: Mapping time

    """
    def __init__(self):
        self.user = None
        self.moderator = None
        self.map_time = None

    def set_user_moderator(self, row):
        self.user = row.user
        self.moderator = row.moderator
        self.map_time = row.map_time


def add_users(moderator, user_handles):
    """ add user"""
    count = 0
    invalid_handles = []
    stmt = "INSERT INTO user_moderator_map (user, moderator, map_time)" \
           "values (%s, %s, NOW())"
    for handle in user_handles:
        params = (handle, moderator)
        mydb.execute_update(stmt, params)
        count += 1

    return "Add count: "+str(count)


def get_added_user(user, moderator):
    """ get added user"""
    stmt = "SELECT * FROM user_moderator_map WHERE user=%s and moderator=%s"
    params = (user, moderator)
    row = mydb.execute_query(stmt, params)
    if len(row) == 0:
        return None
    added_user = UserModeratorMap()
    added_user.set_user_moderator(row[0])
    return added_user


def remove_user(user, moderator):
    """ remove user"""
    stmt = "DELETE FROM user_moderator_map WHERE user=%s and moderator=%s"
    params = (user, moderator)
    mydb.execute_update(stmt, params)
    stmt = "DELETE FROM user_task_map WHERE handle=%s and task_id IN (SELECT task_id FROM task WHERE owner=%s)"
    params = (user, moderator)
    mydb.execute_update(stmt, params)


# ##########################################################################################################################################################
class UserTaskMap:
    """
    this class for User to Task Map
    Attributes:
        :task_id: task id
        :handle: handle which complete the task
        :completion_time: task completion time
        :submission:task submited or not 
        :accepted: task accepted or not
 
    """
    def __init__(self):
        self.task_id = None
        self.handle = None
        self.completion_time = None
        self.submission = None
        self.accepted = None

    def set_user_task_map(self, row):
        self.task_id = row.task_id
        self.handle = row.handle
        self.completion_time = row.completion_time
        self.submission = row.submission
        self.accepted = row.accepted


def get_user_task_map(task_id, handle):
    """ get user task """
    stmt = "SELECT * FROM user_task_map WHERE task_id=%s AND handle=%s"
    params = (task_id, handle)
    row = mydb.execute_query(stmt, params)
    if len(row) == 0:
        return None
    obj = UserTaskMap()
    obj.set_user_task_map(row[0])
    return obj


def accept_submission(task_id, handle):
    """ accept submission"""
    stmt = "UPDATE user_task_map SET accepted=1 WHERE task_id=%s AND handle=%s"
    params = (task_id, handle)
    mydb.execute_update(stmt, params)

    noti_type = "Submission Accepted"
    text = "Your submission for task id:"+task_id+" has been accepted."
    sent_notification(handle=handle, noti_type=noti_type, text=text)


def reject_submission(task_id, handle):
    """ reject submission """
    task = get_task(task_id)
    user_task_map = get_user_task_map(task_id=task_id, handle=handle)

    stmt = "DELETE FROM user_task_map WHERE task_id=%s AND handle=%s"
    params = (task_id, handle)
    mydb.execute_update(stmt, params)

    # delete file
    if task is not None and task.task_type == "Upload":
        path = "janta/static/uploaded-files/" + user_task_map.submission
        if os.path.exists(path):
            os.remove(path)

    noti_type = "Submission Rejected"
    text = "Your submission for task id:"+task_id+" has been rejected."
    sent_notification(handle=handle, noti_type=noti_type, text=text)


# if same concurrent request comes to insert it will throw error eg. clicking two times.
def submit_task(task_id, handle, submission):
    """ submit task"""
    stmt = "INSERT INTO user_task_map (task_id, handle, completion_time, submission, accepted)" \
           "VALUES (%s, %s, NOW(), %s, 0)"
    params = (task_id, handle, submission)
    mydb.execute_update(stmt, params)


def get_submission_status(task_id, moderator):
    """ get submission status"""
    submission_status = {'Accepted': [], 'Submitted': [], 'Legends': []}
    stmt = "SELECT * FROM user_task_map WHERE task_id=%s"
    params = task_id
    rows = mydb.execute_query(stmt, params)
    for row in rows:
        if row.accepted == 1:
            submission_status['Accepted'].append(row.handle)
        else:
            submission_status['Submitted'].append(row.handle)

    stmt = "SELECT * FROM user_moderator_map WHERE moderator=%s AND user NOT IN " \
           "(SELECT handle FROM user_task_map WHERE task_id=%s)"
    params = (moderator, task_id)
    rows = mydb.execute_query(stmt, params)
    for row in rows:
        submission_status['Legends'].append(row.user)

    return submission_status


def get_not_accepted_submissions(task_id):
    """ get not accepted submissions"""
    stmt = "SELECT * FROM user_task_map WHERE task_id=%s AND accepted=0"
    params = task_id
    rows = mydb.execute_query(stmt, params)
    submissions = []
    for row in rows:
        obj = UserTaskMap()
        obj.set_user_task_map(row)
        submissions.append(obj)

    return submissions


# ########################################## Message ###########################################################################################
class Messages:
    """
    this class for Message
    Attributes:
        :id: message id
        :sender: message sender
        :receiver: message receiver
        :text: text of message
        :msg_time: time of message 

    """
    def __init__(self):
        self.id = None
        self.sender = None
        self.receiver = None
        self.text = None
        self.msg_time = None

    def set_message(self, row):
        self.id = row.id
        self.sender = row.sender
        self.receiver = row.receiver
        self.text = row.text
        self.msg_time = row.msg_time


def get_messages(handle):
    """ get message"""
    stmt = "SELECT * FROM messages WHERE sender=%s OR receiver=%s ORDER BY msg_time DESC"
    params = (handle, handle)
    rows = mydb.execute_query(stmt, params)
    messages = []
    for row in rows:
        obj = Messages()
        obj.set_message(row)
        messages.append(obj)

    return messages


def send_message(sender, receiver, text):
    """ send message"""
    stmt = "INSERT INTO messages (sender, receiver, text, msg_time)" \
           "VALUES (%s, %s, %s, NOW())"
    params = (sender, receiver, text)
    mydb.execute_update(stmt, params)

    noti_type = "New Message"
    text = sender+" sent a message."
    sent_notification(handle=receiver, noti_type=noti_type, text=text)


def delete_message(msg_id, handle):
    """ delete message"""
    stmt = "DELETE FROM messages WHERE (sender=%s OR receiver=%s) AND id=%s"
    params = (handle, handle, msg_id)
    mydb.execute_update(stmt, params)


# ######################################## NOTIFICATIONS ################################################################################################
class Notification:
    """
    this class for get  notifications

    """
   
    def __init__(self):
        self.id = None
        self.handle = None
        self.noti_type = None
        self.text = None
        self.noti_time = None
        self.marked = None

    def set_notification(self, row):
        self.id = row.id
        self.handle = row.handle
        self.noti_type = row.noti_type
        self.text = row.text
        self.noti_time = row.noti_time
        self.marked = row.marked


def sent_notification(handle, noti_type, text):
    """ send notification """
    stmt = "INSERT INTO notifications (handle, noti_type, text, noti_time, marked)" \
           "VALUES (%s, %s, %s, NOW(), 0)"
    params = (handle, noti_type, text)
    mydb.execute_update(stmt, params)


def get_notifications(handle):
    """ get unread notifications """
    stmt = "SELECT COUNT(*) AS unread_count FROM notifications WHERE handle=%s AND marked=0"
    params = handle
    rows = mydb.execute_query(stmt, params)
    unread_count = rows[0].unread_count

    # get 10 notifications
    stmt = "SELECT * FROM notifications WHERE handle=%s ORDER BY marked ASC, noti_time DESC LIMIT 10"
    params = handle
    rows = mydb.execute_query(stmt, params)
    notifications = []
    for row in rows:
        obj = Notification()
        obj.set_notification(row)
        obj.noti_time = obj.noti_time.strftime("%d-%b-%Y at %H:%M")
        notifications.append(obj)

    return unread_count, notifications


def mark_as_read(noti_id, handle):
    """ update the notifications mark as read"""
    stmt = "UPDATE notifications SET marked=1 WHERE id=%s"
    params = noti_id
    mydb.execute_update(stmt, params)

    # delete read notification more than 10
    stmt = "DELETE FROM notifications WHERE marked=1 AND handle=%s AND id NOT IN (SELECT id FROM " \
           "(SELECT id FROM notifications WHERE handle=%s AND marked=1 ORDER BY noti_time DESC LIMIT 10) foo)"
    params = (handle, handle)
    mydb.execute_update(stmt, params)


# ################################################# ADMIN #################################################################################################
def admin_del_user(handle):
    """ delete user"""
    stmt = "DELETE FROM user WHERE handle=%s"
    params = handle
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM user_task_map WHERE handle=%s"
    params = handle
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM user_moderator_map WHERE user=%s"
    params = handle
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM messages WHERE sender=%s or receiver=%s"
    params = (handle, handle)
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM notifications WHERE handle=%s"
    params = handle
    mydb.execute_update(stmt, params)


def admin_del_moderator(handle):
    """ delete Moderator """
    stmt = "DELETE FROM user WHERE handle=%s"
    params = handle
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM user_moderator_map WHERE moderator=%s"
    params = handle
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM task WHERE owner=%s"
    params = handle
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM messages WHERE sender=%s or receiver=%s"
    params = (handle, handle)
    mydb.execute_update(stmt, params)

    stmt = "DELETE FROM notifications WHERE handle=%s"
    params = handle
    mydb.execute_update(stmt, params)


def admin_del_task(task_id):
    """ delete task for task_id"""
    stmt = "DELETE FROM task WHERE task_id=%s"
    params = task_id
    mydb.execute_update(stmt, params)
    stmt = "DELETE FROM user_task_map WHERE task_id=%s"
    params = task_id
    mydb.execute_update(stmt, params)


def admin_get_usr_modr_list():
    """ return User Moderator list"""
    stmt = "SELECT * FROM user WHERE user_type=%s OR user_type=%s ORDER BY reg_time DESC"
    params = ("User", "Moderator")
    rows = mydb.execute_query(stmt, params)
    usr_mdrs = []
    for row in rows:
        obj = User()
        obj.set_user(row)
        usr_mdrs.append(obj)
    return usr_mdrs


def admin_get_task_list():
    """ return Task List """
    stmt = "SELECT * FROM task ORDER BY creation_time DESC"
    params = None
    rows = mydb.execute_query(stmt, params)
    tasks_list = []
    for row in rows:
        obj = Task()
        obj.set_task(row)
        tasks_list.append(obj)
    return tasks_list


