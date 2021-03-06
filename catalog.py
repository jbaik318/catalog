'''
Catalog.py is the heart and soul that allows the entire interface system to work. 

This file insures that the user is properly redirected to the corrent endpoint based on the user's actions.
This file also takes into account validating the user's credentials through Google's Oauth2/v1.
Based on whether or not the user is the original creator of each item, this file will allow proper access and action.

Created by: John B
Contact:  jbaik318@gmail.com

'''

#import all libraries here
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Create an engine callable object that allows interaction between database and file
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession =  sessionmaker(bind = engine)
session = DBSession()

# Read the google Oauth credentials 
CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog"

# Serve as an anti-forgery state token with randomized token
@app.route('/login')
def showLogin():
	state =  ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state

	return render_template('login.html', STATE = state)


# Use Google's Oauth to connect to user's Google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists. If it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output


# Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
    
# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    print(url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print(result)
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        ### make a sucessful log out page that links back to main page
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        ### make a sucessful log out page that links back to main page
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


# Shortcut functions
# This function take the category name and returns a database type of that category
def categoryToId(category_name):
	iso = session.query(Category).filter_by(name  = category_name.title())
	catId = ""
	for x in iso:
		catId = x.id
	category = session.query(Category).filter_by(id = catId).one()
	return category

# This function take the item name and returns a database type of that item
def itemToId(item_name):
	iso = session.query(Item).filter_by(name = item_name)
	itemId = ""
	for x in iso:
		itemId =  x.id
	item = session.query(Item).filter_by(id = itemId).first()
	return item


# Route User to Endpoints
@app.route('/')
def showCatalog():
	listCatalog = session.query(Category).all()
	listItem = session.query(Item).all()
	if 'username' not in login_session:
		return render_template('publiccatalog.html', catalog = listCatalog, item = listItem)
	else:
		return render_template('index.html', catalog = listCatalog, item = listItem)


@app.route('/catalog/<category_name>')
@app.route('/catalog/<category_name>/items')
def showCategory(category_name):	
	listCatalog = session.query(Category).all()
	category = categoryToId(category_name)
	item = session.query(Item).filter_by(category_id = category.id)
	if 'username' not in login_session:
		return render_template('publicViewCategory.html', catalog= listCatalog, category = category, item = item)
	else:
		return render_template('viewCategory.html', catalog = listCatalog, category = category, item = item)


@app.route('/catalog/<category_name>/create', methods = ['GET','POST'])
def createItem(category_name):
    if 'username' not in login_session:
        return redirect('/login')catalog = session.query(Category).all()
    category = categoryToId(category_name)

    if request.method == 'POST':
        addItem = Item(name = request.form['name'], description = request.form['description'], catType = request.form.get('category'), category_id = category.id, user_id = login_session['user_id'])
        session.add(addItem)
        session.commit()
        catalogJSON()
        return redirect(url_for('showCategory', category_name = category.name))
    else:
		return render_template('newCategory.html', category = category, catalog = catalog )


@app.route('/catalog/<item_name>/edit', methods = ['GET','POST'])
def editItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Category).all()
    item = itemToId(item_name)
    category = session.query(Category).filter_by(id = item.category_id).first()
    if item.user_id != login_session['user_id']:
		### create a js file for this line below
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()''>"
    if request.method ==  'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.catType = request.form['category']
        session.add(item)
        session.commit()
        catalogJSON()
        return redirect(url_for('showCategory', category_name = category.name))
    else:
        return render_template('editItem.html', item = item, catalog = catalog)

@app.route('/catalog/<item_name>/delete', methods = ['GET','POST'])
def deleteItem(item_name):
    if 'username' not in login_session:
        return redirect('/login')
    item = itemToId(item_name)
    category = session.query(Category).filter_by(id = item.category_id).first()
    if item.user_id != login_session['user_id']:
        ### create a js file for this line below
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please create your own item in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        catalogJSON()
        return redirect(url_for('showCategory', category_name = category.name))
    else:
        return render_template('deleteItem.html', item = item )


@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
	item = itemToId(item_name)
	category = categoryToId(category_name)
	if 'username' not in login_session:
		return render_template('publicViewItem.html', item = item, category = category)
	else:
		return render_template('viewItem.html', item = item, category =category)

    
# Updates json file after every CRUD functon
@app.route('/catalog.json')
def catalogJSON():
    category = session.query(Category).all()
    item = session.query(Item).all()

    catalog = [] 
    for c in category:
        print('start of new category')
        catItem = []
        catalog.append(c.serialize)
        for i in item:
            if i.category_id == c.id:
                catItem.append(i.serialize)
        catalog[c.id-1]['item'] = catItem         
    cat = {'category': catalog}
    
    with open('catalog.json', 'w') as outfile:
        json.dump(cat, outfile)
    
    return jsonify(cat)

    





#designate port to operate
if __name__ == '__main__':
  	app.secret_key = 'super_secret_key'
	app.debug = True
  	app.run(host = '0.0.0.0', port = 8000)
