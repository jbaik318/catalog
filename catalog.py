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


def categoryToId(category_name):
	iso = session.query(Category).filter_by(name  = category_name.title())
	catId = ""
	for x in iso:
		catId = x.id
	category = session.query(Category).filter_by(id = catId).one()
	return category

def itemToId(item_name):
	iso = session.query(Item).filter_by(name = item_name)
	itemId = ""
	for x in iso:
		itemId =  x.id
	item = session.query(Item).filter_by(id = itemId).first()
	return item

#routing endpoints
@app.route('/')
def showCatalog():
	listCatalog = session.query(Category).all()
	listItem = session.query(Item).all()
	return render_template('index.html', catalog = listCatalog, item = listItem)
	
@app.route('/catalog/<category_name>')
@app.route('/catalog/<category_name>/items')
def showCategory(category_name):	
	listCatalog = session.query(Category).all()
	category = categoryToId(category_name)
	item = session.query(Item).filter_by(category_id = category.id)

	return render_template('viewCategory.html', catalog = listCatalog, category = category, item = item)

@app.route('/catalog/<category_name>/create', methods = ['GET','POST'])
def createItem(category_name):
	category = categoryToId(category_name)
	if request.method == 'POST':
		addItem = Item(name = request.form['name'], category_id = category.id)
		session.add(addItem)
		session.commit()
		return redirect(url_for('showCategory', category_name = category.name))
	else:
		return render_template('newCategory.html', category = category)

@app.route('/catalog/<item_name>/edit', methods = ['GET','POST'])
def editItem(item_name):
	item = itemToId(item_name)
	category = session.query(Category).filter_by(id = item.category_id).first()
	if request.method ==  'POST':
		item.name = request.form['name']
		session.add(item)
		session.commit()
		return redirect(url_for('showCategory', category_name = category.name))
	else:
		return render_template('editItem.html', item = item)
	

@app.route('/catalog/<item_name>/delete', methods = ['GET','POST'])
def deleteItem(item_name):
	item = itemToId(item_name)
	category = session.query(Category).filter_by(id = item.category_id).first()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('showCategory', category_name = category.name))
	else:
		return render_template('deleteItem.html', item = item )

'''@app.route('/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
	category = categoryToId(category_name)

	return ('this page shows details on each item')'''

#designate port to operate
if __name__ == '__main__':
  	app.secret_key = 'super_secret_key'
	app.debug = True
  	app.run(host = '0.0.0.0', port = 8000)
