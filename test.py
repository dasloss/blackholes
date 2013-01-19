import unittest, flask
from app import app, User, views, login_manager

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.init_db()

    def init_db(self):
        user = User(name='The Donor',username='donor',password='donor',
                    email='donor@gmail.com',address='123 Main Street', 
                    city='Palo Alto',state='CA',zip='94024',employer='Intel',
                    occupation='Technician',service='local',authenticated=True)
        user.save()

    def tearDown(self):
        from pymongo import Connection
        conn = Connection()
        conn.drop_database(app.config['DB'])
        # How do I delete the collections?
        
    def register(self, name, username, password, email, confirm):
        return self.app.post('/register/', data=dict(
                name=name, username=username,
                password=password, confirm=confirm,
                email=email
                ), follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/login/', data=dict(
                username=username,
                password=password
                ), follow_redirects=True)
    
    def logout(self):
        return self.app.get('/logout/', follow_redirects=True)
   
    def test_about(self):
        rv = self.app.get('/about/')
        assert rv.status_code == 200
    
    def test_login(self):
        rv=self.login('donor','donor')
        assert "You logged in successfully." in rv.data
        self.logout()
        rv=self.login('notauser','passwd')
        assert "There was an error logging in, user not found." in rv.data
        rv=self.login('donor','wrongpass')
        assert "There was an error logging in, password incorrect." in rv.data
      
    def test_index(self):
        rv = self.app.get('/', follow_redirects=True)
        assert "Please log in to access this page." in rv.data
        rv = self.login('donor','donor')
        assert rv.status_code == 200
      
    def test_register_logout(self):
        rv=self.register('The User','user','users','user@gmail.com','users')
        assert "You successfully registered." in rv.data
        rv=self.logout()
        assert "You logged out successfully." in rv.data
        rv=self.register('Another donor','donor','newpass','new@gmail.com','newpass')
        assert "That username is already taken." in rv.data
      
    def test_404(self):
        rv = self.app.get('/notfound/')
        assert rv.status_code == 404

    def test_static(self):
        rv = self.app.get('/static/robots.txt')
        assert rv.status_code == 200
"""
#first two lines are normal init call without summary of pass/fail
if __name__ == "__main__":
    unittest.main()"""
#below if verbose output init call to see summary of what fails/passes
suite = unittest.TestLoader().loadTestsFromTestCase(AppTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
