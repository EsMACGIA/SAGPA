from flask import render_template, flash, redirect, url_for, request
from appi import app, db
from flask_login import current_user, login_user, logout_user, login_required
from appi.models import User, DPGPAS, DSPGPGC
from werkzeug.urls import url_parse
from appi.forms import RegistrationForm, LoginForm, EditForm, RegistrationFormDPGPAS, RegistrationFormDSPGPGC,\
                         EditFormDPGPAS, EditFormDSPGPGC
from appi.tables import Users_Table, DPGPAS_Table, DSPGPGC_Table

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", title='Home Page', posts=posts)



@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html', title='Sign In', form=form)

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
    return render_template('register.html', title='Register', form=form)

@app.route('/show_users', methods=['GET', 'POST'])
@login_required
def show_users():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = User.query.all()
    table = Users_Table(query)
    table.border = True
    return render_template('users_list.html', title="Users List", table=table)



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

        return render_template('edit_user.html', form=form)
    else:
        console.log("base de datos no consiguio el usuario")
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

    return render_template('index.html', title='Home Page')

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
    return render_template('register_discipline.html', title='Register DPGPAS', form=form,  discipline_type="DPGPAS")

@app.route('/show_DPGPAS', methods=['GET', 'POST'])
@login_required
def show_DPGPAS():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = DPGPAS.query.all()
    table = DPGPAS_Table(query)
    table.border = True
    return render_template('DPGPAS_list.html', title="DPGPAS List", table=table)

@app.route('/edit_DPGPAS/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DPGPAS(id):

    
 
    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = DPGPAS.query.filter_by(id=id).first()

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

        return render_template('edit_DPGPAS.html', form=form)
    else:
        console.log("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_DPGPAS/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DPGPAS(id):

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

    return render_template('index.html', title='Home Page')

# DSPGPGC Routes

@app.route('/register_DSPGPGC', methods=['GET', 'POST'])
@login_required
def register_DSPGPGC():

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
    return render_template('register_discipline.html', title='Register DSPGPGC', form=form,  discipline_type="DSPGPGC")


@app.route('/show_DSPGPGC', methods=['GET', 'POST'])
@login_required
def show_DSPGPGC():

    if(current_user.rank != 'Administrator'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = DSPGPGC.query.all()
    table = DSPGPGC_Table(query)
    table.border = True
    return render_template('DSPGPGC_list.html', title="DSPGPGC List", table=table)


@app.route('/edit_DSPGPGC/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DSPGPGC(id):

    
 
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

        return render_template('edit_DSPGPGC.html', form=form)
    else:
        console.log("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_DSPGPGC/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DSPGPGC(id):

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

    return render_template('index.html', title='Home Page')
