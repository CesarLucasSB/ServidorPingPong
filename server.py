import socket
import threading

HOST = '127.0.0.1'  # Endereço IP do localhost
PORT = 65432        # Porta arbitrária não privilegiada (> 1023)
BUFFER_SIZE = 8192  # Aumentei o buffer para mensagens potencialmente maiores

def handle_client(conn, addr):
    print(f"[*] Conexão aceita de {addr}")
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            
            message = data.decode('utf-8')
            # LINHA CORRIGIDA AQUI
            print(f'[{addr}] Recebido: "{message}"') # Usando aspas simples para a f-string e aspas duplas literais
            
            conn.sendall(data)
            # LINHA CORRIGIDA AQUI
            print(f'[{addr}] Ecoado: "{message}"') # Usando aspas simples para a f-string e aspas duplas literais
            
    except ConnectionResetError:
        print(f"[*] Cliente {addr} desconectou abruptamente.")
    except Exception as e:
        print(f"[*] Erro no tratamento do cliente {addr}: {e}")
    finally:
        print(f"[*] Fechando conexão com {addr}")
        conn.close()

def start_server():
    print(f"[*] Iniciando servidor Echo TCP em {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("[*] Servidor escutando por conexões...")
        
        while True:
            conn, addr = s.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, addr))
            client_handler.start()

if __name__ == "__main__":
    start_server()