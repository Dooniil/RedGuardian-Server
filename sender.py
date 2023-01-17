from singleton_decorator import singleton
import socket


@singleton
class Sender:
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_controller(self, host: str, port: int):
        if 1024 <= port <= 65535:
            self.__client.connect_ex((host, port))
            print('Connected')
        else:
            # TODO: Write User's exception
            raise Exception

    def send_req(self, req):
        self.__client.send(req.__str__().encode('UTF-8'))

    def close_session(self):
        self.__client.close()
        print('Closed')

    def open_session(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #  for WITH
    # def __enter__(self):
    #     if not self.__client:
    #         self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     return self.__client
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     try:
    #         self.__client.close()
    #         print('Closed')
    #     except Exception as e:
    #         print(e)
    #         return True

