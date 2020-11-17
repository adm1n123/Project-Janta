"""
Create your views here.

This program deals with task function in our Janta application. 
Different functions related to task will be handled.

""" 
   
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from janta import models
from janta import forms
from janta import viewhelper


def create_task(request):

    """
    This function creates the task by request.

    	:type request: http request
    	:param request: the request sent for the task
    	:return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                task_form = forms.CreateTaskForm()
                user = models.get_user(handle)
                context = {'create_task_form': task_form, 'user': user}
                return render(request, 'janta/create-task.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                form = forms.CreateTaskForm(request.POST)
                message = "Invalid Form please fill again"
                if form.is_valid():
                    fd = form.cleaned_data
                    status, message = viewhelper.validate_create_task(fd)
                    if status:
                        models.insert_task(task_id=fd.get("task_id"), owner=handle, description=fd.get("description"),
                                           task_type=fd.get("task_type"), deadline=fd.get("deadline"))
                        return redirect('/janta/moderator/')
                context = {'create_task_form': form, 'message': message}
                return render(request, 'janta/create-task.html', context)
        return redirect("/janta/login/")


def my_tasks(request):
    """
    This function handles the functionality of the task by request.

    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                tasks = models.get_my_tasks(owner=handle)
                user = models.get_user(handle)
                context = {'tasks': tasks, 'user': user}
                return render(request, 'janta/my-tasks.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    if request.method == 'POST':
        return redirect("/janta/index/")


def delete_task(request):
    """
    This function deletes the task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                delete_task_form = forms.DeleteTaskForm(request.POST)
                recent_tasks = models.get_my_tasks(owner=handle, recent=True)
                user = models.get_user(handle)
                assign_task_form = forms.AddUserForm()
                delete_form_message = "Invalid Form please fill again"
                if delete_task_form.is_valid():
                    fd = delete_task_form.cleaned_data
                    status, delete_form_message = viewhelper.validate_delete_task(moderator=handle, form_data=fd)
                    if status:
                        models.delete_task(task_id=fd.get("task_id"))
                        delete_form_message = "Task Deleted"
                        delete_task_form = forms.DeleteTaskForm()
                        recent_tasks = models.get_my_tasks(owner=handle, recent=True)
                context = {'recent_tasks': recent_tasks, 'user': user, 'add_user_form': assign_task_form,
                           'delete_task_form': delete_task_form, 'delete_form_message': delete_form_message}
                return render(request, 'janta/moderator.html', context)
            return redirect('/janta/index/')
        return redirect("/janta/login/")
    
    
def ongoing_tasks(request):
    """
    This function maintains the ongoing task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user(user_type):
                ong_tasks = models.get_ongoing_tasks(handle=handle)
                user = models.get_user(handle)
                context = {'ongoing_tasks': ong_tasks, 'user': user}
                return render(request, 'janta/ongoing-tasks.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    if request.method == 'POST':
        return redirect("/janta/index/")
    return None
    

def overdue_tasks(request):
    """
    This function maintains the overdue task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user(user_type):
                over_tasks = models.get_overdue_tasks(handle=handle)
                user = models.get_user(handle)
                context = {'overdue_tasks': over_tasks, 'user': user}
                return render(request, 'janta/overdue-tasks.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    if request.method == 'POST':
        return redirect("/janta/index/")

    
def submitted_tasks(request):
    """
    This function keeps track of the submitted task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user(user_type):
                fn_tasks = models.get_submitted_tasks(handle=handle)
                user = models.get_user(handle)
                context = {'submitted_task': fn_tasks, 'user': user}
                return render(request, 'janta/submitted-tasks.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    if request.method == 'POST':
        return redirect("/janta/index/")
    
    
def submit_task(request):
    """
    This function submits the task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user(user_type):
                fd = request.POST
                task_id = fd.get("task_id")
                task = models.get_task(task_id=task_id)
                if task is not None:
                    if viewhelper.is_info(task_type=task.task_type):
                        models.submit_task(task_id=task_id, handle=handle, submission="")
                        return redirect('/janta/submitted-tasks/')
                    elif viewhelper.is_text(task_type=task.task_type):
                        models.submit_task(task_id=task_id, handle=handle, submission=fd.get("input_txt"))
                        return redirect('/janta/submitted-tasks/')
                    elif viewhelper.is_upload(task_type=task.task_type):
                        file = request.FILES.get("input_file")
                        if file is not None and viewhelper.is_file_name(file.name):
                            path = viewhelper.save_file(file=file, handle=handle, task_id=task_id)
                            models.submit_task(task_id=task_id, handle=handle, submission=path)
                            return redirect('/janta/submitted-tasks/')
                        user = models.get_user(handle)
                        message = 'Invalid file name please submit again. file name regex: [a-zA-Z0-9_. ]{1,45}'
                        return render(request, 'janta/error.html', context={'message': message, 'user': user})
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def modify_task(request):
    """
    This function modifies the task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                task_id = request.GET.get("task_id")
                if task_id is not None:
                    task = models.get_task(task_id)
                    task_form = forms.CreateTaskForm(
                        initial={'task_id': task_id, 'task_type': task.task_type,
                                 'description': task.description, 'deadline': task.deadline})
                    # task_form.fields['task_id'].widget.attrs['disabled'] = True
                    task_form.fields['task_id'].widget.attrs['readonly'] = True
                    user = models.get_user(handle)
                    context = {'modify_task_form': task_form, 'user': user}
                    return render(request, 'janta/modify-task.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                form = forms.CreateTaskForm(request.POST)
                message = "Invalid Form please fill again"
                if form.is_valid():
                    fd = form.cleaned_data
                    status, message = viewhelper.validate_modify_task(fd)
                    if status:
                        models.modify_task(task_id=fd.get("task_id"), owner=handle, description=fd.get("description"),
                                           task_type=fd.get("task_type"), deadline=fd.get("deadline"))
                        return redirect('/janta/moderator/')
                form.fields['task_id'].widget.attrs['readonly'] = True
                user = models.get_user(handle)
                context = {'modify_task_form': form, 'message': message, 'user': user}
                return render(request, 'janta/modify-task.html', context)
        return redirect("/janta/login/")


def task_status(request):
    """
    This function keeps track of the status of task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                task_id = request.GET.get("task_id")
                if task_id is not None:
                    task = models.get_task(task_id)
                    if task is not None and task.owner == handle:
                        user = models.get_user(handle)
                        sub_status = models.get_submission_status(task_id=task_id, moderator=handle)
                        submissions = models.get_not_accepted_submissions(task_id=task_id)
                        context = {'task': task, 'user': user, 'sub_status': sub_status, 'submissions': submissions}
                        return render(request, 'janta/task-status.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def accept_submission(request):
    """
    This function accepts the submitted task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                task_id = request.GET.get("task_id")
                user_handle = request.GET.get("handle")
                if task_id is not None and user_handle is not None:
                    task = models.get_task(task_id)
                    user_task_map = models.get_user_task_map(task_id=task_id, handle=user_handle)
                    if task is not None and task.owner == handle and user_task_map is not None:
                        models.accept_submission(task_id=task_id, handle=user_handle)
                        return redirect('/janta/task-status/?task_id='+task_id)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def reject_submission(request):
    """
    This function rejects the submitted task by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                task_id = request.GET.get("task_id")
                user_handle = request.GET.get("handle")
                if task_id is not None and user_handle is not None:
                    task = models.get_task(task_id)
                    user_task_map = models.get_user_task_map(task_id=task_id, handle=user_handle)
                    if task is not None and task.owner == handle and user_task_map is not None:
                        models.reject_submission(task_id=task_id, handle=user_handle)
                        return redirect('/janta/task-status/?task_id='+task_id)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def add_users(request):
    """
    This function add users by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                add_user_form = forms.AddUserForm(request.POST)
                delete_task_form = forms.DeleteTaskForm()
                remove_user_form = forms.RemoveUserForm()
                add_user_message = "Invalid Form please fill again"
                if add_user_form.is_valid():
                    fd = add_user_form.cleaned_data
                    status, add_user_message, user_handles = viewhelper.validate_add_user(form_data=fd, moderator=handle)
                    if status:
                        add_user_message = models.add_users(moderator=handle, user_handles=user_handles)
                        add_user_form = forms.AddUserForm()
                recent_tasks = models.get_my_tasks(owner=handle, recent=True)
                user = models.get_user(handle)
                context = {'add_user_form': add_user_form, 'add_user_message': add_user_message,
                           'recent_tasks': recent_tasks, 'user': user, 'delete_task_form': delete_task_form,
                           'remove_user_form': remove_user_form}
                return render(request, 'janta/moderator.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def remove_user(request):
    """
    This function removes the user by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                add_user_form = forms.AddUserForm()
                delete_task_form = forms.DeleteTaskForm()
                remove_user_form = forms.RemoveUserForm(request.POST)
                remove_user_message = "Invalid Form please fill again"
                if remove_user_form.is_valid():
                    fd = remove_user_form.cleaned_data
                    status, remove_user_message, user_handle = viewhelper.validate_remove_user(form_data=fd, moderator=handle)
                    if status:
                        models.remove_user(user=user_handle, moderator=handle)
                        remove_user_form = forms.RemoveUserForm()
                        remove_user_message = "Handle removed"
                recent_tasks = models.get_my_tasks(owner=handle, recent=True)
                user = models.get_user(handle)
                context = {'add_user_form': add_user_form, 'remove_user_message': remove_user_message,
                           'recent_tasks': recent_tasks, 'user': user, 'delete_task_form': delete_task_form,
                           'remove_user_form': remove_user_form}
                return render(request, 'janta/moderator.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def moderator_home(request):
    """
    This function moderates the form request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_moderator(user_type):
                recent_tasks = models.get_my_tasks(owner=handle, recent=True)
                user = models.get_user(handle)
                assign_task_form = forms.AddUserForm()
                delete_task_form = forms.DeleteTaskForm()
                remove_user_form = forms.RemoveUserForm()
                context = {'recent_tasks': recent_tasks, 'user': user, 'add_user_form': assign_task_form,
                           'delete_task_form': delete_task_form, 'remove_user_form': remove_user_form}
                return render(request, 'janta/moderator.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def user_home(request):
    """
    This function handles the notification by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user(user_type):
                ong_tasks = models.get_recent_ongoing_tasks(handle=handle)
                user = models.get_user(handle)
                notifications = models.get_notifications(handle)
                context = {'rcnt_ong_tasks': ong_tasks, 'user': user, 'notifications': notifications}
                return render(request, 'janta/user.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")


def register(request):
    """
    This function registers the user by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        message = "Invalid Form please fill again"
        if form.is_valid():
            fd = form.cleaned_data
            status, message = viewhelper.validate_registration(fd)
            if status:
                models.user_register(handle=fd.get("handle"), password=fd.get("password"), user_type=fd.get("user_type"),
                                     name=fd.get("name"), emailid=fd.get("email"), gender=fd.get("gender"))
                return redirect("/janta/login/")
        context = {'registration_form': form, 'message': message}
        return render(request, 'janta/register.html', context)
    elif request.method == 'GET':
        form = forms.RegistrationForm()
        context = {'registration_form': form}
        return render(request, 'janta/register.html', context)
    
    
def login(request):
    """
    This function deals with the login of user by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        message = 'Invalid form please try again'
        if form.is_valid():
            login_data = form.cleaned_data
            handle = login_data.get("handle")
            password = login_data.get("password")
            status, message = viewhelper.validate_login(handle, password)
            if status:
                user = models.get_user(handle)
                viewhelper.set_session(request, user)
                if viewhelper.is_admin(user.user_type):
                    return redirect("/janta/admin/")
                if viewhelper.is_moderator(user.user_type):
                    return redirect("/janta/moderator/")
                if viewhelper.is_user(user.user_type):
                    return redirect("/janta/user/")
                message = 'Session creation failed please try again'
        context = {'login_form': form, 'message': message}
        return render(request, 'janta/login.html', context)
    elif request.method == 'GET':
        # do not redirect here otherwise it will fall in loop or change url pattern instead
        form = forms.LoginForm()
        context = {'login_form': form}
        return render(request, 'janta/login.html', context)
    
    
def logout(request):
    """
    This function deals with the logout of the user by request.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            request.session.flush()
        return redirect("/janta/index/")


def index(request):
    """
    This function is the index page of user.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user_type(user_type):
                user = models.get_user(handle)
                context = {'user': user}
                return render(request, 'janta/index.html', context)
        context = {'user': None}
        return render(request, 'janta/index.html', context)
    
    
def profile(request):
    """
    This function is the profile page of the user.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            params = request.GET.dict()
            handle = params.get("handle")
            stalker = models.get_user(request.session.get("handle"))
            if handle is None or not viewhelper.is_handle(handle):
                handle = stalker.user_handle
            user = models.get_user(handle)
            if user is not None:
                if stalker.user_handle != user.user_handle:
                    noti_type = "Profile Visit"
                    text = stalker.user_handle+" has visited you profile"
                    models.sent_notification(handle=user.user_handle, noti_type=noti_type, text=text)
                context = {'user': stalker, 'profile_user': user}
                return render(request, 'janta/profile.html', context)
        return redirect("/janta/index/")
    elif request.method == 'POST':
        # do profile update
        print("profile post method called")


def edit_profile(request):
    """
    This function is use to edit the profile page of the user.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user = models.get_user(handle)
            edit_profile_form = forms.EditProfileForm(
                initial={'name': user.user_name, 'gender': user.user_gender, 'email': user.user_email,
                         'about': user.user_about, 'git_link': user.git_link, 'linkedin_link': user.linkedin_link})
            context = {'user': user, 'edit_form': edit_profile_form}
            return render(request, 'janta/edit-profile.html', context)
        return redirect("/janta/index/")
    elif request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            form = forms.EditProfileForm(request.POST)
            message = "Invalid Form please fill again"
            if form.is_valid():
                fd = form.cleaned_data
                status, message = viewhelper.validate_profile_edit(fd)
                if status:
                    message = "Error updating details try again"
                    models.profile_edit(handle=handle, name=fd.get("name"), emailid=fd.get("email"),
                                        gender=fd.get("gender"), about=fd.get("about"),
                                        git_link=fd.get("git_link"), linkedin_link=fd.get("linkedin_link"))
                    return redirect("/janta/profile/")
            context = {'edit_form': form, 'message': message}
            return render(request, 'janta/edit-profile.html', context)


def change_password(request):
    """
    This function is use to change password for the user.
    
    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user = models.get_user(handle)
            change_pass_form = forms.ChangePasswordForm()
            context = {'user': user, 'change_pass_form': change_pass_form}
            return render(request, 'janta/change-password.html', context)
        return redirect("/janta/index/")
    elif request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            form = forms.ChangePasswordForm(request.POST)
            message = "Invalid Form please fill again"
            user = models.get_user(handle)
            if form.is_valid():
                message = "Error changing password try again"
                fd = form.cleaned_data
                status, message = viewhelper.validate_change_password(fd)
                if status:
                    message = "Incorrect old password"
                    status = models.change_password(
                        handle=handle, old_password=fd.get("old_password"), new_password=fd.get("new_password")
                    )
                    if status:
                        return redirect("/janta/profile/")
            context = {'change_pass_form': form, 'message': message, 'user': user}
            return render(request, 'janta/change-password.html', context)
    
    
def send_message(request):
    """
    This function is use to send the messages.

    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user_type(user_type):
                message_form = forms.SendMessageForm(request.POST)
                message = 'Invalid form please try again'
                user = models.get_user(handle=handle)
                messages = models.get_messages(handle=handle)
                if message_form.is_valid():
                    fd = message_form.cleaned_data
                    status, message = viewhelper.validate_send_message(fd)
                    if status:
                        user_handle = fd.get("user_handle")
                        text = fd.get("text")
                        models.send_message(sender=handle, receiver=user_handle, text=text)
                        message = "Message sent"
                        message_form = forms.SendMessageForm()
                        user = models.get_user(handle=handle)
                        messages = models.get_messages(handle=handle)
                context = {'send_message_form': message_form, 'user': user, 'message': message, 'my_messages': messages}
                return render(request, 'janta/message.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def get_messages(request):
    """
    This function is use to get the messages.

    	:type request: http request
    	:param request: the request sent for the task
    	:return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            receiver = request.GET.dict().get("receiver")  # if request coming from profile
            message_form = forms.SendMessageForm()
            if viewhelper.is_handle(receiver) and models.get_user(receiver) is not None:
                message_form = forms.SendMessageForm(initial={'user_handle': receiver})
                message_form.fields['user_handle'].widget.attrs['readonly'] = True
            if viewhelper.is_user_type(user_type):
                user = models.get_user(handle=handle)
                messages = models.get_messages(handle=handle)
                context = {'send_message_form': message_form, 'user': user, 'message': '', 'my_messages': messages}
                return render(request, 'janta/message.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")


def delete_messages(request):
    """
    This function is use to delete the messages.

    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            msg_id = request.GET.dict().get("id")
            if msg_id is not None:
                models.delete_message(msg_id=msg_id, handle=handle)
                return redirect('/janta/messages/')
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
@csrf_exempt
def mark_as_read(request):
    """
    This function is used to read the messages and mark them as read.

    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            noti_id = request.POST.dict().get("id")
            if viewhelper.is_user_type(user_type) and noti_id is not None:
                noti_id_int = int(noti_id)
                user = models.get_user(handle=handle)
                if user is not None:
                    models.mark_as_read(noti_id=noti_id_int, handle=handle)
                    return JsonResponse({'Status': 1}, safe=False)
        return JsonResponse({'Status': 0}, safe=False)


@csrf_exempt
def get_notifications(request):
    """
    This function is use to get the notifications.

    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_user_type(user_type):
                user = models.get_user(handle=handle)
                if user is not None:
                    notifications = models.get_notifications(handle)
                    json_res = viewhelper.convert_to_json(notifications)
                    return HttpResponse(json_res)
        return JsonResponse({'Count': 0}, safe=False)
    
    
# ################################################################  ADMIN ##########################################
def admin(request):
    """
    This function maintains the admin page.


    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'GET':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_admin(user_type):
                user = models.get_user(handle=handle)
                context = {'user': user, 'message': ''}
                return render(request, 'janta/admin.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")


def reset_database(request):
    """
    This function is use to reset the database by request.


    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    models.reset_db()
    message = "see operations in console"
    context = {message: message}
    return render(request, 'janta/error.html', context)
    
    
def admin_del_user(request):
    """
    This function is used to delete the user by admin.


    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_admin(user_type):
                user = models.get_user(handle=handle)
                fd = request.POST
                del_user_handle = fd.get("del_user_handle")
                message = "Invalid handle"
                if del_user_handle is not None:
                    message = "User does not exists"
                    del_user = models.get_user(del_user_handle)
                    if del_user is not None and viewhelper.is_user(del_user.user_type):
                        models.admin_del_user(handle=del_user_handle)
                        message = "User Deleted"
                context = {'user': user, 'message': message}
                return render(request, 'janta/admin.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def admin_del_moderator(request):
    """
    This function is used to delete the moderator by admin.

    :type request: http request
    :param request: the request sent for the task 
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_admin(user_type):
                user = models.get_user(handle=handle)
                fd = request.POST
                del_moderator_handle = fd.get("del_moderator_handle")
                message = "Invalid handle"
                if del_moderator_handle is not None:
                    message = "Moderator does not exists"
                    del_moderator = models.get_user(del_moderator_handle)
                    if del_moderator is not None and viewhelper.is_moderator(del_moderator.user_type):
                        models.admin_del_moderator(handle=del_moderator_handle)
                        message = "Moderator Deleted"
                context = {'user': user, 'message': message}
                return render(request, 'janta/admin.html', context)
            return redirect("/janta/index/")
        return redirect("/janta/login/")
    
    
def admin_del_task(request):
    """
    This function is used to delete the tasks by admin.


    :type request: http request
    :param request: the request sent for the task
    :return: redirecting to the page according to http request
    """
    if request.method == 'POST':
        if request.session.keys():
            handle = request.session.get("handle")
            user_type = request.session.get("user_type")
            if viewhelper.is_admin(user_type):
                user = models.get_user(handle)
                message = "Invalid Task Id"
                fd = request.POST
                task_id = fd.get("del_task_id")
                if task_id is not None and viewhelper.is_task_id(task_id=task_id):
                    task = models.get_task(task_id=task_id)
                    message = "Task Id does not exists"
                    if task is not None:
                        models.admin_del_task(task_id=task_id)
                        message = "Task deleted"
                context = {'user': user, 'message': message}
                return render(request, 'janta/admin.html', context)
            return redirect('/janta/index/')
        return redirect("/janta/login/")
    
   

     


