import os
import time
import subprocess

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

FIREBASE_SECRET_PATH = os.environ['FIREBASE_SECRET_PATH']
FIREBASE_DATABASE_URL = os.environ['FIREBASE_DATABASE_URL']

OPENJTALK_HTSVOICE_PATH = os.environ.get('OPENJTALK_HTSVOICE_PATH')

SPEECH_ENABLED = os.environ.get('SPEECH_ENABLED', '1') == '1'

PERSON_SOUND_ENABLED = os.environ.get('PERSON_SOUND_ENABLED', '0') == '1'

STATIC_SPEECH_ENABLED = os.environ.get('STATIC_SPEECH_ENABLED', '0') == '1'
STATIC_SPEECH_TEXT = os.environ.get('STATIC_SPEECH_TEXT')

if (SPEECH_ENABLED or STATIC_SPEECH_ENABLED) and not os.path.exists(OPENJTALK_HTSVOICE_PATH):
    raise Exception(f'HTS Voice not found at {OPENJTALK_HTSVOICE_PATH}')


cred = credentials.Certificate(FIREBASE_SECRET_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_DATABASE_URL,
})

messagesRef = db.reference('messages')



def play_speech(text):
    print(f'playing speech: {text}')
    
    p = subprocess.Popen([ 'open_jtalk', '-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic', '-m', OPENJTALK_HTSVOICE_PATH, '-r', '1.0', '-ow', '/dev/stdout' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    sound, _ = p.communicate(text.encode('utf-8'))

    p = subprocess.Popen([ 'play', '-' ], stdin=subprocess.PIPE)
    p.communicate(sound)

def play_sound(path):
    print(f'playing sound at {path}')
    subprocess.run([ 'play', path ])

def play_person_sound(user_id):
    sound_path = os.path.join('/sounds/person/', os.path.basename(user_id) + '.mp3')

    if not os.path.exists(sound_path):
        print(f'Person Sound not found at {sound_path}')
        return
    
    play_sound(sound_path)


def on_message_updated(event: db.Event):
    if event.data is None:
        return

    print('Message updated.')
    print(f'Path: {event.path}')
    
    if event.path == '/': # / == /messages
        messages = event.data
    elif len(event.path.split('/')) == 2: # /MESSAGE_KEY == /messages/MESSAGE_KEY
        key = os.path.basename(event.path)
        messages = { key: event.data }
    else:
        print('Ignored (c.z. minor change).')
        return
    
    message_count = len(messages.items())
    print(f'Message Count: {message_count}')
    print(messages)

    for key, message in messages.items():
        print(message)

        post_user = message.get('from', {})
        user_id = post_user.get('aadObjectId')
        username = post_user.get('name')

        text = message.get('text')

        play_sound('/sounds/opening.mp3')
         
        if PERSON_SOUND_ENABLED:
            play_person_sound(user_id)

        if SPEECH_ENABLED:
            play_speech(text)
        
        if STATIC_SPEECH_ENABLED:
            play_speech(STATIC_SPEECH_TEXT)
        
        messagesRef.child(key).delete()
        print(f'Message {key} deleting')

        play_sound('/sounds/closing.mp3')

    print('All Messages proceeded.')
        

if __name__ == '__main__':
    print('start listening')
    messagesRef.listen(on_message_updated)

    while True:
        time.sleep(0.1)

