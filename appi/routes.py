from flask import render_template, flash, redirect, url_for, request
from appi import app, db
from flask_login import current_user, login_user, logout_user, login_required
from appi.models import User, DPGPAS, DSPGPGC, ProcessGroup
from werkzeug.urls import url_parse
from appi.forms import RegistrationForm, LoginForm, EditForm, RegistrationFormDPGPAS, RegistrationFormDSPGPGC,\
                         EditFormDPGPAS, EditFormDSPGPGC, RegistrationFormProcessGroup, EditFormProcessGroup
from appi.tables import Users_Table, DPGPAS_Table, DSPGPGC_Table, ProcessGroup_Table

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = []
    query = ProcessGroup.query.all()
    return render_template("index.html", title='Home Page', posts=posts, processes=query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    query = ProcessGroup.query.all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')

            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, processes=query)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, processes=query)

@app.route('/show_users', methods=['GET', 'POST'])
@login_required
def show_users():
    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator')

        return render_template('index.html', title='Home Page'), 400
    query = User.query.all()
    table = Users_Table(query)
    table.border = True
    query = ProcessGroup.query.all()
    return render_template('users_list.html', title="Users List", table=table, processes=query), 200



@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):

    
 
    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    user = User.query.filter_by(id=id).first()

    if user:
        form = EditForm(formdata=request.form, obj=user)
        if form.validate_on_submit():

            new_username = form.username.data
            new_email = form.email.data
            # check for errors with new names being in use

            used_username = User.query.filter_by(username=new_username).first()
            used_email = User.query.filter_by(email=new_email).first()

            # if exists a different user using the same username
            if used_username:
                if used_username.id != id:
                    form.username.errors.append('Please use a different username.')
                    return render_template('edit_user.html', form=form)

            # if exists a different user using the same email
            if used_email:
                if used_email.id != id:
                    form.email.errors.append('Please use a different email address.')
                    return render_template('edit_user.html', form=form)
           
            # save edits
            user.email = new_email
            user.username =  new_username
            user.rank = form.rank.data
            db.session.commit()
            flash('User updated successfully!')
            return redirect('/')
        query = ProcessGroup.query.all()
        return render_template('edit_user.html', form=form, processes=query)
    else:
        print("base de datos no consiguio el usuario")
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully');
    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)

# DPGPAS Routes

@app.route('/register_DPGPAS', methods=['GET', 'POST'])
@login_required
def register_DPGPAS():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    form = RegistrationFormDPGPAS()
    if form.validate_on_submit():
        discipline = DPGPAS(description=form.description.data)
       
        db.session.add(discipline)
        db.session.commit()
        flash('New Gerencia de Proyectos Agrícolas adedded')
        return redirect(url_for('index'))
    query = ProcessGroup.query.all()
    return render_template('register_discipline.html', title='Register DPGPAS', form=form,  discipline_type="Disciplina de Proceso", processes=query)

@app.route('/show_DPGPAS', methods=['GET', 'POST'])
@login_required
def show_DPGPAS():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = DPGPAS.query.all()
    table = DPGPAS_Table(query)
    table.border = True
    query = ProcessGroup.query.all()
    return render_template('DPGPAS_list.html', title="DPGPAS List", table=table, processes=query)

@app.route('/edit_DPGPAS/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DPGPAS(id):

    
 
    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = DPGPAS.query.filter_by(id=id).first()
    query = ProcessGroup.query.all()

    if discipline:
        form = EditFormDPGPAS(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use

            used_description = DPGPAS.query.filter_by(description=new_description).first()

            # if exists a different user using the same username
            if used_description:
                if used_description.id != id:
                    form.description.errors.append('Please use a different description.')
                    return render_template('edit_DPGPAS.html', form=form)
           
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect('/')

        return render_template('edit_DPGPAS.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_DPGPAS/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DPGPAS(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = DPGPAS.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Discipline deleted successfully');

    else:
        flash('Not such discipline!');

    return render_template('index.html', title='Home Page', processes=query)

# DSPGPGC Routes

@app.route('/register_DSPGPGC', methods=['GET', 'POST'])
@login_required
def register_DSPGPGC():
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    form = RegistrationFormDSPGPGC()
    if form.validate_on_submit():
        discipline = DSPGPGC(description=form.description.data)
       
        db.session.add(discipline)
        db.session.commit()
        flash('New Gerencia de Proyectos Agrícolas adedded')
        return redirect(url_for('index'))
    return render_template('register_discipline.html', title='Register DSPGPGC', form=form,  discipline_type="Disciplina de Soporte", processes=query)


@app.route('/show_DSPGPGC', methods=['GET', 'POST'])
@login_required
def show_DSPGPGC():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = DSPGPGC.query.all()
    table = DSPGPGC_Table(query)
    table.border = True
    query = ProcessGroup.query.all()
    return render_template('DSPGPGC_list.html', title="DSPGPGC List", table=table, processes=query)


@app.route('/edit_DSPGPGC/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DSPGPGC(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = DSPGPGC.query.filter_by(id=id).first()

    if discipline:
        form = EditFormDSPGPGC(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use

            used_description = DSPGPGC.query.filter_by(description=new_description).first()

            # if exists a different user using the same username
            if used_description:
                if used_description.id != id:
                    form.description.errors.append('Please use a different description.')
                    return render_template('edit_DSPGPGC.html', form=form)
           
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect('/')

        return render_template('edit_DSPGPGC.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_DSPGPGC/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DSPGPGC(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = DSPGPGC.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Discipline deleted successfully');

    else:
        flash('Not such discipline!');

    return render_template('index.html', title='Home Page', processes=query)

@app.route('/process_groups', methods=['GET'])
@login_required
def show_process_groups():
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = ProcessGroup.query.all()
    table = ProcessGroup_Table(query)
    table.border = True
    return render_template('process_groups_list.html', title="Grupo de Procesos", table=table, processes=query)

@app.route('/register_process_group', methods=['GET', 'POST'])
@login_required
def register_process_group():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    form = RegistrationFormProcessGroup()
    if form.validate_on_submit():
        process_group = ProcessGroup(description=form.description.data)
       
        db.session.add(process_group)
        db.session.commit()
        flash('New Process Group added')
        return redirect(url_for('show_process_groups'))
    query = ProcessGroup.query.all()
    return render_template('register_process_groups.html', title='Register Process Group', form=form,  process_group="Grupo de Proceso", processes=query)

@app.route('/edit_process_group/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_process_group(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    process_group = ProcessGroup.query.filter_by(id=id).first()

    if process_group:
        form = EditFormProcessGroup(formdata=request.form, obj=process_group)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use

            used_description = ProcessGroup.query.filter_by(description=new_description).first()

            # if exists a different user using the same username
            if used_description:
                if used_description.id != id:
                    form.description.errors.append('Please use a different description.')
                    return render_template('edit_process_group.html', form=form)
           
            # save edits
            process_group.description = new_description
            db.session.commit()
            flash('Process Group updated successfully!')
            return redirect(url_for('show_process_groups'))

        return render_template('edit_process_group.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_process_group/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_process_group(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    process_group = ProcessGroup.query.filter_by(id=id).first()
    if process_group:
        db.session.delete(process_group)
        db.session.commit()
        flash('Discipline deleted successfully')
        return redirect(url_for('show_process_groups'))

    else:
        flash('Not such discipline!')

    return render_template('index.html', title='Home Page', processes=query)