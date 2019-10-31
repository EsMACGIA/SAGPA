# test_basic.py

import os
import unittest

from appi import app, db

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):

  ###########################
  ########## Helpers ########
  ###########################

  def login(self, username, password):
    return self.app.post(
        '/login',
        data=dict(username=username, password=password),
        follow_redirects=True
    )

  def logout(self):
    return self.app.get(
        '/logout',
        follow_redirects=True
    )

  ############################
  #### setup and teardown ####
  ############################

  # executed prior to each test
  def setUp(self):
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
      os.path.join(app.config['BASEDIR'], TEST_DB)
    self.app = app.test_client()

    self.logout()
    # db.drop_all()
    # db.create_all()

  # executed after each test
  def tearDown(self):
    pass

  ###########################
  ########## Tests ##########
  ###########################

  def test_main_page(self):
    response = self.app.get('/', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_correct_login(self):
    response = self.login('mfaria', '12345678')
    self.assertEqual(response.status_code, 200)

  def test_incorrect_login(self):
    response = self.login('mfaria', 'password')
    self.assertEqual(response.status_code, 400)

  def test_show_users_page(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/show_users', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_DPGPAS_page(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/show_DPGPAS', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_DSPGPGC_page(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/show_DSPGPGC', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_users(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_users',
      data = dict(username='epale', password='12345648', email='testemail@email.com'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 404)

  def test_register_DPGPAS(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_DPGPAS',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_DSPGPGC(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_DSPGPGC',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_users(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_users/1',
      data = dict(username='epale', password='12345648', email='testemail@email.com'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 404)

  def test_edit_DPGPAS(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_DPGPAS/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_DSPGPGC(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_DSPGPGC/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_users(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_users/1',
      data = dict(username='epale', password='12345648', email='testemail@email.com'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 404)

  def test_delete_DPGPAS(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_DPGPAS/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_DSPGPGC(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_DSPGPGC/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
  unittest.main()
