# -*- encoding=UTF-8 -*-

from nowsgram import app, db
from flask_script import Manager
from nowsgram.models import User, Image, Comment
import random
manager = Manager(app)


def get_image_url():
    return'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'


@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('User'+str(i+1), 'a'+str(i+1)))
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i+1))
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(k), 1+3*i+j, i+1))
    for j in range(0, 7):
        db.session.add(Image(get_image_url(), 100))
    db.session.commit()
    for i in range(50, 100, 2):
        user = User.query.get(i)
        user.username = '[New1]' + user.username
    db.session.add(Image(get_image_url(), i + 1))
    for i in range(50, 100, 2):
        comment = Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()

    print User.query.all()
    print User.query.get(3)
    print User.query.filter_by(id=5).first_or_404()
    print User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print User.query.order_by(User.id.desc()).all()
    print User.query.filter(User.username.endswith('0')).limit(3).all()
    print User.query.paginate(page=1, per_page=10).items
    user = User.query.get(1)

    print user.images
    image = Image.query.get(1)
    print image, image.user


if __name__ == '__main__':
    manager.run()
