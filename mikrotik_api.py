import logging
from librouteros import connect

logger = logging.getLogger(__name__)

def get_user_info(username, connection):
    logger.info(f"Fetching info for user: {username}")
    
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

# Usage in your main script
def main():
    # Set up connection parameters
    API_USER = os.getenv('API_USER')
    API_PASSWORD = os.getenv('API_PASSWORD')
    API_HOST = os.getenv('API_HOST')
    
    host, port = (API_HOST.split(':') + [None])[:2]
    port = int(port) if port else 8728

    try:
        with connect(username=API_USER, password=API_PASSWORD, host=host, port=port) as connection:
            username_to_check = input("Enter username to check: ")
            user_info = get_user_info(username_to_check, connection)
            
            if user_info:
                print(f"Account Info for '{username_to_check}':")
                for key, value in user_info.items():
                    print(f"  {key}: {value}")
            else:
                print(f"User '{username_to_check}' not found.")
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)

if __name__ == "__main__":
    main()