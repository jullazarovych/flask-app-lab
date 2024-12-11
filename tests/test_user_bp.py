import unittest
from app import create_app, db
from flask import url_for
from app.users.models import User

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_greetings_page(self):
        response = self.client.get("/users/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get("/users/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            test_user = User(username='testuser', email='test@example.com', password='password')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    def test_register_page_loads(self):
        with self.app.test_request_context():
            response = self.client.get('/users/register')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Реєстрація'.encode('utf-8'), response.data)

    def test_login_page_loads(self):
        with self.app.test_request_context():
            response = self.client.get('/users/login')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Login', response.data)



class UserRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        registration_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }

        response = self.client.post('/users/register', data=registration_data, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your account has been created!'.encode('utf-8'), response.data)

        with self.app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'newuser')


class UserLoginLogoutTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            test_user = User(username='testuser', email='testuser@example.com', password='password123')
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_login(self):
        login_data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }

        response = self.client.post('/users/login', data=login_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Login successful!'.encode('utf-8'), response.data)
        with self.client:
            response = self.client.get('/users/account')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'testuser', response.data)

    def test_user_logout(self):
        login_data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }

        self.client.post('/users/login', data=login_data, follow_redirects=True)
        response = self.client.get('/users/logout', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('You have successfully logged out'.encode('utf-8'), response.data)

        response = self.client.get('/users/account', follow_redirects=True)
        self.assertIn('Please log in to access this page.'.encode('utf-8'), response.data)

if __name__ == "__main__":
    unittest.main()
