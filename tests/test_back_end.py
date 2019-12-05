# test_basic.py

import os
import unittest

from appi import app, db

TEST_DB = 'app.db'

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
    self.assertEqual(response.status_code, 200)

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

  def test_show_process_group_page(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/process_groups', follow_redirects = True)
    self.assertEqual(response.status_code, 200)
    
  def test_show_tecAndTools_page(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/process_groups/1/tecAndTools', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_participants_actors_page(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/process_groups/1/actors', follow_redirects = True)
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

  def test_register_process_group(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_process_group',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_Tec(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/register_Tec',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_Tool(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/register_Tool',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_participants_actors(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/register_actor',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
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

  def test_edit_process_group(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_process_group/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_Tec(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/edit_Tec/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_Tool(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/edit_Tool/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_participants_actors(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/edit_actor/1',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
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

  def test_delete_process_group(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      'delete_process_group/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tec(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tec/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tool(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tool/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_participants_actors(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_actor/1',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_DSPGPGC_in_workflow(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_DSPGPGC/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_process_group_in_workflow(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      'delete_process_group/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tec_in_workflow(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tec/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tool_in_workflow(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tool/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_participants_actors_in_workflow(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_actor/1',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_main_page2(self):
    response = self.app.get('/', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_correct_login2(self):
    response = self.login('mfaria', '12345678')
    self.assertEqual(response.status_code, 200)

  def test_incorrect_login2(self):
    response = self.login('mfaria', 'password')
    self.assertEqual(response.status_code, 200)

  def test_show_users_page2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/show_users', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_DPGPAS_page2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/show_DPGPAS', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_DSPGPGC_page2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/show_DSPGPGC', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_process_group_page2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/process_groups', follow_redirects = True)
    self.assertEqual(response.status_code, 200)
    
  def test_show_tecAndTools_page2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/process_groups/1/tecAndTools', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_show_participants_actors_page2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.get('/process_groups/1/actors', follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_users2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_users',
      data = dict(username='epale', password='12345648', email='testemail@email.com'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 404)

  def test_register_DPGPAS2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_DPGPAS',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_DSPGPGC2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_DSPGPGC',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_process_group2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/register_process_group',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_Tec2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/register_Tec',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_Tool2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/register_Tool',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_register_participants_actors2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/register_actor',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)
    
  def test_edit_users2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_users/1',
      data = dict(username='epale', password='12345648', email='testemail@email.com'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 404)

  def test_edit_DPGPAS2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_DPGPAS/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_DSPGPGC2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_DSPGPGC/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_process_group2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/edit_process_group/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_Tec2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/edit_Tec/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_Tool2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/edit_Tool/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_edit_participants_actors2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/edit_actor/1',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)
    
  def test_delete_users2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_users/1',
      data = dict(username='epale', password='12345648', email='testemail@email.com'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 404)

  def test_delete_DPGPAS2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_DPGPAS/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_DSPGPGC2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_DSPGPGC/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_process_group2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      'delete_process_group/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tec2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tec/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tool2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tool/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_participants_actors2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_actor/1',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_DSPGPGC_in_workflow2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/delete_DSPGPGC/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_process_group_in_workflow2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      'delete_process_group/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tec_in_workflow2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tec/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_Tool_in_workflow2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_Tool/1',
      data = dict(description='Mi Disciplina'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)

  def test_delete_participants_actors_in_workflow2(self):
    response = self.login('mfaria', '12345678')
    response = self.app.post(
      '/process_groups/1/delete_actor/1',
      data = dict(name='Nombre', lastname='Apellido', role='Todos'), 
      follow_redirects = True)
    self.assertEqual(response.status_code, 200)
    
if __name__ == "__main__":
  unittest.main()
