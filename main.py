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
    import oauth, daddy
except ImportError:
    sys.exit('error: import failed for one or more modules')

def main():
    #
    # script execution
    #
    classroom = oauth.auth(scopes=oauth.SCOPES, creds='token.pickle')

try:
    if __name__ == '__main__':
        main()
    else:
        raise RuntimeError('error: this module cannot be loaded from another one')
except RuntimeError:
    print_exc()