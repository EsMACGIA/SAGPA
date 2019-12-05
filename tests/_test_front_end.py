# tests/front_end_tests.py

import unittest
import urllib

from flask_testing import LiveServerTestCase
from selenium import webdriver

from appi.models import User, DPGPAS, DSPGPGC, ProcessGroup, Tec, Tool, ParticipantsActors, Project

import time
from flask import url_for

# Set test variables for test admin user
test_admin_username = "admin"
test_admin_email = "admin@email.com"
test_admin_password = "admin2016"

# Set test variables for test gerente
test_gerente_first_name = "Test"
test_gerente_last_name = "Employee"
test_gerente_username = "gerente"
test_gerente_email = "gerente@email.com"
test_gerente_password = "1test2016"

# Set test variables for test especialista
test_especialista_first_name = "Test"
test_especialista_last_name = "Employee"
test_especialista_username = "especialista"
test_especialista_email = "especialista@email.com"
test_especialista_password = "2test2016"

# Set variables for test disciplinas de proceso
test_proceso_description = "Disciplina de Proceso 1"

# Set variables for test disciplinas de soporte
test_soporte_description = "Disciplina de Soporte 1"

# Set variables for test proyectos
test_proyecto_description = "Proyecto 1"

# Set variables for test Actividades
test_actividad_description = "Actividad 1"

# Set variables for test Tarea
test_tarea_description = "Tarea 1"


class TestBase(LiveServerTestCase):

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        return app

    def setUp(self):
        """Setup the test driver and create test users"""
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())

        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        self.admin = User(username=test_admin_username,
                              email=test_admin_email,
                              password=test_admin_password,
                              is_admin=True)

        # create test employee user
        self.habilitadora = DPGPAS(username=test_employee1_username,
                                 first_name=test_employee1_first_name,
                                 last_name=test_employee1_last_name,
                                 email=test_employee1_email,
                                 password=test_employee1_password)

        # create test disciplina
        self.soporte = DSPGPGC(name=test_disciplina1_name,
                                     description=test_disciplina1_description)

        # create test role
        self.grupo = ProcessGroup(name=test_role1_name,
                         description=test_role1_description)

        # save users to database
        db.session.add(self.admin)
        db.session.add(self.habilitadora)
        db.session.add(self.soporte)
        db.session.add(self.grupo)
        db.session.commit()

    def tearDown(self):
        self.driver.quit()

    def test_server_is_up_and_running(self):
        response = urllib.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)


if __name__ == '__main__':
    unittest.main()

class TestRegistration(TestBase):

    def test_registration(self):
        """
        Tests that a user can be added to the sistem as gerente de proyecto
        """

        # Click register menu link
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys(test_especialista_email)
        self.driver.find_element_by_id("username").send_keys(
            test_especialista_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_especialista_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_especialista_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_especialista_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            test_especialista_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert url_for('auth.login') in self.driver.current_url

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully registered" in success_message

        # Assert that there are now 3 employees in the database
        self.assertEqual(Employee.query.count(), 3)

    def test_registration_invalid_email(self):
        """
        Test that a user cannot register using an invalid email format
        and that an appropriate error message will be displayed
        """

        # Click register menu link
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys("invalid_email")
        self.driver.find_element_by_id("username").send_keys(
           test_especialista_username)
        self.driver.find_element_by_id("first_name").send_keys(
           test_especialista_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
           test_especialista_last_name)
        self.driver.find_element_by_id("password").send_keys(
           test_especialista_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
           test_especialista_password)
        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Invalid email address" in error_message

    def test_registration_confirm_password(self):
        """
        Test that an appropriate error message is displayed when the password 
        and confirm_password fields do not match
        """

        # Click register menu link
        self.driver.find_element_by_id("register_link").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_id("email").send_keys(test_especialista_email)
        self.driver.find_element_by_id("username").send_keys(
            test_especialista_username)
        self.driver.find_element_by_id("first_name").send_keys(
            test_especialista_first_name)
        self.driver.find_element_by_id("last_name").send_keys(
            test_especialista_last_name)
        self.driver.find_element_by_id("password").send_keys(
            test_especialista_password)
        self.driver.find_element_by_id("confirm_password").send_keys(
            "password-won't-match")
        self.driver.find_element_by_id("submit").click()
        time.sleep(5)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name(
            "help-block").text
        assert "Field must be equal to confirm_password" in error_message

class TestLogin(object):

    def login_admin_user(self):
        """Log in as the test gerente"""
        login_link = self.get_server_url() + url_for('auth.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id("email").send_keys(test_admin_email)
        self.driver.find_element_by_id("password").send_keys(
            test_admin_password)
        self.driver.find_element_by_id("submit").click()

    def login_test_user(self):
        """Log in as the test especialista"""
        login_link = self.get_server_url() + url_for('auth.login')
        self.driver.get(login_link)
        self.driver.find_element_by_id("email").send_keys(test_gerente_email)
        self.driver.find_element_by_id("password").send_keys(
            test_gerente_password)
        self.driver.find_element_by_id("submit").click()

def add_disciplina(self):

    # existing code remains

    if form.validate_on_submit():
        disciplina = disciplina(name=form.name.data,
                                description=form.description.data)
        try:
            # add disciplina to the database
            db.session.add(disciplina)
            db.session.commit()
            flash('You have successfully added a new disciplina.')
        except:
            # in case disciplina name already exists
            db.session.rollback()
            flash('Error: disciplina name already exists.')

class TestRoles(CreateObjects, TestBase):

    def test_add_role(self):
        """
        Test that an admin user can add a role
        """

        # Login as admin user
        self.login_admin_user()

        # Click roles menu link
        self.driver.find_element_by_id("roles_link").click()
        time.sleep(1)

        # Click on add role button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Fill in add role form
        self.driver.find_element_by_id("name").send_keys(test_role2_name)
        self.driver.find_element_by_id("description").send_keys(
            test_role2_description)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully added a new role" in success_message

        # Assert that there are now 2 roles in the database
        self.assertEqual(Role.query.count(), 2)

    def test_add_existing_role(self):
        """
        Test that an admin user cannot add a role with a name
        that already exists
        """

        # Login as admin user
        self.login_admin_user()

        # Click roles menu link
        self.driver.find_element_by_id("roles_link").click()
        time.sleep(1)

        # Click on add role button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Fill in add role form
        self.driver.find_element_by_id("name").send_keys(test_role1_name)
        self.driver.find_element_by_id("description").send_keys(
            test_role1_description)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Error: role name already exists" in error_message

        # Assert that there is still only 1 role in the database
        self.assertEqual(Role.query.count(), 1)

    def test_edit_role(self):
        """
        Test that an admin user can edit a role
        """

        # Login as admin user
        self.login_admin_user()

        # Click roles menu link
        self.driver.find_element_by_id("roles_link").click()
        time.sleep(1)

        # Click on edit role link
        self.driver.find_element_by_class_name("fa-pencil").click()
        time.sleep(1)

        # Fill in add role form
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys("Edited name")
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(
            "Edited description")
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully edited the role" in success_message

        # Assert that role name and description has changed
        role = Role.query.get(1)
        self.assertEqual(role.name, "Edited name")
        self.assertEqual(role.description, "Edited description")

    def test_delete_role(self):
        """
        Test that an admin user can delete a role
        """

        # Login as admin user
        self.login_admin_user()

        # Click roles menu link
        self.driver.find_element_by_id("roles_link").click()
        time.sleep(1)

        # Click on edit role link
        self.driver.find_element_by_class_name("fa-trash").click()
        time.sleep(1)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully deleted the role" in success_message

        # Assert that there are no roles in the database
        self.assertEqual(Role.query.count(), 0)

class Testdisciplinas(CreateObjects, TestBase):

    def test_add_disciplina(self):
        """
        Test that an admin user can add a disciplina
        """

        # Login as admin user
        self.login_admin_user()

        # Click disciplinas menu link
        self.driver.find_element_by_id("disciplinas_link").click()
        time.sleep(1)

        # Click on add disciplina button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Fill in add disciplina form
        self.driver.find_element_by_id("name").send_keys(test_disciplina2_name)
        self.driver.find_element_by_id("description").send_keys(
            test_disciplina2_description)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully added a new disciplina" in success_message

        # Assert that there are now 2 disciplinas in the database
        self.assertEqual(disciplina.query.count(), 2)

    def test_add_existing_disciplina(self):
        """
        Test that an admin user cannot add a disciplina with a name
        that already exists
        """

        # Login as admin user
        self.login_admin_user()

        # Click disciplinas menu link
        self.driver.find_element_by_id("disciplinas_link").click()
        time.sleep(1)

        # Click on add disciplina button
        self.driver.find_element_by_class_name("btn").click()
        time.sleep(1)

        # Fill in add disciplina form
        self.driver.find_element_by_id("name").send_keys(test_disciplina1_name)
        self.driver.find_element_by_id("description").send_keys(
            test_disciplina1_description)
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert error message is shown
        error_message = self.driver.find_element_by_class_name("alert").text
        assert "Error: disciplina name already exists" in error_message

        # Assert that there is still only 1 disciplina in the database
        self.assertEqual(disciplina.query.count(), 1)

    def test_edit_disciplina(self):
        """
        Test that an admin user can edit a disciplina
        """

        # Login as admin user
        self.login_admin_user()

        # Click disciplinas menu link
        self.driver.find_element_by_id("disciplinas_link").click()
        time.sleep(1)

        # Click on edit disciplina link
        self.driver.find_element_by_class_name("fa-pencil").click()
        time.sleep(1)

        # Fill in add disciplina form
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys("Edited name")
        self.driver.find_element_by_id("description").clear()
        self.driver.find_element_by_id("description").send_keys(
            "Edited description")
        self.driver.find_element_by_id("submit").click()
        time.sleep(2)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully edited the disciplina" in success_message

        # Assert that disciplina name and description has changed
        disciplina = disciplina.query.get(1)
        self.assertEqual(disciplina.name, "Edited name")
        self.assertEqual(disciplina.description, "Edited description")

    def test_delete_disciplina(self):
        """
        Test that an admin user can delete a disciplina
        """

        # Login as admin user
        self.login_admin_user()

        # Click disciplinas menu link
        self.driver.find_element_by_id("disciplinas_link").click()
        time.sleep(1)

        # Click on edit disciplina link
        self.driver.find_element_by_class_name("fa-trash").click()
        time.sleep(1)

        # Assert success message is shown
        success_message = self.driver.find_element_by_class_name("alert").text
        assert "You have successfully deleted the disciplina" in success_message

        # Assert that there are no disciplinas in the database
        self.assertEqual(disciplina.query.count(), 0)