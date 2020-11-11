import os
import time
import subprocess

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

FIREBASE_SECRET_PATH = os.environ['FIREBASE_SECRET_PATH']
FIREBASE_DATABASE_URL = os.environ['FIREBASE_DATABASE_URL']
OPENJTALK_HTSVOICE_PATH = os.environ['OPENJTALK_HTSVOICE_PATH']

cred = credentials.Certificate(FIREBASE_SECRET_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_DATABASE_URL,
})

messagesRef = db.reference('messages')


def on_message_updated(event: db.Event):
    if event.data is None:
        return

    messages = event.data
    print('New Message coming.')

    for key, message in messages.items():
        post_user = message.get('from', {})
        userid = post_user.get('aadObjectId')
        username = post_user.get('name')

        text = message.get('text')

        subprocess.run([ 'play', '/sounds/opening.mp3' ])

        p = subprocess.Popen([ 'open_jtalk', '-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic', '-m', OPENJTALK_HTSVOICE_PATH, '-r', '1.0', '-ow', '/dev/stdout' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        sound, _ = p.communicate(text.encode('utf-8'))

        p = subprocess.Popen([ 'play', '-' ], stdin=subprocess.PIPE)
        p.communicate(sound)

        print(message)
        
        messagesRef.child(key).delete()
        print(f'Message ${key} deleting')

        subprocess.run([ 'play', '/sounds/closing.mp3' ])
        

if __name__ == '__main__':
    print('start listening')
    messagesRef.listen(on_message_updated)

    while True:
        time.sleep(0.1)

