from sender import Sender


def send_data(data):
    sender = Sender(8999)
    sender.send_req(data)

