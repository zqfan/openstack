import socket

import msgpack

PORT = 6666
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
listen_addr = ("", PORT)
udp_socket.bind(listen_addr)

# Report on all data packets received and
# where they came from in each case (as this is
# UDP, each may be from a different source and it's
# up to the server to sort this out!)
while True:
    data, addr = udp_socket.recvfrom(1024)
    print addr,
    try:
        data = msgpack.loads(data, encoding='utf-8')
    except:
        pass
    finally:
        print data
