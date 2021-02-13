from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from traceback import print_exc

#
# default scopes in case client_secrets.json not valid
#
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.guardianlinks.students',
    'https://www.googleapis.com/auth/classroom.profile.photos',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.announcements'
]

def auth(scopes, creds=None, secrets=None):
    service = None
    credentials = None
    exceptions = []
    n_exc = 0
    try:
        if creds and not isinstance(creds, str):
            raise TypeError('error: creds must be a path to a .pickle file')

        if creds and os.path.exists(creds):
            # Starting the service when creds valid
            with open(creds, 'rb') as t:
                credentials = pickle.load(t)
        elif creds and not os.path.exists(creds):
            exceptions.append( FileNotFoundError('error: the creds .pickle file was not found in the provided path') )

        # Starting the service when not creds valid
        if not creds or not credentials or not credentials.valid:
            if creds and credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh( Request() )
            else:
                if secrets == None:
                    socket = InstalledAppFlow.from_client_secrets_file( 'client_secrets.json', scopes )
                else:
                    socket = InstalledAppFlow.from_client_secrets_file( secrets, scopes )
                
                socket.redirect_uri = 'http://localhost:50790/'
                # pass localhost as argument to avoid uri redirect mismatch
                credentials = socket.run_local_server(host='localhost', port=50790)
                # Save the credentials for the next run
                if not creds:
                    with open('token.pickle', 'wb') as t:
                        pickle.dump(credentials, t)
                else:
                    with open(creds, 'wb') as t:
                        pickle.dump(credentials, t)
        service = build('classroom', 'v1', credentials=credentials)
    except Exception:
        print_exc()
    finally:
        if len(exceptions) != 0:
            while n_exc < len(exceptions):
                print( exceptions[n_exc].args[0] )
                n_exc += 1
        return service