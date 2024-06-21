from librouteros import connect
import ssl

# Disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def get_user_info(username):
    connection = connect(
        username='api_user', 
        password='api_password',
        host='192.168.88.1',
        ssl_wrapper=ssl_context.wrap_socket
    )

    for user in connection('/tool/user-manager/user/print'):
        if user['username'] == username:
            return user

    return None
