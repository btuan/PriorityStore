
import pprint
import json
import threading
import zmq

context = zmq.Context()
p = pprint.PrettyPrinter(indent=4)


class ServerTask(threading.Thread):
    def __init__(self, config):
        self.config = config
        threading.Thread.__init__(self)

    def run(self):
        frontend = context.socket(zmq.ROUTER)
        frontend.bind("tcp://*:{}".format(self.config['port']))

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(self.config['num_workers']):
            worker = ServerWorker()
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        worker = context.socket(zmq.DEALER)
        worker.connect('inproc://backend')

        while True:
            ident, msg = worker.recv_multipart()
            reply = handle_msg(msg)
            if reply is not None:
                worker.send_multipart([ident, msg])


def load_configs(fname):
    with open(fname, 'r') as f:
        config = json.load(f)
        return config


def create_file(fname, data, node=None):
    pass


def delete_file(fname):
    pass


def retrieve_file(fname):
    pass


def list_files():
    pass


def handle_msg(msg):
    p.pprint(msg)
    return msg


def run():
    config = load_configs('/Users/brian/Desktop/School/2016-2017/CMSC33520/PriorityStore/config.json')
    server = ServerTask(config)
    server.run()

    # while True:
    #     msg = socket.recv_json()
    #     handle_msg(msg, socket)


if __name__ == '__main__':
    run()
