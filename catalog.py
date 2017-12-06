#import all libraries here
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)



#routing endpoints
@app.route('/')
def showCatalog():
	return ('this is the main catalog page')

@app.route('/<string:category>')
@app.route('/<string:category>/items')
def showCategory(category):	
	return ('this returns items within a catalog')

@app.route('/<string:category>/<string:item>')
def showItem(category, item):
	return ('this page shows details on each item')

@app.route('/<string:category>/create')
def createItem(category):
	return ('this page add a new item to category')

@app.route('/<string:category>/edit')
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
