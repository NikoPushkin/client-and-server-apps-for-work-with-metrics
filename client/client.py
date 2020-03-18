import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        try:
            self.client_socket = socket.create_connection((self.host, self.port), self.timeout)
        except:
            raise ClientError()

    @staticmethod
    def _handle_response(response):
        my_dict = {}
        for i in response[1:]:
            pair_of_data = i.split()
            key = pair_of_data[0]
            metric = float(pair_of_data[1])
            timestamp = int(float(pair_of_data[2]))

            if len(pair_of_data) != 3:
                raise ClientError()

            elif key not in my_dict:
                vals = [(timestamp, metric)]
                new_dict = {key: vals}
                my_dict.update(new_dict)

            else:
                new_vals = [(timestamp, metric)]
                my_dict[key] += new_vals
                my_dict[key].sort(key=lambda x:x[0])

        if my_dict == {}:
            raise ClientError()
        else:
            return my_dict

    def get(self, name):
        self.client_socket.sendall("get {}\n".format(name).encode("utf8"))
        response = self.client_socket.recv(1024).decode('utf8').split('\n')

        final_list = response[0:-2]
        try:
            if final_list[0] == 'ok':
                if len(final_list) <= 1:
                    return {}
                else:
                    data = Client._handle_response(final_list)
                    return data
            else:
                raise ClientError()
        except:
            raise ClientError()

    def put(self, metric, value, timestamp=None):
        try:
            if timestamp == None:
                self.client_socket.sendall("put {} {} {}\n".format(metric, value, int(time.time())).encode("utf8"))
                response = self.client_socket.recv(1024).decode('utf8').split('\n')
            else:
                self.client_socket.sendall("put {} {} {}\n".format(metric, value, timestamp).encode("utf8"))
                response = self.client_socket.recv(1024).decode('utf8').split('\n')

            if response[0] != "ok":
                raise ClientError()
        except:
            raise ClientError()

a = Client('localhost', 5000)
