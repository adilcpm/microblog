from flask import session
from flask_login import current_user
from app.models import Chats, Messages, User
from flask_socketio import join_room
from app import db,socketio

@socketio.on('send message')
def handleMessage(msg):
    temp_chat = session['chat_session'][0] #Hold value of session at this stage, for use down below
    if(temp_chat == 'None'):
        # no chat is allocated, so create a new chat
        this_chat = Chats(user1=current_user.id,user2=session['chat_session'][1])
        session['chat_session'][0] == this_chat.id
        db.session.add(this_chat)
    else: 
        # if chat was already there, load the chat
        this_chat = Chats.query.get(session['chat_session'][0])
    msg = Messages(author=current_user, recipient=this_chat.other(current_user.id),
                      body=msg,chat_session=this_chat)
    reciever = User.query.get(session['chat_session'][1])
    reciever.add_notification('unread_chats',reciever.unread_chats())
    db.session.add(msg)
    db.session.commit()
    if(temp_chat == 'None'): #if first message, refresh the page to load chat session properly
        socketio.emit('refresh')
    json_msg = {
        'body' : msg.body,
        'author' : current_user.username
    }
    socketio.emit('receive message',json_msg, room=session['chat_session'][0])


@socketio.on('connect')
def handleConnect():
    join_room(session['chat_session'][0])
    current_user.online = True
    db.session.commit()
    socketio.emit('online', current_user.username)

@socketio.on('disconnect')
def handleDisconnect():
    current_user.online = False
    db.session.commit()
    socketio.emit('offline', current_user.username)

@socketio.on('typing')
def typing(user):
    socketio.emit('typed',user,room=session['chat_session'][0])

@socketio.on('read msg')
def readmsg():
    Chats.query.get(session['chat_session'][0]).last_msg().reciever_read = True
    current_user.add_notification('unread_chats',current_user.unread_chats())
    db.session.commit()
