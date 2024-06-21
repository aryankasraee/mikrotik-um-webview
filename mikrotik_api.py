import os
from librouteros import connect

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_info(username):
    # Split host and port if provided
    host, port = (API_HOST.split(':') + [None])[:2]
    port = int(port) if port else 8728  # Default port is 8728

    # Connect without SSL for port 8728
    connection = connect(
        username=API_USER,
        password=API_PASSWORD,
        host=host,
        port=port,
        # Remove ssl_wrapper argument for non-SSL connection
    )

    for user in connection('/tool/user-manager/user/print'):
        if user['username'] == username:
            return user

    return None
