# -*- coding: utf-8 -*-

from socket_class import Sockets
from shortcuts import ShortCuts
import _multiprocessing
from subprocess import Popen, PIPE
import re
import socket

MAC_REGULAR_EXPRESSION = '([a-fA-F0-9]{2}[:|\-]?){6}'
IP_REGULAR_EXPRESSION = '192.168.1.(\d){1,3}'
MAC_FILTER = ['ff-ff-ff-ff-ff-ff', 'ff-ff-ff-ff-ff-fa']
IP_FILTER = ['192.168.1.1']
PING_QUESTION_LIST_OF_ELEMENT = ['ping', '-an', '', '&&', 'echo', 'T', '||', 'echo', 'F']

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8820


class Server():
    def __init__(self):
        self.__shortcut_builder = ShortCuts()
        self.__server_socket = Sockets()
        self.__client_socket = Sockets()
        self.__server_socket.open_server(SERVER_IP, SERVER_PORT)
        print 'server is up'
        self.open_server()

    def open_server(self):
        self.__client_socket, client_address = self.__server_socket.client_connection()

    def receive_information_from_client(self):
        data = self.__server_socket.read_from_client(self.__client_socket)
        return data.split('$$')

    def pass_information_to_client(self, data):
        self.__server_socket.write_to_client(data, self.__client_socket)

    def make_the_shortcut_file(self, action, sequence, argument):
        self.__shortcut_builder.get_user_previous_activity()
        self.__shortcut_builder.set_users_choice(action)
        self.__shortcut_builder.set_shortcut_sequence(sequence)
        self.__shortcut_builder.write_new_shortcut(argument)
        self.__shortcut_builder.save_user_activity()


    def activate_the_shortcut_on_the_computer(self):
        pass


class Client():
    def __init__(self):
        self.__client_socket = Sockets()
        self.__computer_information = {}
        self.__raw_computer_information = []

    def connect_to_server(self, ip, port):
        try:
            self.__client_socket.connect_to_server(ip, port)
            return True
        except socket.error, e:
            print e
            return False

    def receive_information_from_the_server(self):
        data = self.__client_socket.read_from_server()
        return data

    def send_request_to_the_server(self, action, sequence, argument):
        data_to_send = action+'$$'+sequence+'$$'+argument
        self.__client_socket.write_to_server(data_to_send)

    def activate_the_shortcut_on_the_computer(self):
        pass

    def find_computers_in_the_network(self):
        arp_question = Popen(['arp', '-a'], stdout=PIPE)
        result = arp_question.communicate()[0]
        result_split_lines = [line.strip() for line in result.splitlines()]  # split the arp answer to lines

        for line in result_split_lines:
            mac_finder = re.search(MAC_REGULAR_EXPRESSION, line)
            ip_finder = re.search(IP_REGULAR_EXPRESSION, line)
            if mac_finder and ip_finder:
                if mac_finder.group(0).lower() not in MAC_FILTER and ip_finder.group(0) not in IP_FILTER:
                    print line.split()[:2]
                    self.__raw_computer_information.append(line.split()[:2])

        for computer in self.__raw_computer_information:
            computer_name, ping_result = self.find_computer_name_and_find_if_pinging(computer[0])
            if ping_result == 'T':
                self.__computer_information[computer_name] = computer

        del self.__raw_computer_information[:]  # clear raw computer information
                                                # ip and mac
        print self.__computer_information


    def find_computer_name_and_find_if_pinging(self, computer_ip):
        ping_arg_list = PING_QUESTION_LIST_OF_ELEMENT
        ping_arg_list[2] = computer_ip
        ping_question = Popen(ping_arg_list, stdout=PIPE, shell=True)
        result = ping_question.communicate()[0]
        result_split_lines = [line.strip() for line in result.splitlines()]  # split the arp answer to lines

        print result_split_lines[1].split()[1], '---name---'
        print result_split_lines[-1], '---ping---'
        return result_split_lines[1].split()[1], result_split_lines[-1]

    def check_if_remote_server_is_on(self, server_ip):
        if self.connect_to_server(server_ip, SERVER_PORT):
            print 'connection was successful'
            return True
        else:
            print 'connection failed'
            return False

    def add_computer_information_to_data_base(self):
        pass

    def change_computer_name(self):
        pass



def main():
    # client = Client()
    # client.find_computers_in_the_network()
    # if client.check_if_remote_server_is_on('192.168.1.46'):
    #     client.send_request_to_the_server('open', 'a+f', 'google.com')
    #     print client.receive_information_from_the_server()

    server = Server()
    a = server.receive_information_from_client()
    print a
    server.make_the_shortcut_file(a[0], a[1], a[2])
    server.pass_information_to_client('ok')




if __name__ == '__main__':
    main()