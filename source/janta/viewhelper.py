from janta import models
from datetime import datetime
from datetime import date
import re
import json


def set_session(request, user):
    """
    This function set the session for user.
        
    :type request: http request
    :param request: the request sent for the session
    :param user: user details
    :return: redirecting to the page according to http request
    """
    
    request.session["handle"] = user.user_handle
    request.session["user_type"] = user.user_type
    request.session["user_name"] = user.user_name
    request.session["user_email"] = user.user_email
    request.session["user_gender"] = user.user_gender


def validate_login(handle, password):
    """
    This function validate the login Details.
        
    :param handle: handle of user
    :param password: user password
    :return:
    :status: status 
    :message: message 
    """

    status = True
    message = None
    if not is_handle(handle):
        status = False
        message = "Invalid Handle"
        return status, message
    if not is_password(password):
        status = False
        message = "Invalid Password"
        return status, message
    if not models.validate_credentials(handle, password):
        status = False
        message = "Account does not exist"
        return status, message
    return status, message


def validate_registration(form_data):
    """
    This function validate the registration details.
        
    :param form_data: user details
    :return:
        :status: status 
        :message: message 
    """
    message = "! Form validation error submit again"
    status = True
    name = form_data.get("name")
    handle = form_data.get("handle")
    password = form_data.get("password")
    conf_pass = form_data.get("conf_pass")
    emailid = form_data.get("email")
    user_type = form_data.get("user_type")
    gender = form_data.get("gender")

    if not is_name(name):
        status = False
        message = "Invalid Name"
        return status, message
    if not is_handle(handle):
        status = False
        message = "Invalid Handle"
        return status, message
    if not is_password(password):
        status = False
        message = "Invalid Password"
        return status, message
    if password != conf_pass:
        status = False
        message = "Password and Confirm Password do not match"
        return status, message
    if not is_email(emailid):
        status = False
        message = "Invalid Email Id"
        return status, message
    if not is_user_type(user_type):
        status = False
        message = "Invalid Account Type"
        return status, message
    if not is_gender(gender):
        status = False
        message = "Invalid Gender"
        return status, message
    if models.get_user(handle) is not None:
        status = False
        message = "Handle already exists"
        return status, message
    return status, message


def validate_profile_edit(form_data):
    """
    This function validate the profile_edit details.
        
    :param form_data: user details
    :return:
        :status: status 
        :message: message 
    """
    message = "! Form validation error submit again"
    status = True
    name = form_data.get("name")
    gender = form_data.get("gender")
    emailid = form_data.get("email")

    if not is_name(name):
        status = False
        message = "Invalid Name"
        return status, message
    if not is_email(emailid):
        status = False
        message = "Invalid Email Id"
        return status, message
    if not is_gender(gender):
        status = False
        message = "Invalid Gender"
        return status, message
    return status, message


def validate_change_password(form_data):
    """
    This function validate the change_password details.
        
    :param form_data: user details
    :return:
        :status: status 
        :message: message
    """
    message = "! Form validation error submit again"
    status = True
    old_password = form_data.get("old_password")
    new_password = form_data.get("new_password")
    conf_pass = form_data.get("conf_pass")

    if not is_password(old_password):
        status = False
        message = "Invalid old password"
        return status, message
    if not is_password(new_password):
        status = False
        message = "Invalid new password"
        return status, message
    if new_password != conf_pass:
        status = False
        message = "Password and Confirm Password do not match"
        return status, message
    return status, message


def validate_create_task(form_data):
    """
    This function validate the create_task details.
        
    :param form_data: task details
    :return:
        :status: status 
        :message: message
        
    """

    message = None
    status = True
    # test if task_id already exist
    task_id = form_data.get("task_id")
    description = form_data.get("description")
    task_type = form_data.get("task_type")
    deadline = form_data.get("deadline")

    if not is_task_id(task_id):
        status = False
        message = "Invalid Task Id"
        return status, message
    if not is_description(description):
        status = False
        message = "Invalid Task Id"
        return status, message
    if not is_task_type(task_type):
        status = False
        message = "Invalid task type"
        return status, message
    if deadline < date.today():
        status = False
        message = "Invalid past deadline"
        return status, message

    if models.get_task(task_id) is not None:
        status = False
        message = "Task Id already exists try another"
        return status, message
    return status, message


def validate_modify_task(form_data):
    """
    This function validate the modify_task details.
        
    :param form_data: task details
    :return:
    :status: status 
    :message: message
        
    """

    message = None
    status = True
    task_id = form_data.get("task_id")
    description = form_data.get("description")
    task_type = form_data.get("task_type")
    deadline = form_data.get("deadline")

    if not is_task_id(task_id):
        status = False
        message = "Invalid Task Id"
        return status, message
    if not is_description(description):
        status = False
        message = "Invalid Task Id"
        return status, message
    if not is_task_type(task_type):
        status = False
        message = "Invalid task type"
        return status, message
    if deadline < date.today():
        status = False
        message = "Invalid past deadline"
        return status, message

    if models.get_task(task_id) is None:
        status = False
        message = "Task Id does not exists"
        return status, message
    return status, message


def validate_add_user(form_data, moderator):
    """
    This function validate the add_user details.
        
    :param form_data: detail of the  user's  which are adding in this moderator
    :param moderator: moderator details
    :return:
        :status: status 
        :message: message
        :handle_list: list of handle which are adding

    """

    message = None
    status = True
    handle_list = []

    handles = form_data.get("user_handles")
    regex = form_data.get("regex")
    if regex is None or len(regex) == 0:
        regex = "[;, ]"
    if handles is None or len(handles) == 0:
        status = False
        message = "Invalid Handles"
        return status, message, handle_list

    handle_list = set(x.strip() for x in re.compile(regex).split(handles))
    handle_list = set(x for x in handle_list if is_handle(x))

    if len(handle_list) == 0:
        status = False
        message = "Invalid Handles"
        return status, message, handle_list

    invalid_handles = []
    added_handles = []
    for handle in handle_list:
        if models.get_user_by_type(handle=handle, user_type="User") is not None:
            if models.get_added_user(handle, moderator) is not None:
                added_handles.append(handle)
        else:
            invalid_handles.append(handle)

    if len(invalid_handles) > 0:
        status = False
        message = "Invalid Handles: ["+(", ".join(invalid_handles))+"]"
        return status, message, handle_list

    handle_list = list(set(handle_list) - set(added_handles))
    if len(handle_list) == 0:
        status = False
        message = "Invalid Handles"
        return status, message, handle_list

    return status, message, handle_list


def validate_remove_user(form_data, moderator):
    """
    This function validate the remove_user details.
        
    :param form_data: detail of the  user  which are removeing in this moderator
    :param moderator: moderator details
    :return:
        :status: status 
        :message: message
        :userhandle: handle of user
    """


    status = True
    message = None
    user_handle = form_data.get("user_handle")
    if not is_handle(user_handle):
        status = False
        message = "Invalid Handle"
        return status, message, user_handle
    if models.get_added_user(user=user_handle, moderator=moderator) is None:
        status = False
        message = "Handle was not added by you"
        return status, message, user_handle
    return status, message, user_handle


def validate_delete_task(moderator, form_data):
    """
    This function validate the delete_task details.
        
    :param form_data: detail of task
    :param moderator: moderator details
    :return:
        :status: status
        :message: message
    """

    status = True
    message = None
    task_id = form_data.get("task_id")
    if not is_task_id(task_id):
        status = False
        message = "Invalid Task Id"
        return status, message
    task = models.get_task(task_id)
    if task is None:
        status = False
        message = "Task Id does not exist"
        return status, message
    if task.owner != moderator:
        status = False
        message = "You are NOT owner of Task Id:"+task_id
        return status, message
    return status, message


def save_file(file, handle, task_id):
    """
    This function save the file.
        
    :param file: detail of the file
    :param handle: handle of user
    :param task_id: task id 
    :return: return the filename
    """

    filename = handle+task_id+file.name
    path = "janta/static/uploaded-files/"+filename
    dest = open(path, 'wb')
    if file.multiple_chunks:
        for c in file.chunks():
            dest.write(c)
    else:
        dest.write(file.read())
    dest.close()
    return filename


def validate_send_message(form_data):
    """
    This function validate the send_message details.
        
    :param form_data: message details
    :return:
        :status: status after send message 
        :message: message after send message
        
    """

    status = True
    message = None
    user_handle = form_data.get("user_handle")
    text = form_data.get("text")
    if is_handle(user_handle) is None:
        status = False
        message = "Invalid Handle"
        return status, message

    recipient = models.get_user(user_handle)
    if recipient is None:
        status = False
        message = "Handle does not exist"
        return status, message

    return status, message


def convert_to_json(unread_count, notifications):
    """
    This function convert data into json formate.
        
    :param unread_count: no of unread notifications
    :param notifications:  unread notifications
    :return: 
        :response_json: notifications in json
        
    """

    response_dict = {'UnreadCount': unread_count, 'Count': len(notifications), 'Data': notifications}
    response_json = json.dumps(response_dict, default=lambda x: x.__dict__)
    return response_json


def is_task_id(task_id):
    """
    This function check that task id is valid or not.
        
    :param task_id:  task id
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    
    if task_id is None:
        return False
    x = re.search("^[a-zA-Z0-9._ ]{5,45}$", task_id)
    if x is None:
        return False
    return True


def is_description(description):
    """
    This function check that description is valid or not.
        
    :param description:  description
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if description is None:
        return False
    x = re.search(".{1,100}", description)
    if x is None:
        return False
    return True
    return True


def is_task_type(task_type):
    """
    This function check that task type is valid or not.
        
    :param task_type:  task type
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if task_type is None:
        return False
    if is_info(task_type) or is_text(task_type) or is_upload(task_type):
        return True
    return False


def is_info(task_type):
    """
    This function check that task type is Info or not.
        
    :param task_type:  task type
    :return: 
        :True: if Info
        :False: if not Info
        
    """

    if task_type is None:
        return False
    if task_type == "Info":
        return True
    return False


def is_text(task_type):
    """
    This function check that task type is Text or not.
        
    :param task_type:  task type
    :return: 
        :True: if Text
        :False: if not Text
        
    """

    if task_type is None:
        return False
    if task_type == "Text":
        return True
    return False


def is_upload(task_type):
    """
    This function check that task type is Upload or not.
        
    :param task_type:  task type
    :return: 
        :True: if Upload
        :False: if not Upload
        
    """

    if task_type is None:
        return False
    if task_type == "Upload":
        return True
    return False


def is_handle(handle):
    """
    This function check that handle is valid or not.
        
    :param handle: handle of user
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    
    if handle is None:
        return False
    x = re.search("^[a-zA-Z0-9_]{1,45}$", handle)
    if x is None:
        return False
    return True


def is_password(password):
    """
    This function check that password is valid or not.
        
    :param password:  password of handle
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if password is None:
        return False
    x = re.search("^.{1,45}$", password)
    if x is None:
        return False
    return True


def is_name(name):
    """
    This function check that name is valid or not.
        
    :param name:  name of user
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if name is None:
        return False
    x = re.search("^[a-zA-Z][a-zA-Z ]{0,44}$", name)
    if x is None:
        return False
    return True


def is_email(email):
    """
    This function check that email is valid or not.
        
    :param email:  user email
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if email is None:
        return False
    x = re.search("^.+@.+$", email)
    if x is not None and len(x.group(0)) <= 45:
        return True
    return False


def is_user_type(user_type):
    """
    This function check that user_type is valid or not.
        
    :param user_type:  user type
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if user_type is None:
        return False
    if is_user(user_type) or is_moderator(user_type) or is_admin(user_type):
        return True
    return False


def is_gender(gender):
    """
    This function check that user have valid  gender or not.
        
    :param gender:  user gender
    :return: 
        :True: if valid gender
        :False: if not valid
        
    """

    
    if gender is None:
        return False
    if is_male(gender) or is_female(gender):
        return True
    return False


def is_male(gender):
    """
    This function check that user  is male or not.
        
    :param gender:  user gender
    :return: 
        :True: if Male
        :False: if not Male
        
    """

    if gender is None:
        return False
    if gender == "Male":
        return True
    return False


def is_female(gender):
    """
    This function check that user  is Female or not.
        
    :param gender:  user gender
    :return: 
        :True: if Female
        :False: if not Female
        
    """

    if gender is None:
        return False
    if gender == "Female":
        return True
    return False


def is_moderator(user_type):
    """
    This function check that user type is Moderator or not.
        
    :param user_type:  user type
    :return: 
        :True: if Moderator
        :False: if not Moderator
        
    """

    if user_type == "Moderator":
        return True
    return False


def is_user(user_type):
    """
    This function check that user type is User or not.
        
    :param user_type:  user type
    :return: 
        :True: if User
        :False: if not User
        
    """

    if user_type == "User":
        return True
    return False


def is_admin(user_type):
    """
    This function check that user type is Admin or not.
        
    :param user_type:  user type
    :return: 
        :True: if Admin
        :False: if not Admin
        
    """

    if user_type == "Admin":
        return True
    return False


def is_file_name(name):
    """
    This function check that file name is valid or not.
        
    :param name:  file name
    :return: 
        :True: if valid
        :False: if not valid
        
    """

    if name is None:
        return False
    x = re.search("^[a-zA-Z0-9_. ]{1,45}$", name)
    if x is not None and len(x.group(0)) <= 45:
        return True
    return False
