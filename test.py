import subprocess
import SimpleHTTPServer
import SocketServer
import webbrowser

TEST_DIR = 'berlin'

if __name__ == '__main__':
    subprocess.call(['bin/opensfm_run_all', 'data/' + TEST_DIR])
    PORT = 8000

    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)

    print "serving at port", PORT
    httpd.serve_forever()
    webbrowser.open('http://localhost:8000/viewer/reconstruction.html#file=/data/' + TEST_DIR + '/reconstruction.meshed.json', new=2))
