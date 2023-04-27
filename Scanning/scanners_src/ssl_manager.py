import ssl
from cert_gen import CERT_FILE, KEY_FILE


class SslManager:
    def __init__(self):
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.load_cert_chain(CERT_FILE, KEY_FILE)

    @property
    def context(self):
        return self.ssl_context


ssl_manager = SslManager()
