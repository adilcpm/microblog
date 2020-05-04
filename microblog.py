from app import create_app, db
from app.models import User, Post, Messages, Notification, Chats


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post,
        'Messages': Messages,'Notifcation' : Notification, 'Chats' : Chats}
