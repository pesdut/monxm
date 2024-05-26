import socket
import json
import time
import threading
import struct
import random
import binascii
from colorthon import Colors as Fore
import pyrx  # Ensure you have pyrx installed: pip install pyrx

# Define your Monero address
address = "YOUR_MONERO_ADDRESS"

soloxminer = '''
                            ███████╗ ██████╗ ██╗      ██████╗
                            ██╔════╝██╔═══██╗██║     ██╔═══██╗
                            ███████╗██║   ██║██║     ██║   ██║
                            ╚════██║██║   ██║██║     ██║   ██║
                            ███████║╚██████╔╝███████╗╚██████╔╝
                            ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝

                            ███╗   ███╗██╗███╗   ██╗███████╗██████╗
                            ████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
                            ██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
                            ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
                            ██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
                            ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
'''

mmdrza = '''
                   |======================================================|
                   |=========== ╔╦╗╔╦╗╔╦╗╦═╗╔═╗╔═╗ ╔═╗╔═╗╔╦╗  ============|
                   |=========== ║║║║║║ ║║╠╦╝╔═╝╠═╣ ║  ║ ║║║║  ============|
                   |=========== ╩ ╩╩ ╩═╩╝╩╚═╚═╝╩ ╩o╚═╝╚═╝╩ ╩  ============|
                   |------------------------------------------------------|
                   |- WebSite ------------------------------- Mmdrza.Com -|
                   |- GiTHUB  ---------------------- Github.Com/PyMmdrza -|
                   |- MEDIUM  -------------- PythonWithMmdrza.Medium.Com -|
                   |======================================================|
'''

print(Fore.RED, soloxminer, Fore.RESET)
print(Fore.YELLOW, mmdrza, Fore.RESET)
inpAdd = input(f'{Fore.MAGENTA}[*]{Fore.RESET}{Fore.WHITE} INSERT YOUR MONERO WALLET ADDRESS FOR WITHDRAWAL{Fore.RESET} : ')
address = str(inpAdd)
print(f'\n{Fore.GREY}Monero Wallet Address{Fore.RESET} ===>> {Fore.MAGENTA}{address}{Fore.RESET}')
print(f"{Fore.GREY}{'-' * 66}{Fore.RESET}")

time.sleep(3)

# Function to handle the mining process
def MoneroMiner():
    print('[*] Monero Miner Started')

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('pool.hashvault.pro', 7777))
    except socket.gaierror as e:
        print(f"Error connecting to pool: {e}")
        return

    login = {
        "method": "login",
        "params": {
            "login": address,
            "pass": "x",
            "agent": "xmr-stak/2.10.7"
        },
        "id": 1
    }

    sock.sendall(json.dumps(login).encode('utf-8') + b'\n')

    response = json.loads(sock.recv(1024).decode('utf-8'))
    job = response['result']['job']
    job_id = job['job_id']
    target = job['target']
    blob = job['blob']

    def hash_to_hex(hash):
        return binascii.hexlify(hash).decode('utf-8')

    def randomx_hash(blob, nonce):
        # Example usage of pyrx for RandomX hashing
        return pyrx.get_rx_hash(blob + nonce)

    while True:
        nonce = struct.pack('I', random.randint(0, 2**32 - 1))
        blob_bytes = binascii.unhexlify(blob)
        hashed_blob = randomx_hash(blob_bytes, nonce)
        result = hash_to_hex(hashed_blob)

        if int(result, 16) < int(target, 16):
            print('[*] New block mined')
            submit = {
                "method": "submit",
                "params": {
                    "id": response['result']['id'],
                    "job_id": job_id,
                    "nonce": binascii.hexlify(nonce).decode('utf-8'),
                    "result": result
                },
                "id": 1
            }
            sock.sendall(json.dumps(submit).encode('utf-8') + b'\n')

            response = sock.recv(1024).decode('utf-8')
            print(response)
            break

# Main function to start the miner
if __name__ == '__main__':
    MoneroMiner()
