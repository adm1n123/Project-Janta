"""ProjectJanta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from janta import views


urlpatterns = [
    # pattern matches the prefix if regex is not used



    path('', views.index),
    path('janta/index/', views.index),
    path('janta/profile/', views.profile),
    path('janta/edit-profile/', views.edit_profile),
    path('janta/change-password/', views.change_password),
    path('janta/login/', views.login),
    path('janta/logout/', views.logout),
    path('janta/register/', views.register),
    path('janta/send-message/', views.send_message),
    path('janta/messages/', views.get_messages),
    path('janta/delete-message/', views.delete_messages),
    path('janta/mark-as-read/', views.mark_as_read),  # JS request
    path('janta/get-notifications/', views.get_notifications),  # JS request

    # moderators urls
    path('janta/moderator/', views.moderator_home),
    path('janta/create-task/', views.create_task),
    path('janta/my-tasks/', views.my_tasks),
    path('janta/add-users/', views.add_users),
    path('janta/remove-user/', views.remove_user),
    path('janta/delete-task/', views.delete_task),
    path('janta/modify-task/', views.modify_task),
    path('janta/task-status/', views.task_status),
    path('janta/accept-submission/', views.accept_submission),
    path('janta/reject-submission/', views.reject_submission),

    # user urls
    path('janta/user/', views.user_home),
    path('janta/ongoing-tasks/', views.ongoing_tasks),
    path('janta/overdue-tasks/', views.overdue_tasks),
    path('janta/submit-task/', views.submit_task),
    path('janta/submitted-tasks/', views.submitted_tasks),

    # admin urls
    path('janta/admin/', views.admin),
    path('janta/admin-del-user/', views.admin_del_user),
    path('janta/admin-del-moderator/', views.admin_del_moderator),
    path('janta/admin-del-task/', views.admin_del_task),
    path('janta/admin-resetdb/', views.admin_resetdb),
    path('janta/admin-list-users/', views.admin_list_users),
    path('janta/admin-list-tasks/', views.admin_list_tasks),
    path('janta/admin-del-user_list/', views.admin_del_user_list),
    path('janta/admin-del-moderator_list/', views.admin_del_moderator_list),
    path('janta/admin-del-task_list/', views.admin_del_task_list),
]
