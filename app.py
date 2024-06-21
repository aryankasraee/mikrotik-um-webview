import logging
from flask import Flask, request, render_template
from mikrotik_api import get_user_info

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_account():
    username = request.form['username']
    logger.debug(f"Checking account for username: {username}")
    user_info = get_user_info(username)
    logger.debug(f"User info returned: {user_info}")
    if user_info:
        return render_template('result.html', user_info=user_info)
    else:
        return render_template('result.html', error="User not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)