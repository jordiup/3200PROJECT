# CITS3200

## Team O

First Name	Surname	Email

Max Michael	Evans	21970246@student.uwa.edu.au

Mitchell Adrian Ellis	Gill	21953849@student.uwa.edu.au

Jordi	Hermoso Clarke	21959041@student.uwa.edu.au

Robin Luca	Markwitz	21968594@student.uwa.edu.au

Adi	Santoso	21760921@student.uwa.edu.au

Zhong Han	Yong	21970086@student.uwa.edu.au

https://drive.google.com/open?id=1O0h4gvzOGBzJKG4CB2H1QT9IeZqqf6hx

# letter_extraction directory

This contains the Django project I’ve been fiddling around with. It has the updated models, skeleton views, some half-finished HTML pages and CSS stylesheet, a small skeleton script to upload test data with, and a few other default Django files.

## Getting started

This is a Django project. I use VS Code,  I’m not sure what everyone else uses but this would be my suggestion.
Go to the terminal and enter the letter_extraction directory. Type 
```
python3 manage.py runserver
```
This will start the server on port 8000. To see the login page, go to a browser and type
```
127.0.0.1:8000/db/login/
```
Note that the views don’t actually handle any form data yet, so any account can login right now.

## Database

The database information is specified in letter_extraction/settings.py. Make sure you have PostgreSQL installed (refer to the django_postgres_install.txt file on GitHub if you need to install). You will most likely need to change your port to 5432 (I am running two PostgreSQL servers). You will also need to create a database called testdb in your PostgreSQL instance for this to work.
Note: the db.sqlite3 file does nothing.

## Models

The models can be found in db/models.py. There are User, Document, Person, Location and PersonLocation models. To add the models to the database, type 
```
python3 manage.py makemigrations
```
then type 
```
python3 manage.py migrate
```
If this does not work consult the Django tutorials.

## Inserting data

If you wish to insert test data, there is a script in the main directory called modelAddScripts.py. In the terminal, type 
```
python3 manage.py shell
```
and then run this script, after changing the default values that are in there. You can also play around with the data in there to test some things, view the Django tutorial if you want to see how to do that.

## Views

Views can be found in db/views.py. The views are the Django constructs that take a request (from form data submitted by a user), do stuff with the form data, and then send back a response. There are already some views defined, however they don’t do anything meaningful. When adding a view, be careful - you need to add some information to db/urls.py also (see what I did with the other views and just copy that). Make sure to make new files to handle all the processing - don’t do everything in the views.

## Admin

To log into the admin page, run the server and type 
```
127.0.0.1:8000/admin/
```
into a browser. The username is “admin” and the password is “cits3200groupo”. 

## HTML/CSS/JavaScript

The HTML files can be found in the db/templates/db directory. When creating new files, you MUST put them in this directory, otherwise Django can’t find them. Every new HTML file should have the header div, the stylesheet loader and {% load static %} in it.
I’ve made some really simple pages that are meant to be edited. To see the login page, go to a browser and type
```
127.0.0.1:8000/db/login/
```
Press login and then you will see the home page. The links in the header work, you can navigate between “Home”, “Search”, and “Upload”. The search page is the only one that has actually been worked on.

The CSS file can be found in the db/static/db directory. Right now there isn’t too much in there. A good resource for adding more dynamic elements is this https://htmlcheatsheet.com/css/ generator. If you wish to add JavaScript files, you must also put them in this directory. There is currently no JS in this project. 

Any specific questions, refer to the Django tutorial series, they most likely have an answer. Else consult me, but no guarantees.

## GitHub

Make sure to create a new branch when working on stuff, and then merge back into master. We want to avoid complicated merges at all costs.
 
