from flask import Flask, render_template, request, url_for, redirect, flash, get_flashed_messages
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def ListItemsFromRest(restaurant_id):
    session = sessionmaker(bind = engine)()
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    session.close()
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['POST', 'GET'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        session = sessionmaker(bind = engine)()
        newItem = MenuItem(name = request.form['restname'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash('Added ' + newItem.name + ' to the menu!')
        session.close()
        return redirect(url_for('ListItemsFromRest', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html')

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['POST','GET'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        session = sessionmaker(bind=engine)()
        currentItem = session.query(MenuItem).filter_by(id = menu_id).one()
        oldName = currentItem.name
        currentItem.name = request.form['editname']
        session.commit()
        flash('Changed menu item ' + oldName + ' to ' + currentItem.name + '!')
        session.close()
        return redirect(url_for('ListItemsFromRest', restaurant_id = restaurant_id))
    else:
        session = sessionmaker(bind=engine)()
        currentRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('editmenuitem.html', restaurant = currentRestaurant, item = menuItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['POST', 'GET'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        session = sessionmaker(bind=engine)()
        currentItem = session.query(MenuItem).filter_by(id = menu_id).one()
        oldName = currentItem.name
        session.delete(currentItem)
        session.commit()
        flash('Deleted menu item ' + oldName + '!')
        session.close()
        return redirect(url_for('ListItemsFromRest', restaurant_id = restaurant_id))
    else:
        session = sessionmaker(bind=engine)()
        currentRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('deletemenuitem.html', restaurant = currentRestaurant, item = menuItem)
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)