import os
from librouteros import connect

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_info(username):
    # Split host and port if provided
    host, port = (API_HOST.split(':') + [None])[:2]
    port = int(port) if port else 8728  # Default port is 8728

    try:
        # Connect to MikroTik router
        connection = connect(
            username=API_USER,
            password=API_PASSWORD,
            host=host,
            port=port,
        )

        # Find user by username
        users = connection('/user-manager/user/print', **{'?name': username})
        if users:
            user_id = users[0].get('.id')
            if user_id:
                # Fetch user profile information
                user_profile_info = connection('/user-manager/user-profile/print', **{'?user': user_id})
                if user_profile_info:
                    return user_profile_info[0]

    except Exception as e:
        print(f"Error fetching user profile information: {e}")

    return None
