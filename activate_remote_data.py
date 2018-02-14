# -*- coding: utf-8 -*-

import sys
from subprocess import *
from new_computer_class import *


def main():
    action = sys.argv[1]
    argument = sys.argv[2]
    mac = sys.argv[3]

    arp_question = Popen(['python', 'get_ip_and_mac.py', mac], stdout=PIPE)
    result = arp_question.communicate()[0].strip()
    ip = result.split('$$')[0]

    client = Client()
    client.connect_to_server(ip, SERVER_ACTING_PORT)
    client.send_request_to_the_server(action, argument)

    with open('a.txt', 'w') as f:
        f.write(client.receive_information_from_the_server())

    client.close_client()



if __name__ == '__main__':
    main()