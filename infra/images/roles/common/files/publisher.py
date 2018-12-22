import socket
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, help="Port to handle")
args = parser.parse_args()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("", int(args.port)))
serversocket.listen(999)
while True:
    conn, addr = serversocket.accept()
    # sleep(1)
    try:
        conn.shutdown(socket.SHUT_RDWR)
    except socket.error as e:
        print "Shit happened:\n{}".format(e)
    conn.close()
