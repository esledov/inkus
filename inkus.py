#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
from mako.lookup import TemplateLookup
from mako import exceptions
import threading
import sys

try:
    # for python 3
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:
    # for python 2
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer as HTTPServer

HTTP_STATUS_OK = 200
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# add current folder to system path
sys.path.insert(0, os.getcwd())

imports = []

try:
    # you can use mysite module to hold global variables
    import mysite
    imports.append('import mysite')
except ImportError:
    print('Please create module mysite.py to keep global vars!')

lookup = TemplateLookup(
            directories=['.'],
            input_encoding='utf-8',
            output_encoding='utf-8',
            encoding_errors='replace',
            imports = imports
        )


class StoppableHTTPServer(HTTPServer):
    """HTTPServer that can be interrupted by pressing Ctrl-C"""
    def run(self):
        (hostaddr, port) = self.socket.getsockname()
        print("Serving HTTP on {} port {} ...".format(hostaddr, port))
        h = '127.0.0.1' if hostaddr == '0.0.0.0' else hostaddr
        print("Open http://{}:{} in your browser!".format(h, port))
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            # Clean-up server (close socket, etc.)
            self.server_close()
            sys.exit(0)


class MakoHandler(SimpleHTTPRequestHandler):
    """When .htm file is requested, looks for mako file
    with the same name, renders it and serves it instead"""

    def do_GET(self):
        """Serve a GET request."""

        serve_index_mako = self.serve_index_mako()

        # shutdown the server by visiting /killme page
        # Ctrl-C from the same thread does not work so good
        if self.path.startswith('/killme'):
            def killme(server):
                server.shutdown()
            self.log_message('Stopping server')
            threading.Thread(
                    target=killme,
                    args=(httpd,)
            ).start()
            self.send_error(HTTP_STATUS_INTERNAL_SERVER_ERROR)
            return

        # if path does't end with html extension,
        # serve it in a normal way
        if not (serve_index_mako or self.path.endswith('.htm')):
            return SimpleHTTPRequestHandler.do_GET(self)

        # if path ends with htm extension
        # find appropriate .mako file and render it
        if serve_index_mako:
            # it is a directory with index.mako file inside
            sep = '' if self.path.endswith('/') else '/'
            fname = self.path + sep + 'index.mako'
        else:
            # replace .htm extension for .mako
            fname = self.path[:-4] + '.mako'

        self.log_message("rendering %s template", fname)

        try:

            template = lookup.get_template(fname)

            # CURRENT_URI is passed to the template
            # more parameters can be added if necessary
            html = template.render(CURRENT_URI=self.path)

        except exceptions.TopLevelLookupException:
            self.send_error(
                HTTP_STATUS_NOT_FOUND,
                "Template not found (%s)" % fname)
            return
        except:

            # show detailed rendering error description
            html = exceptions.html_error_template().render()

        if not html: return # nothing to show here

        # if it is unicode, convert it to utf-8
        # if isinstance(html, str):
        #     html = html.encode('utf-8')

        self.send_response(HTTP_STATUS_OK)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(html))
        self.end_headers()
        self.wfile.write(html)

    def serve_index_mako(self):
        """If index.mako is present in a directory,
        serve it instead of a directory listing"""

        path = self.translate_path(self.path)

        # not a directory
        if not os.path.isdir(path):
            return False

        # if index.html exists in directory,
        # show it rather than index.mako
        index_path = os.path.join(path, 'index.html')
        if os.path.exists(index_path):
            return False

        index_path = os.path.join(path, 'index.mako')
        return os.path.exists(index_path)


if __name__ == '__main__':
    httpd = StoppableHTTPServer(('', 8000), MakoHandler)
    httpd.run()