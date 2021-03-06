# -*- encoding=UTF-8 -*-
from nowsgram import app, db
from flask import render_template, redirect, request, flash, get_flashed_messages, send_from_directory
from models import Image, User
import random
import hashlib
import json
import uuid
import os
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>/')
def image(image_id):
    image1 = Image.query.get(image_id)
    if image1 is None:
        return redirect('/')
    return render_template('pageDetail.html', image=image1)


@app.route('/profile/<int:user_id>/')
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    if user is None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=3, per_page=3, error_out=False)
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    maps = {'has_next': paginate.has_next}
    images = []
    for img in paginate.items:
        imginfo = {'id': img.id, 'url': img.url, 'comment_count': len(img.comments)}
        images.append(imginfo)
    maps['images'] = images
    return json.dumps(maps)


@app.route('/regloginpage/')
def regloginpage():
    if current_user.is_authenticated:
        return redirect('/')
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))


def redirect_with_msg(target, msg, category):
    if msg is not None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/login/', methods={'get', 'post'})
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()
    user = User.query.filter_by(username=username).first()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名和密码不能为空', 'reglogin')

    if user is None:
        return redirect_with_msg('/regloginpage/', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update(password+user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/regloginpage/', u'密码错误', 'reglogin')

    login_user(user)
    n = request.values.get('next')
    if n is not None and n.startswith('/'):
        return redirect(n)

    return redirect('/')


@app.route('/reg/', methods={'get', 'post'})
def reg():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名和密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()
    if user is not None:
        return redirect_with_msg('/regloginpage/', u'用户名已经存在', 'reglogin')

    # 更多判断
    salt = '.'.join(random.sample('0123456789abcdefghiABCDEFGHI', 10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()
    user = User(username, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    n = request.values.get('next')
    if n is not None and n.startswith('/'):
        return redirect(n)
    return redirect('/')


@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


def save_to_local(file, file_name):
    save_dir = app.config['UPLOAD_DIR']
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name


@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)


@app.route('/upload', methods={"post"})
def upload():
    file = request.files['file']
    file_ext = ''
    if file.filename.find('.') > 0:
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '')+'.'+file_ext
        url = save_to_local(file, file_name)
        if url is not None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)


