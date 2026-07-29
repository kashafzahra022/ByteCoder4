import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app


def test_username_and_email_are_normalized_for_signup_and_login():
    conn = sqlite3.connect(app.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM pending_registrations')
    conn.commit()
    conn.close()

    created = app.register_user(None, ' Test@Example.com ', 'secret123')
    assert created is True

    user = app.login_user('test@example.com', 'secret123')
    assert user is not None
    assert user[2] == 'test@example.com'

    existing = app.check_email_exists('test@example.com')
    assert existing is not None
    assert existing['email'] == 'test@example.com'


def test_pending_registration_requires_valid_otp_before_account_is_created():
    conn = sqlite3.connect(app.DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    cursor.execute('DELETE FROM pending_registrations')
    cursor.execute('DELETE FROM otp_codes')
    conn.commit()
    conn.close()

    assert app.save_pending_registration('victim@example.com', 'secret123', 'Victim User') is True
    assert app.check_email_exists('victim@example.com') is None
    assert app.login_user('victim@example.com', 'secret123') is None

    app.save_otp('victim@example.com', '111111')
    assert app.complete_pending_registration('victim@example.com', '000000') is False
    assert app.check_email_exists('victim@example.com') is None

    assert app.complete_pending_registration('victim@example.com', '111111') is True
    user = app.login_user('victim@example.com', 'secret123')
    assert user is not None
    assert user[2] == 'victim@example.com'
