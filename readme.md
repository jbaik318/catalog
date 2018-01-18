# Udacity Catalog Project

## Goal
The objective of this project is to create a backend server program that hosts a web-based catalog for authorized users and non-authorized users.

File Content 
<dl>
    <dt>catalog.py</dt>
    <dd>The heart and soul of the catalog program. This file reroutes users to designated endpoints based on their requests and authorization.</dd>
    <dt>database_setup.py</dt>
    <dd>This program is need only to setup a database where the users can populate</dd>
    <dt>populate_database.py</dt>
    <dd>to be determined if needed</dd>
    <dt>client_secret.json</dt>
    <dd>This file authenicates the use of api through provided keys from a third party (Google Inc.)</dd>
    <dt>templates</dt>
    <dd>This directory contains all the html endpoints that catalog.py redirects user to.</dd>
    ***<dt>head.html</dt>
    ***<dd>Contains all links and references needed for all pages.</dd>
    ***<dt>header.html</dt>
    ***<dd>Contains a header that will be placed on all pages when user has been authorized.</dd>
    ***<dt>publicHeader.html</dt>
    ***<dd>Contains a header that will be placed on all pages when user is unauthorized.</dd>
    ***<dt>index.html</dt>
    ***<dd>Contains the first page that shows all categories and items</dd>
    ***<dt>login.html</dt>
    ***<dd>Login page that allows user to create and authenticate themselves.</dd>
    ***<dt>publiccatalog.html</dt>
    ***<dd>A public view of the main page that does not offer CRUD capabilities</dd>
    ***<dt>viewCategory.html</dt>
    ***<dd>Displays items within a certain category and allows CRUD abilities.</dd>
    ***<dt>publicViewCategory.html</dt>
    ***<dd>A public view of specific categories and their respective items without CRUD capabilities.</dd>
    ***<dt>viewItem.html</dt>
    ***<dd>Provides authorized user with item informationa and edit/delte options</dd>
    ***<dt>publicViewItem.html</dt>
    ***<dd>Provides unauthorized user information about item.</dd>
    ***<dt>editItem.html</dt>
    ***<dd>User can edit inidivdual parts of the item.</dd>
    ***<dt>deleteItem.html</dt>
    ***<dd>User can delete Item.</dd>
    ***<dt>newCategory.html</dt>
    ***<dd>User can create a new Item in a category.</dd>
    <dt>Static</dt>
    <dd>Directory that contains static css file.</dd>
    ***<dt>styles.css</dt>
    ***<dd>Styling for all pages on website.</dd>
</dl>

## Prerequisites

###You need the follow libraries in python for the program to work
Flask
Sqlalchemy
Oauth2

## Setup

### Clone the remote repository to local repository
```
git clone https://github.com/jbaik318/catalog
```

### Set up database
``` 
python database_setup.py
```

### Start the server program
```
python catalog.py
```


created by John B.
