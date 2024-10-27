import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type

user_list = [{
    'id': 1,
    'first_name': 'Jan',
    'last_name': 'Soliński',
    'role': 'instructor'
}]
id_counter = 2  

class SimpleRequestHandler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(user_list).encode())

    def do_POST(self) -> None:
        global id_counter  
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        user_id = id_counter
        response = {
            "id": user_id,
            "first_name": received_data['first_name'],
            "last_name": received_data['last_name'],
            "role": received_data['role']
        }
        id_counter += 1  

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

        user_list.append(response)

    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        user_id = received_data['id'] 
        user_to_delete = next((user for user in user_list if user["id"] == user_id), None)

        if user_to_delete:
            user_list.remove(user_to_delete)
            self.send_response(200)
            response = {"status": "User deleted successfully."}
        else:
            self.send_response(404)
            response = {"status": "User not found."}

        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def run(server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000) -> None:
    server_address: tuple = ('', port)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
