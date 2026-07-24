import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app


def test_username_and_email_are_normalized_for_signup_and_login():
    conn = sqlite3.connect(app.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    conn.commit()
    conn.close()

    created = app.register_user(' TestUser ', ' Test@Example.com ', 'secret123')
    assert created is True

    user = app.login_user('testuser', 'secret123')
    assert user is not None
    assert user[1] == 'TestUser'

    existing = app.check_email_exists('test@example.com')
    assert existing is not None
    assert existing['email'] == 'test@example.com'
