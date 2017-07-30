# export PYTHONPATH=/usr/local/lib/python2.7/site-packages:$PYTHONPATH
import os
from flask import Flask, request, redirect, url_for, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import subprocess
import SimpleHTTPServer
import SocketServer
import webbrowser
from threading import Thread

UPLOAD_FOLDER = 'uploads/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print 'starting uploading'
        # delete
        old_files = os.listdir(app.config['UPLOAD_FOLDER'])


        for file in old_files:
            if file.endswith(".jpg") or file.endswith('png') or file.endswith('jpeg'):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

        # check if the post request has the file part
        if 'file' not in request.files:
            response = jsonify(message='No file part')
            response.status_code = 422
            return response

        uploaded_files = request.files.getlist('file')
        print len(uploaded_files)
        if len(uploaded_files) == 0:
            return jsonify(message='no files uploaded')
        # save new
        for file in uploaded_files:
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print 'saved ' + file.filename

        sfm_and_serve('uploads')

        return "Done"
    return render_template('index.html')

def sfm_and_serve(dir):
    subprocess.call(['bin/opensfm_run_all', dir])
    thread = Thread(target=viz_server, args=(dir,))
    thread.start()
    print 'viz thread finished'

def viz_server(dir):
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "serving at port", PORT
    print 'http://localhost:8000/viewer/reconstruction.html#file=/' + dir + '/reconstruction.meshed.json'
    httpd.serve_forever()
    webbrowser.open_new_tab('http://localhost:8000/viewer/reconstruction.html#file=/' + dir + '/reconstruction.meshed.json')
