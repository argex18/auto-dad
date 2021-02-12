from traceback import print_exc
import oauth

class CallbackNotFoundError(Exception):
    """Exception raised for errors in input callback in __get__()

    Attributes:
        invalid_callback: str
    """

    def __init__(self, invalid_callback):
        self.invalid_callback = None
        try:
            if not isinstance(invalid_callback, str):
                raise TypeError()
            self.invalid_callback = f'error: not found {invalid_callback} in the service resources'
        except Exception:
            print_exc()
    
    def __get__(self):
        try:
            if self.invalid_callback:
                return self.invalid_callback
            else:
                raise AttributeError()
        except Exception:
            print_exc()
    
    def __set__(self, invalid_callback):
        try:
            if isinstance(invalid_callback, str):
                self.invalid_callback = f'error: not found {invalid_callback} in the service resources'
            else:
                raise TypeError()
        except Exception:
            print_exc()
        

def get(service, callback, *args):
    try:
        if not isinstance(callback, str):
            raise TypeError('error: callback must be of type str')

        resources = [
            'service',
            'courses()',
            'invitations()',
            'registrations()',
            'userProfiles()',
            'aliases()',
            'announcements()',
            'courseWork()',
            'courseWorkMaterials()',
            'students()',
            'teachers()',
            'topics()'
        ]

        subclasses = callback.split('.')
        method = subclasses.pop()
        for subclass in subclasses:
            flag = False
            if subclass in resources:
                flag = True
            else:
                break

        if flag:
            callback = f"{'.'.join(subclasses)}.{method}"
        else:
            raise CallbackNotFoundError(callback)

        if args:
            args = ','.join(args)
            return eval(f"{callback}({args}).execute()")
        else:
            return eval(f"{callback}().execute()")
    except CallbackNotFoundError as cnf:
        print( cnf.__get__() )
    except Exception:
        print_exc()

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

def get_announcements(service, *course_names):
    announcements = []
    try:
        #
        # get_announcements() function
        #
        courses = get(service, 'service.courses().list', 'studentId="me"')
        names = list( map(lambda course: course['name'], courses['courses']) )
        i = 0
        while i < len(names):
            names[i] = names[i].replace(' ', '').lower() 
            i+=1
        del i
        ids = list( map(lambda course: course['id'], courses['courses']) )
        names_ids = dict( zip(names,ids) )
        
        for course_name in course_names:
            course_name = course_name.replace(' ', '').lower()
            if course_name in names:
                course_id = names_ids[course_name]
                announcements.append( get(service, 'service.courses().announcements().list', f'courseId={course_id}') )
            else:
                raise Exception(f'error: {course_name} not found in the course names')
                break
            
    except Exception:
        print_exc()
    finally:
        return announcements   

"""
def t_01(service):
    request = service.courses().courseWorkMaterials().list(courseId='158451300703')
    results = request.execute()
    return results
"""

"""
service = oauth.auth(oauth.SCOPES, 'token.pickle')

if __name__ == '__main__':
    #
    # courses
    #
    results = t_01(service)
    for result in results:
        print(result)
    #
    # materials
    #
    materials = t_01(service)
    print( materials )
""" 
service = oauth.auth(oauth.SCOPES, 'token.pickle')
if __name__ == '__main__':
    announcements = get_announcements(service, 'Istituzioni di Diritto privato', 'Informatica (Economia)')
    for announcement in announcements:
        print(announcement)