import os
from librouteros import connect
import logging

logger = logging.getLogger(__name__)

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_connection():
    host, port = (API_HOST.split(':') + [None])[:2]
    port = int(port) if port else 8728
    return connect(username=API_USER, password=API_PASSWORD, host=host, port=port)

def get_user_info(username):
    logger.info(f"Fetching info for user: {username}")
    
    try:
        with get_connection() as connection:
            # Fetch all users
            users = list(connection('/user-manager/user/print'))
            logger.debug(f"Retrieved {len(users)} users")
            
            # Find the specific user
            user = next((u for u in users if u.get('name').lower() == username.lower()), None)
            
            if not user:
                logger.warning(f"User '{username}' not found")
                return None

            logger.debug(f"User found: {user}")
            
            # Extract relevant information from the user object
            user_info = {
                'user': username,
                'state': 'Enabled' if user.get('disabled') == 'false' else 'Disabled',
                'shared-users': user.get('shared-users', 'Unknown'),
                'end-time': user.get('end-time', 'Unknown'),
                'group': user.get('group', 'Unknown')
            }
            
            logger.info(f"Successfully retrieved info for user '{username}'")
            return user_info
    except Exception as e:
        logger.error(f"Error in get_user_info: {e}", exc_info=True)
        return None

# For testing
if __name__ == "__main__":
    username_to_check = input("Enter username to check: ")
    user_info = get_user_info(username_to_check)
    if user_info:
        print(f"Account Info for '{username_to_check}':")
        for key, value in user_info.items():
            print(f"  {key}: {value}")
    else:
        print(f"User '{username_to_check}' not found or an error occurred.")