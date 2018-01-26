#-*- encoding=UTF-8 -*-
from flask import Flask, render_template, request, make_response, redirect, flash, get_flashed_messages

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'
app.secret_key = 'nowcoder'
@app.route('/index/')
@app.route('/')
def index():
    res = ''
    for msg, category in get_flashed_messages(with_categories = True):
        res = res + category +msg + '<br>'
    res = res + 'hello'
    return res

@app.route('/profile/<int:uid>/',methods = ['GET','POST'])
def profile(uid):
    colors = ('red', 'green')
    dict = {'nowcoder':'abc','google':'def'}
    return render_template('profile.html',uid = uid,colors = colors,infos = dict)

@app.route('/request')
def request_demo():
    key = request.args.get('key','defaultkey')
    res = request.args.get('key','defaultkey') + '<br>'
    res = res + request.url +'++'+ request.path + '<br>'
    for property in dir(request):
        res = res +str(property) + '<br>' + str(eval('request.'+ property)) + '<br>'

    respones = make_response(res)
    respones.set_cookie('nowcoderid', key)
    respones.status = '404'
    respones.headers['nowcoder'] = 'hello'
    return respones

@app.route('/newpath')
def newpath():
    return 'newpath'

@app.route('/re/<int:code>')
def redirect_demo(code):
    return redirect('/newpath',code = code)

@app.errorhandler(400)
def exception_page(e):
    response = make_response('出错啦@！！')
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html',url = request.url ),404

@app.route('/admin')
def admin():
    key = request.args.get('key')
    if key == 'admin':
        return 'hello admin'
    else:
        raise Exception()

@app.route('/login')
def login():
    app.logger.info('log success')
    flash('登录成功','info')
    return 'ok'
    #return redirect('/')

@app.route('/log/<level>/<msg>/')
def log(level, msg):
    res = ''
    dict = {'warn':logging.WARN, 'error':logging.ERROR, 'info':logging.INFO}
    if dict.has_key(level):
        res += level
        app.logger.log(dict[level], msg)
    return 'logged:' + res + msg

def set_logger():
    info_file_handler = RotatingFileHandler('F:\\dev\\log\\info.txt')
    info_file_handler.setLevel(logging.INFO)
    app.logger.addHandler(info_file_handler)

    warn_file_handler = RotatingFileHandler('F:\\dev\\log\\warn.txt')
    warn_file_handler.setLevel(logging.WARN)
    app.logger.addHandler(warn_file_handler)

    error_file_handler = RotatingFileHandler('F:\\dev\\log\\error.txt')
    error_file_handler.setLevel(logging.ERROR)
    app.logger.addHandler(error_file_handler)


if __name__ == '__main__':
    set_logger()
    app.run(debug=True)
