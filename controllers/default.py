import os, json
from plugin_ractive import ractive, Form
from osutils import get_files

auth.data = {
    'user':auth.user, 
    'links':
        {'sign_in':URL('user/login'), 
         'sign_out':URL('user/logout'), 
         'profile':URL('user/profile'), 
         'lost_password':URL('user/request_reset_password'), 
         'lost_username':URL('user/retrieve_username'), 
         'change_password':URL('user/change_password')}}

@ractive
def index():
    return dict(auth = auth.data)

def user():
    response.delimiters = ('{%', '%}')
    return dict(form=auth())

@ractive
def files():
    files = get_files(path=request.folder)
    alerts = []
    user = {'first_name':'Massimo'}
    form = request.forms.get('0')
    if form:
        # save file
        filename = os.path.abspath(os.path.join(request.folder, form['filename']))
        if filename.startswith(request.folder):
            bytes = form.get('bytes')
            if bytes is not None:
                open(filename, 'w').write(bytes)
    # open file
    bytes = None
    filename = None
    if request.vars.filename:
        filename = os.path.join(request.folder, request.vars.filename)
        if os.path.exists(filename):
            if os.path.getsize(filename)<1e6:
                bytes = open(filename).read()
                filename = filename[len(request.folder):]
                try:
                    json.dumps(bytes)
                except:
                    bytes = None
                    alerts.append({'info':'File is not a text file'})
            else:
                alerts.append({'info':'File is too large'})
        else:
            alerts.append({'error':'File does not exist'})
    return dict(menu = files, user=user, alerts=alerts, 
                forms = [dict(bytes=bytes, filename=filename)], 
                auth = auth.data)

@ractive
def form():
    alerts = []
    print request.forms.get('0')
    form = Form(db.thing,15).process(request.forms.get('0'))
    if form.errors: alerts.append({'error':'Invalid form'})
    table = db(db.thing).select().xml() # this should move to JS too
    return dict(forms = [form], table = table, alerts = alerts, auth = auth.data)

@ractive
def markmin():
    bytes = open(os.path.join(request.folder, 'private', 'example.mm2')).read()
    return dict(forms = [{'filename':'example', 'bytes':bytes}], auth = auth.data)

@ractive
def tree():
    tree = [{'name':'root',
            'children':[
            {'name':'a'},
            {'name':'b', 'link':'http://google.com'}]
            }]
    return dict(tree = tree, auth = auth.data)
