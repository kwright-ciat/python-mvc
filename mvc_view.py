#!bin/python
'''
Presents a MVC View to client 

Only communicates with the Controller and presents View to client.
'''
from urllib import parse
import cgi
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import io
import traceback

from mvc_app import ip_default, port_default, testing
import mvc_controller

class SimpleHandler(BaseHTTPRequestHandler):
    ''' Handler for both POST and GET requests '''        

    def do_POST(self):
        ''' Parse the form data posted for fields '''
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # Begin the response
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        
        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        if testing:
            out.write('Client: {}\n'.format(self.client_address))
            out.write('User-agent: {}\n'.format(
                self.headers['user-agent']))
            out.write('Path: {}\n'.format(self.path))
            
            out.write('Form data:\n')
    
            # Echo back information about what was posted in the form
            for field in form.keys():
                field_item = form[field]
                # Regular form value
                out.write('\t{}={}\n'.format(
                field, form[field].value))
                if field_item.filename:
                    # The field contains an uploaded file
                    file_data = field_item.file.read()
                    file_len = len(file_data)
                    del file_data
    
                    out.write(
                        '\tUploaded {} as {!r} ({} bytes)\n'.format(
                            field, field_item.filename, file_len)
                    )
                else:
                    # Regular form value
                    out.write('\t{}={}\n'.format(
                        field, form[field].value))

        # Disconnect our encoding wrapper from the underlying
        # buffer so that deleting the wrapper doesn't close
        # the socket, which is still being used by the server.
        parsed_path = parse.urlparse(self.path)
        endpoint = parsed_path.path
        data = mvc_controller.post_endpoints(fields, endpoint)
        out.write(data)
        out.detach()
        
        #

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        if testing:
            message_parts = [
                'CLIENT VALUES:',
                'client_address={} ({})'.format(
                    self.client_address,
                    self.address_string()),
                'command={}'.format(self.command),
                'path={}'.format(self.path),
                'real path={}'.format(parsed_path.path),
                'query={}'.format(parsed_path.query),
                'request_version={}'.format(self.request_version),
                '',
                'SERVER VALUES:',
                'server_version={}'.format(self.server_version),
                'sys_version={}'.format(self.sys_version),
                'protocol_version={}'.format(self.protocol_version),
                '',
                'HEADERS RECEIVED:',
            ]
            message_parts.append('\r\n')
            for name, value in sorted(self.headers.items()):
                message_parts.append(
                    '{}={}'.format(name, value.rstrip())
                )
            message_parts = '\r\n'.join(message_parts) 
        else:
            message_parts = '\r\n'
        endpoint = parsed_path.path
        data = mvc_controller.get_endpoints(endpoint)
        if not data:
            data = 'No records found.'

        message_title = 'Project Tasks\n\n'
        message = '\r\n'.join(('endpoint', endpoint, message_parts, message_title, data, '\r\n'))
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

        
def start_server(ip=ip_default, port=port_default):
    ''' 
    Function to start server
    
    Once the server starts, then the program blocks.
    '''
    
    print('Starting server, use <Ctrl-C> to stop')
    try:
        server = HTTPServer((ip, port), SimpleHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print ('\nStopping server, goodbye!')
    except OSError:
        # OSError: [WinError 10049] The requested address is not valid in its context
        print('Requested address is not valid in its context')
    except Exception:
        print('Printing Traceback: Unhandled Exception occurred\n')
        traceback.print_exc()
    else:
        pass
    finally:
        pass

if __name__ == '__main__':
    start_server(ip_default, port_default)
