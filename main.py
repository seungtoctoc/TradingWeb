from collections import UserDict
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SECRET_KEY'] = "secret"
db = SQLAlchemy(app)

# static 폴더로 경로 설정
app.config['UPLOAD_FOLDER'] = '/Users/code_rosie/desktop/coding/py/static/'


class User_class(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    u_id = db.Column(db.String(20))
    u_pw = db.Column(db.String(20))
    u_name = db.Column(db.String(20))
    u_following = []
    
    def __init__(self, id, pw, nm):
        self.u_id = id
        self.u_pw = pw
        self.u_name = nm
        
    def AddFollowing(self, id):
        self.u_following.append(id)
        
    def removeFollowing(self, id):
        self.u_following.remove(id)

    
    
class Product_class(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, autoincrement = True)
    p_name = db.Column(db.String(50))
    p_price = db.Column(db.String(50))
    p_sale = db.Column(db.String(50))
    p_id = db.Column(db.String(50))
    p_info = db.Column(db.String(200))
    p_img = db.Column(db.String(200))
    
    def __init__(self, name, price, sale, id, info, img):
        self.p_name = name
        self.p_price = price
        self.p_sale = sale
        self.p_id = id
        self.p_info = info
        self.p_img = img

    def edit(self, name, price, sale, id, info, img):
        self.p_name = name
        self.p_price = price
        self.p_sale = sale
        self.p_id = id
        self.p_info = info
        self.p_img = img


    def soldout(self):
        self.p_sale = "판매 완료"
        
    def soldin(self):
        self.p_sale = "판매중"

# main식으로 세션 유무에 따라서 1이나 2로 연결!
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return redirect(url_for('search', word = request.form['search']))
    else:
        if 'username' in session:
            username = session['username']
            product_query = Product_class.query.all()
            return render_template('main2.html', username = username, product_query = product_query)
        else:
            product_query = Product_class.query.all()
            return render_template('main.html', product_query = product_query)

@app.route('/search/<word>', methods=['GET', 'POST'])
def search(word):
    if request.method == 'POST':
        return redirect(url_for('search', word = request.form['search']))
    else:    
        result = Product_class.query.filter(Product_class.p_name.like("%"+word+"%"))
        if 'username' in session:
            return render_template('search2.html', username = session['username'], result=result)
        else:
            return render_template('search.html', result=result)
        
        
        
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))



@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method=='POST':
        if not request.form['id'] or not request.form['pw'] or not request.form['nm']:
           flash('Please enter all the fields', 'error')
        else:
            user = User_class(request.form['id'], request.form['pw'], request.form['nm'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('sign.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if not request.form['id'] or not request.form['pw']:
            flash('Please enter all the fields', 'error')
        else:
            inputId = request.form['id']
            inputPw = request.form['pw']
            data = User_class.query.filter_by(u_id = inputId, u_pw = inputPw).first()
            if data is not None:
                session['username'] = inputId
                return redirect(url_for('main'))
            else:
                return render_template('login.html')
            
    return render_template('login.html')


@app.route('/test')
def test():
    return render_template('test.html', user_query = User_class.query.all(), product_query = Product_class.query.all())


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method=='POST':
        if not request.form['name'] or not request.form['price'] or not request.form['info'] or not request.files['file']:
            flash('Please enter all the fields', 'error')
        else:
            name=request.form['name']
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            
            
            product = Product_class(name, request.form['price'], "판매중", session['username'], request.form['info'], secure_filename(f.filename))
            db.session.add(product)
            db.session.commit()
            
            return redirect(url_for('main'))
    return render_template('upload.html', username = session['username'])


@app.route('/detail/<p_name>', methods=['GET', 'POST'])
def detail(p_name):
    if request.method == 'POST':
        return redirect(url_for('search', word = request.form['search']))
    else:
        result = Product_class.query.filter_by(p_name = p_name).first()
        if 'username' in session:
            username = session['username']
            result_user = User_class.query.filter_by(u_id = session['username']).first()
            return render_template('detail2.html', username = username, result = result, result_user = result_user)
        else:
            return render_template('detail.html', result = result)
        
        
@app.route('/delete/<p_name>')
def delete(p_name):
    result = Product_class.query.filter_by(p_name = p_name).first()
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('test'))

@app.route('/following')
def following():
    result = User_class.query.filter_by(u_id = session['username']).first()
    # followingList = result.u_following
    return render_template('following.html', username = session['username'], result=result, product_query = Product_class.query.all())


@app.route('/follow/<id>')
def follow(id):
    result = User_class.query.filter_by(u_id = session['username']).first()
    result.AddFollowing(id)
    db.session.commit()
    return redirect(url_for('following'))

@app.route('/unfollow/<id>')
def unfollow(id):
    result = User_class.query.filter_by(u_id = session['username']).first()
    result.removeFollowing(id)
    db.session.commit()
    return redirect(url_for('following'))

@app.route('/soldout/<p_name>')
def soldout(p_name):
    result = Product_class.query.filter_by(p_name=p_name).first()
    result.soldout()
    db.session.commit()
    return redirect(url_for('detail', p_name = p_name))

@app.route('/soldin/<p_name>')
def soldin(p_name):
    result = Product_class.query.filter_by(p_name=p_name).first()
    result.soldin()
    db.session.commit()
    return redirect(url_for('detail', p_name = p_name))

@app.route('/edit/<p_name>', methods=['GET', 'POST'])
def edit(p_name):
    result = Product_class.query.filter_by(p_name=p_name).first()
    if request.method=='POST':
        if not request.form['name'] or not request.form['price'] or not request.form['info'] or not request.files['file']:
            flash('Please enter all the fields', 'error')
        else:
            name=request.form['name']
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            
            result.edit(name, request.form['price'], result.p_sale, session['username'], request.form['info'], secure_filename(f.filename))
            db.session.commit()
            
            return redirect(url_for('main'))
    return render_template('edit.html', username = session['username'], result=result)







@app.route('/selling', methods=['GET', 'POST'])
def selling():
    if request.method == 'POST':
        return redirect(url_for('search', word = request.form['search']))
    else:
        return render_template('selling.html', username = session['username'], product_query = Product_class.query.all())


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5050)