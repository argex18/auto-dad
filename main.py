"""

In this module will be executed the main script.

"""

try:
    import sys
except ImportError:
    print('error: import error for sys module...killing script execution')
    __name__ = None

try:
    from traceback import print_exc
    import oauth
except ImportError:
    sys.exit('error: import failed for one or more modules')

def main():
    #
    # script execution
    #
    classroom = oauth.auth(scopes=oauth.SCOPES, creds=None, secrets='client_secrets.json')
    courses = oauth.get_courses(classroom)

    # test 1.1
    # test of the get function
    # test 1.1
    if not courses:
        print('No courses found.')
    else:
        print('Courses:')
        for course in courses:
            print(course['name'])

try:
    if __name__ == '__main__':
        main()
    else:
        raise RuntimeError('error: this module cannot be loaded from another one')
except RuntimeError:
    print_exc()