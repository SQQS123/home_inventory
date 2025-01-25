from flask import Flask,render_template,request,redirect,url_for,flash
from models import db,Item
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home_inventory.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html',items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        room = request.form['room']
        category = request.form['category']
        
        new_item = Item(name=name, description=description, room=room, category=category)
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('物品已删除！')
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.room = request.form['room']
        item.category = request.form['category']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit.html', item=item)



if __name__ == '__main__':
	app.run(debug=True)
