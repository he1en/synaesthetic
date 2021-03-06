from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session
import json
from unittest.mock import patch
import spotify_api


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test homepage"""

        result = self.client.get("/")
        self.assertIn(b"Synaesthetic", result.data)


    def test_login(self):
        """Test redirect of login route"""

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 302)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    # def test_users_list(self):
    #     """Test departments page."""

    #     result = self.client.get("/users")
    #     self.assertIn(b"test", result.data)

    # def test_departments_details(self):
    #     """Test departments page."""

    #     result = self.client.get("/department/fin")
    #     self.assertIn(b"Phone: 555-1000", result.data)

class SpotifyAPI(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # # Get the Flask test client
        # self.client = app.test_client()
        #app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables
        db.create_all()


    @patch('spotipy.Spotify')
    def test_user_artists(self, sp):

        token = "kfsdf"
        user_id = "123"

        with open('top_artists.json') as f:
            data = json.load(f)

        sp.return_value.current_user_top_artists.return_value = data

        response = spotify_api.user_artists(token, user_id)

        print(sp.call_args)

        assert response == "Success"

        


class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = "test"


    def test_api_artists(self):
        """Test response from /api/artists route"""

        result = self.client.get("/api/artists")
        self.assertEqual(result.status_code, 200)


    def test_api_audio(self):
        """Test response from /api/audio route"""

        result = self.client.get("/api/audio")
        self.assertEqual(result.status_code, 200)

    def test_data_page(self):
        """Test response from /my-data route"""

        result = self.client.get("/my-data")
        self.assertEqual(result.status_code, 200)

#     def test_important_page(self):
#         """Test important page."""

#         result = self.client.get("/important")
#         self.assertIn(b"You are a valued user", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn(b"You are a valued user", result.data)
#         self.assertIn(b"You must be logged in", result.data)


# class FlaskTestsLogInLogOut(TestCase):  # Bonus example. Not in lecture.
#     """Test log in and log out."""

#     def setUp(self):
#         """Before every test"""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_login(self):
#         """Test log in form.

#         Unlike login test above, 'with' is necessary here in order to refer to session.
#         """

#         with self.client as c:
#             result = c.post('/login',
#                             data={'user_id': '42', 'password': 'abc'},
#                             follow_redirects=True
#                             )
#             self.assertEqual(session['user_id'], '42')
#             self.assertIn(b"You are a valued user", result.data)

#     def test_logout(self):
#         """Test logout route."""

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = '42'

#             result = self.client.get('/logout', follow_redirects=True)

#             self.assertNotIn(b'user_id', session)
#             self.assertIn(b'Logged Out', result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
