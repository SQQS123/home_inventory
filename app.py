from flask import Flask,render_template,request,redirect,url_for,flash
from models import db,Item
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    # items = Item.query.all()

    # 分页逻辑
    page = request.args.get('page', 1, type=int)  # 获取当前页码，默认为第一页
    per_page = 10  # 每页显示的条数
    pagination = Item.query.paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    total_pages = pagination.pages  # 总页数
    current_page = pagination.page  # 当前页码

    return render_template('index.html',items=items,total_pages=total_pages, current_page=current_page)

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
