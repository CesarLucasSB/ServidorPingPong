import socket
import sys # Importa sys para sys.exit()

HOST = '127.0.0.1'  # O endereço do servidor
PORT = 65432        # A porta que o servidor está escutando
BUFFER_SIZE = 8192  # Deve ser igual ou maior que o do servidor

def start_client():
    print(f"[*] Cliente iniciando. Conectando a {HOST}:{PORT}")
    print("Digite 'sair' ou 'exit' para encerrar a conexão.")

    try:
        # Cria um socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Conecta ao servidor
            s.connect((HOST, PORT))
            print(f"[*] Conectado ao servidor em {HOST}:{PORT}")

            while True:
                # O cliente entra com a mensagem
                message_to_send = input("Sua mensagem > ")
                
                # Verifica se o usuário quer sair
                if message_to_send in ('QUIT'):
                    print("[*] Encerrando o cliente...")
                    break # Sai do loop e fecha a conexão
                
                if not message_to_send:
                    print("[!] Mensagem vazia não será enviada.")
                    continue # Volta para o início do loop sem enviar

                # Envia a mensagem para o servidor
                # LINHA CORRIGIDA AQUI
                print(f'[+] Enviando: "{message_to_send}"')
                s.sendall(message_to_send.encode('utf-8')) # Codifica a string para bytes
                
                # Recebe a resposta do servidor
                data = s.recv(BUFFER_SIZE)
                echoed_message = data.decode('utf-8') # Decodifica os bytes para string
                # LINHA CORRIGIDA AQUI
                print(f'[-] Recebido (eco): "{echoed_message}"')
                
                # Verifica a integridade da mensagem
                if message_to_send == echoed_message:
                    print(f'    Verificação de integridade: OK!')
                else:
                    # LINHA CORRIGIDA AQUI
                    print(f'    Verificação de integridade: FALHA! Esperado "{message_to_send}", Recebido "{echoed_message}"')
                
        print("[*] Conexão encerrada.")

    except ConnectionRefusedError:
        print(f"[!] Erro: Conexão recusada. Certifique-se de que o servidor está rodando em {HOST}:{PORT}.")
    except Exception as e:
        print(f"[!] Ocorreu um erro: {e}")
    finally:
        # Garante que o programa saia limpo
        sys.exit(0) 

if __name__ == "__main__":
    start_client()