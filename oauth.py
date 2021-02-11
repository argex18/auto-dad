from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from requests_oauthlib import OAuth2Session
from google.auth.transport.requests import Request
from traceback import print_exc

#
# default scopes in case client_secrets.json not valid
#
SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.announcements'
]

def auth(scopes, creds=None, secrets=None):
    service = None
    try:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh( Request() )
            else:
                if secrets == None:
                    socket = InstalledAppFlow.from_client_secrets_file( 'client_secrets.json', scopes )
                else:
                    socket = InstalledAppFlow.from_client_secrets_file( secrets, scopes )
                
                socket.redirect_uri = 'http://localhost:50790/'
                # pass localhost as argument to avoid uri redirect mismatch
                creds = socket.run_local_server(host='localhost', port=50790)
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as t:
                    pickle.dump(creds, t)
        # Starting the service when creds valid
        with open('token.pickle', 'rb') as t:
            creds = pickle.load(t)
        service = build('classroom', 'v1', credentials=creds)
    except Exception:
        print_exc()
    finally:
        return service
        
def get_courses(service):
    courses = []
    try:
        results = service.courses().list(pageSize=10).execute()
        courses = results.get('courses', [])
    except Exception:
        courses = None
        print_exc()
    finally:
        return courses
