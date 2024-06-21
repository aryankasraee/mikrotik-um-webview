import os
from librouteros import connect

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_info(username):
    # Split host and port if provided
    host, port = (API_HOST.split(':') + [None])[:2]
    port = int(port) if port else 8728  # Default port is 8728

    connection = connect(
        username=API_USER,
        password=API_PASSWORD,
        host=host,
        port=port,
    )

    try:
        # Execute '/user-manager/user/print' command to list all users
        users = connection('/user-manager/user/print')

        for user in users:
            if user.get('name') == username:
                return user

    except Exception as e:
        print(f"Error: {e}")

    return None

# Example usage
if __name__ == "__main__":
    # Example of retrieving username dynamically (e.g., from user input or web form)
    username_to_check = input("Enter username to check: ")

    user_info = get_user_info(username_to_check)
    if user_info:
        print(f"Account Info for '{username_to_check}':")
        for key, value in user_info.items():
            print(f"  {key}: {value}")
    else:
        print(f"User '{username_to_check}' not found.")