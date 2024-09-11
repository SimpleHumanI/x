import http.server
import socketserver
import subprocess as sp
import http.client

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Get the content length to read the body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8').strip()
        print(f"Received raw data: {post_data}")

        # Extract the command from the POST request
        command = post_data
        print(f"Extracted command: {command}")

        # Execute the command and capture the output
        try:
            cmd_output = sp.check_output(command, shell=True, stderr=sp.STDOUT)
            cmd_output = cmd_output.decode('utf-8')  # Decode bytes to string

            # Send the command output to another HTTP server
            self.send_output_to_http_server(cmd_output)

            # Send a response back to the client
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(cmd_output)))
            self.end_headers()
            self.wfile.write(cmd_output.encode('utf-8'))
            print("Command executed successfully and output sent to HTTP server.")
        except sp.CalledProcessError as e:
            error_message = f"Error executing command: {e.output.decode('utf-8')}"
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(error_message)))
            self.end_headers()
            self.wfile.write(error_message.encode('utf-8'))
            print("Error executing command.")

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(error_message)))
            self.end_headers()
            self.wfile.write(error_message.encode('utf-8'))
            print("An unexpected error occurred.")

    def send_output_to_http_server(self, data):
        # Send the output to the HTTP server running on localhost:5000
        conn = http.client.HTTPConnection("127.0.0.1", 5000)
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': str(len(data))
        }
        
        conn.request("POST", "/", body=data, headers=headers)
        response = conn.getresponse()
        print(f"Response from HTTP server: {response.status} {response.reason}")
        response_data = response.read()
        print(f"Response data: {response_data.decode('utf-8')}")
        conn.close()

def run(server_class=http.server.HTTPServer, handler_class=MyRequestHandler, port=12345):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()


