import os
from librouteros import connect
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more detailed logs
logger = logging.getLogger(__name__)

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_info(username):
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

        # Fetch all users
        users = list(connection('/user-manager/user/print'))
        logger.debug(f"Retrieved {len(users)} users")
        
        # Find the user with matching username
        user = next((u for u in users if u.get('name').lower() == username.lower()), None)
        
        if not user:
            logger.warning(f"User '{username}' not found")
            return None

        user_id = user.get('.id')
        logger.debug(f"Found user: {user}")

        # Fetch all user profiles
        user_profiles = list(connection('/user-manager/user-profile/print'))
        logger.debug(f"Retrieved {len(user_profiles)} user profiles")
        
        # Find the profile for the user
        user_profile = next((p for p in user_profiles if p.get('user') == user_id), None)
        
        if not user_profile:
            logger.warning(f"Profile for user '{username}' not found")
            # If profile not found, return available user information
            return {
                'user': username,
                'profile': 'Not found',
                'state': user.get('state', 'Unknown'),
                'end-time': user.get('end-time', 'Unknown')
            }

        # Merge user and user profile information
        user_info = {
            'user': username,
            'profile': user_profile.get('profile', 'Unknown'),
            'state': user_profile.get('state', 'Unknown'),
            'end-time': user_profile.get('end-time', 'Unknown')
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