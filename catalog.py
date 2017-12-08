#import all libraries here
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Item
app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession =  sessionmaker(bind = engine)
session = DBSession()

#routing endpoints
@app.route('/')
def showCatalog():
	listCatalog = session.query(Category).all()
	listItem = session.query(Item).all()
	return render_template('index.html', catalog = listCatalog, item = listItem)
	
@app.route('/<category_name>')
@app.route('/<category_name>/items')
def showCategory(category_name):	
	listCatalog = session.query(Category).all()
	iso = session.query(Category).filter_by(name  = category_name.title())
	for x in iso:
		catId = x.id
	category = session.query(Category).filter_by(id = catId).one()
	item = session.query(Item).filter_by(category_id = category.id)

	return render_template('viewCategory.html', catalog = listCatalog, category = category, item = item)


@app.route('/<string:category>/<string:item>')
def showItem(category, item):

	return ('this page shows details on each item')

@app.route('/<string:category>/create', methods = ['GET','POST'])
def createItem(category):
	specificCategory = session.query(Category).filter_by(name = category.title())
	category = session.query(Category).filter_by(id = specificCategory[0].id)
	
	if request.method == 'POST':
		addItem = Item(name = request.form['name'], description = request.form['description'], menu_id = category.id)
		session.add(addItem)
		session.commit()
		return redirect(url_for('showCategory'))
	else:
		return render_template('newCategory.html')

@app.route('/<string:category>/edit', methods = ['GET','POST'])
def editItem(category):

	return ('this page edits item')

@app.route('/<string:category>/delete')
def deleteItem(category):
	return ('this page deletes item')


#designate port to operate
if __name__ == '__main__':
  	app.secret_key = 'super_secret_key'
	app.debug = True
  	app.run(host = '0.0.0.0', port = 5000)
