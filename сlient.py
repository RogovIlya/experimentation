import socket
import time


class ClientError (Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.socket = socket.create_connection(host, port, timeout or 10)

    def get(self, key):
        response = {}
        if key:
            command = "get {0}\n".format(key)
            self.socket.send(command.encode())
            resp = self.socket.recv(1024)
            if "error\nwrong command\n\n" in resp.decode():
                raise ClientError("Error from server")
            # print(resp)
            list = resp.decode().replace("ok\n", "").split("\n")
            for l in list:
                l.replace("\n", "")

            # print(list)

            for s in [l.split(" ") for l in list if len(l) != 0]:
                if s[0] in response:
                    response[s[0]].append((int(s[2]), float(s[1])))
                else:
                    response[s[0]] = [(int(s[2]), float(s[1]))]

            for k, v in response.items():
                response[k] = sorted(v, key=lambda x: x[0])

            # print(response)

        else:
            raise ClientError("Key is None or empty")

        return response

    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def put(self, key, value, timestamp=None):
        if key and value and self.is_float(value):
            command = "put {0} {1} {2}\n".format(key, float(value), timestamp or str(int(time.time())))
            self.socket.send(command.encode())
            resp = self.socket.recv(1024).decode().strip('\n')
            if resp != "ok" or resp == "errorwrong command":
                raise ClientError("Error from server")
            # else:
            #     print(resp)
        else:
            raise ClientError("Args is None")

