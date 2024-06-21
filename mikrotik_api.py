import os
from librouteros import connect
import ssl

# Disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_info(username):
    connection = connect(
        username=API_USER,
        password=API_PASSWORD,
        host=API_HOST,
        ssl_wrapper=ssl_context.wrap_socket
    )

    for user in connection('/tool/user-manager/user/print'):
        if user['username'] == username:
            return user

    return None
