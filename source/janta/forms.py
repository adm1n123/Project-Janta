from django import forms


class LoginForm(forms.Form):
    """ Form For Login"""
    handle = forms.CharField(label='Handle', max_length=45)
    password = forms.CharField(max_length=45, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    """ Form for Registration"""
    name = forms.CharField(label='Name', max_length=45)
    handle = forms.CharField(label='Handle', max_length=45)
    password = forms.CharField(label='Password', max_length=45, widget=forms.PasswordInput)
    conf_pass = forms.CharField(label='Confirm Password', max_length=45, widget=forms.PasswordInput)
    gender_choices = [('Male', 'Male'), ('Female', 'Female')]

    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect)
    user_type_choices = [('User', 'User'), ('Moderator', 'Moderator')]

    user_type = forms.ChoiceField(label='Account Type', choices=user_type_choices, widget=forms.RadioSelect)
    email = forms.EmailField(label='Email', max_length=45)


class CreateTaskForm(forms.Form):
    """ Form for Create Task"""
    task_type_choices = [('Info', 'Info'), ('Text', 'Text input'), ('Upload', 'File upload')]
    task_id = forms.CharField(label='Task Id', max_length=45, min_length=5, widget=forms.TextInput(attrs={'placeholder': '[a-zA-Z0-9._ ]'}))
    task_type = forms.ChoiceField(choices=task_type_choices, widget=forms.RadioSelect)
    description = forms.CharField(label='Description', max_length=100)
    deadline = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'required': 'required'}))


class AddUserForm(forms.Form):
    """ Form for Add User"""
    user_handles = forms.CharField(label='Handles', max_length=5000)
    regex = forms.CharField(label='regex')


class DeleteTaskForm(forms.Form):
    """ Form for Delete Task"""
    task_id = forms.CharField(label='Task Id', max_length=45)


class RemoveUserForm(forms.Form):
    """ Form for Remove User"""
    user_handle = forms.CharField(label='Handle', max_length=45)


class SendMessageForm(forms.Form):
    """ Form for Send Message"""
    user_handle = forms.CharField(label='', max_length=45, widget=forms.TextInput(attrs={'placeholder': 'Recipients handle'}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'type message here'}))


class EditProfileForm(forms.Form):
    """ Form for Edit Profile"""
    name = forms.CharField(label='Name', max_length=45)
    gender_choices = [('Male', 'Male'), ('Female', 'Female')]
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect)
    email = forms.EmailField(label='Email', max_length=45, required=False)
    about = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={'placeholder': 'write about yourself'}))
    git_link = forms.URLField(required=False)
    linkedin_link = forms.URLField(required=False)


class ChangePasswordForm(forms.Form):
    """ Form for Change password"""
    old_password = forms.CharField(label='Old Password', max_length=45, widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', max_length=45, widget=forms.PasswordInput)
    conf_pass = forms.CharField(label='Confirm Password', max_length=45, widget=forms.PasswordInput)

