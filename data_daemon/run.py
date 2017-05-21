
import json
import sys, os
import socket
import time
import zmq

context = zmq.Context()


def get_uid():
    ip = socket.gethostbyname(socket.gethostname())
    pid = os.getpid()
    now = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    uid_str = 'IP:{} PROC:{} SINCE:{}'.format(ip, pid, now)
    return uid_str


def conn_init(config):
    master_socket = context.socket(zmq.DEALER)
    master_socket.connect("tcp://{}:{}".format(config['master'], config['port']))
    return master_socket


def load_configs(fname):
    with open(fname, 'r') as f:
        config = json.load(f)
    return config


def handle_msg(msg_json, master_socket):
    pass


def run():
    config = load_configs('/Users/brian/Desktop/School/2016-2017/CMSC33520/PriorityStore/config.json')
    uid = get_uid()

    master_socket = conn_init(config)
    master_socket.send_string(u''.format(uid))
    # master_socket.send_json({
    #     'src': uid,
    #     'dst': 'master',
    #     'cmd': 'HELLO',
    # })
    #
    # master_socket.send_json({'hello':None})
    #
    # while True:
    #     msg = master_socket.recv_json()
    #     handle_msg(msg, master_socket)


if __name__ == '__main__':
    run()





