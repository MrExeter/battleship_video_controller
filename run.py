'''
Description - Run App
@author - John Sentz
@date - 01-Mar-2018
@time - 2:05 PM
'''


from app import create_app, db
from app.auth.models import User


if __name__ == '__main__':
    flask_app = create_app('dev')
    with flask_app.app_context():
        db.create_all()

        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry',
                             email='harry@potters.com',
                             password='secret')

    flask_app.run()

