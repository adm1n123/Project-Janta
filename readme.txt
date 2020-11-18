Deepak Singh Baghel(203050005 deepakbaghel) backend
Ankush Agarwal(203050007 ankushagrawal) frontend
Abhinandan Singh(203050031 abhinandan) frontend
Rajendra(203050094 rajcseosian) backend


Motivation:
In this online semester collaborating with peers and team members to complete tasks and project has been difficult. This happens because the
work is scattered on many platforms. There was no single platform where the teams can collaborate efficiently. Due to this pandemic most of the
job is done from home so there was a need of a single platform that can be used to complete the task simply and efficiently.

How to use:

Install python 3.8 if not installed already
$sudo apt install python 3.8

1.1 Clone the repository  https://git.cse.iitb.ac.in/deepakbaghel/ProjectJanta/tree/master/


1.2.1 Install virtual environment if installed go to step 1.2.2
$sudo pip3 install virtualenv


1.2.2 Create virtual environment in source directory
source$ virtualenv venv


1.3 Activate virtual environment
source$ source venv/bin/activate


1.4 Install django
source$ pip3 install django


1.5 install pymysql
source$ pip3 install PyMySQL


1.6 Deactivate virtual environment
source$ deactivate


2.1 Install mysql server if installed then goto source/ProjectJanta/settings.py
and provide HOST, PORT, USER and PASSWORD then go to step 2.5
$sudo apt install mysql-server


2.2 Open mysql
sudo mysql


2.3 Modify the plugin
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';


2.4 Run command to make changes
mysql> FLUSH PRIVILEGES;


2.5 Verify mysql server is started or not
$ systemctl status mysql.service

If not then run command
$sudo systemctl start mysql


2.6 Login into mysql client and create database and exit
mysql> CREATE DATABASE projectjanta;exit;


3.1 Activate the virtual environment from source directory
source$ source venv/bin/activate


3.2 Run server
source$ python3 manage.py runserver


3.3 hit URL
127.0.0.1:8000/janta/admin-resetdb?key=Wq5tx7r3Zp


3.4 Stop server
Press CTRL+C


3.5 Migrate django session
source$ python3 manage.py migrate sessions


3.6 Run server
source$ python3 manage.py runserver


4.0 Visit ProjectJanta Index page
http://127.0.0.1:8000/
