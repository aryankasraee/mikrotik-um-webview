import os
from librouteros import connect

API_USER = os.getenv('API_USER')
API_PASSWORD = os.getenv('API_PASSWORD')
API_HOST = os.getenv('API_HOST')

def get_user_profile_info(username):
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
        # Execute '/user-manager/user/print' command to find user
        users = connection('/user-manager/user/print')

        for user in users:
            if user.get('name') == username:
                # Fetch user profile information from user-profiles menu
                user_profile_info = connection('/user-manager/user-profile/print',
                                               **{'?user': user['.id']})
                if user_profile_info:
                    return user_profile_info[0]  # Assuming only one profile per user

    except Exception as e:
        print(f"Error: {e}")

    return None

# Example usage
if __name__ == "__main__":
    # Example of retrieving username dynamically (e.g., from user input or web form)
    username_to_check = input("Enter username to check: ")

    user_profile_info = get_user_profile_info(username_to_check)
    if user_profile_info:
        user = user_profile_info.get('user', '')
        profile = user_profile_info.get('profile', '')
        state = user_profile_info.get('state', '')
        end_time = user_profile_info.get('end-time', '')

        print(f"User: {user} Profile: {profile} State: {state} End Time: {end_time}")
    else:
        print(f"No user profile information found for '{username_to_check}'.")
