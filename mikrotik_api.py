import os
from librouteros import connect
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_info(username):
    # Split host and port if provided
    host, port = (API_HOST.split(':') + [None])[:2]
    port = int(port) if port else 8728  # Default port is 8728

    logger.info(f"Attempting to connect to {host}:{port} with user {API_USER}")

    try:
        connection = connect(
            username=API_USER,
            password=API_PASSWORD,
            host=host,
            port=port,
        )
        logger.info("Connected successfully to MikroTik router")

        # Fetch user information
        users = list(connection('/user-manager/user/print', **{'?name': username}))
        
        if not users:
            logger.warning(f"User '{username}' not found")
            return None

        user = users[0]
        user_id = user.get('.id')

        # Fetch user profile information
        user_profiles = list(connection('/user-manager/user-profile/print', **{'?user': user_id}))
        
        if not user_profiles:
            logger.warning(f"Profile for user '{username}' not found")
            return None

        user_profile = user_profiles[0]

        # Merge user and user profile information
        user_info = {
            'user': username,
            'profile': user_profile.get('profile'),
            'state': user_profile.get('state'),
            'end-time': user_profile.get('end-time')
        }

        logger.info(f"Successfully retrieved info for user '{username}'")
        return user_info

    except Exception as e:
        logger.error(f"Error in get_user_info: {e}", exc_info=True)
        return None

# Example usage
if __name__ == "__main__":
    username_to_check = input("Enter username to check: ")

    user_info = get_user_info(username_to_check)
    if user_info:
        print(f"Account Info for '{username_to_check}':")
        for key, value in user_info.items():
            print(f"  {key}: {value}")
    else:
        print(f"User '{username_to_check}' not found or an error occurred.")