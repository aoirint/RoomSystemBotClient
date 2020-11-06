import os
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

FIREBASE_SECRET_PATH = os.environ['FIREBASE_SECRET_PATH']
FIREBASE_DATABASE_URL = os.environ['FIREBASE_DATABASE_URL']

cred = credentials.Certificate(FIREBASE_SECRET_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_DATABASE_URL,
})


def on_message_updated(event: db.Event):
    if event.data is None:
        return

    message = event.data
    print(message)

if __name__ == '__main__':
    messages = db.reference('messages')
    
    print('start listening')
    messages.listen(on_message_updated)

    while True:
        time.sleep(0.1)

