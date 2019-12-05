from flask import render_template, flash, redirect, url_for, request, make_response
from appi import app, db
from flask_login import current_user, login_user, logout_user, login_required
from appi.models import User, DPGPAS, DSPGPGC, ProcessGroup, ProcessGroupWithDPGPAS2, ProcessGroupWithDSPGPGC2
from werkzeug.urls import url_parse
from appi.forms import RegistrationForm, LoginForm, EditForm, RegistrationFormDPGPAS, RegistrationFormDSPGPGC,\
                         EditFormDPGPAS, EditFormDSPGPGC, RegistrationFormProcessGroupWithDPGPAS2, RegistrationFormProcessGroupWithDSPGPGC2
from appi.tables import Users_Table, DPGPAS_Table, DSPGPGC_Table, ProcessGroup_Table, EnablingDisciplines_Table, SupportingDisciplines_Table, \
                        Project_Table, ActivityDPGPAS_Table
from appi.models import User, DPGPAS, DSPGPGC, ProcessGroup, Tec, Tool, ParticipantsActors, Project, ActivityDPGPAS, ActivityDSPGPGC,TaskActivityDPGPAS,TaskActivityDSPGPGC
from werkzeug.urls import url_parse
from appi.forms import RegistrationForm, LoginForm, EditForm, RegistrationFormDPGPAS, RegistrationFormDSPGPGC,\
                         EditFormDPGPAS, EditFormDSPGPGC, RegistrationFormProcessGroup, EditFormProcessGroup, \
                         EditFormTec, EditFormTool, RegistrationFormTec, RegistrationFormTool, RegistrationFormActor, \
                         EditFormProject, RegistrationFormProject, RegistrationFormDPGPASActivity, EditFormDPGPASActivity, \
                         EditFormDSPGPGCActivity, RegistrationFormDSPGPGCActivity,RegistrationFormTaskDPGPASActivities
from appi.tables import Users_Table, DPGPAS_Table, DSPGPGC_Table, ProcessGroup_Table, Tools_Table, Tec_Table, Participants_Actors_Table, Project_Table, \
                         ActivityDPGPAS_Table, ActivityDSPGPGC_Table, TaskActivityDPGPAS_Table,TaskActivityDSPGPGC_Table
import pdfkit

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
    query = ProcessGroup.query.all()

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
    print('Query:', query[0].project_id)
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
    print(user.project_id)

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
            # print(form.project_id.data.id)
            user.project_id = form.project_id.data.id
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

    
 
    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = DPGPAS.query.filter_by(id=id)

    return render_template('index.html', title='Home Page', processes=query)

# DSPGPGC Routes

@app.route('/register_DSPGPGC', methods=['GET', 'POST'])
@login_required
def register_DSPGPGC():
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
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

##Process Gruops Routes 

@app.route('/process_groups', methods=['GET'])
@login_required
def show_process_groups():
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = ProcessGroup.query.all()
    table = ProcessGroup_Table(query)
    table.border = True
    return render_template('process_groups_list.html', title="Grupo de Procesos", table=table, processes=query)

@app.route('/workflow/<int:id>', methods=['GET'])
@login_required
def show_workflow(id):

    print('Id: ', id)
    processes = ProcessGroup.query.all()
    process = ProcessGroup.query.filter_by(id=id).first()
    query = (ProcessGroupWithDPGPAS2.query
            .join(ProcessGroup, ProcessGroupWithDPGPAS2.process_id==ProcessGroup.id)
            .join(DPGPAS, ProcessGroupWithDPGPAS2.dpgpas_id==DPGPAS.id))
    enabling_disciplines = EnablingDisciplines_Table(query)
    enabling_disciplines.border = True
    query = (ProcessGroupWithDSPGPGC2.query
        .join(ProcessGroup, ProcessGroupWithDSPGPGC2.process_id==ProcessGroup.id)
        .join(DSPGPGC, ProcessGroupWithDSPGPGC2.dspgpgc_id==DSPGPGC.id))
    supporting_disciplines = SupportingDisciplines_Table(query)
    supporting_disciplines.border = True


    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    return render_template(
             'workflow.html', 
             title="Flujos de Trabajo", 
             processes=processes,
             process=process,
             ed=enabling_disciplines,
             sd=supporting_disciplines
    )

@app.route('/workflow/DPGPAS/<int:id>', methods=['GET', 'POST'])
@login_required
def registerDPGPASinWorkflow(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    form = RegistrationFormProcessGroupWithDPGPAS2()
    
    if form.validate_on_submit():
        obj = ProcessGroupWithDPGPAS2(process_id=id, dpgpas_id=form.discipline_id.data.id, description=form.description.data)
        db.session.add(obj)
        db.session.commit()
        flash('Nueva disciplina añadida')
        return redirect(url_for('show_workflow', id=id))
    return render_template('register_discipline.html', title='Register Tool', form=form,  discipline_type="Disciplina Habilitadora", processes=query)


@app.route('/edit_workflow/DPGPAS', methods=['GET', 'POST'])
@login_required
def edit_DPGPAS_workflow():
    query = ProcessGroup.query.all()

    id = request.args.get('id')
    pid = request.args.get('pid')

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

        # print('PId: ', pid)

    discipline = ProcessGroupWithDPGPAS2.query.filter_by(id=id).first()

    if discipline:
        print('Hola')
        form = RegistrationFormProcessGroupWithDPGPAS2(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use
       
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect('/workflow/' + pid)
        return render_template('register_discipline.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_workflow/DPGPAS', methods=['GET', 'POST'])
@login_required
def delete_DPGPAS_workflow():
    query = ProcessGroup.query.all()

    id = request.args.get('id')
    pid = request.args.get('pid')

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = ProcessGroupWithDPGPAS2.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Discipline deleted successfully');

    else:
        flash('Not such discipline!');
    return redirect('/workflow/' + pid)

@app.route('/workflow/DSPGPGC/<int:id>', methods=['GET', 'POST'])
@login_required
def registerDSPGPGCinWorkflow(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    form = RegistrationFormProcessGroupWithDSPGPGC2()
    
    if form.validate_on_submit():
        obj = ProcessGroupWithDSPGPGC2(process_id=id, dspgpgc_id=form.discipline_id.data.id, description=form.description.data)
        db.session.add(obj)
        db.session.commit()
        flash('Nueva disciplina añadida')
        return redirect(url_for('show_workflow', id=id))
    return render_template('register_discipline.html', title='Register Tool', form=form,  discipline_type="Diciplina de Soporte", processes=query)


@app.route('/edit_workflow/DSPGPGC', methods=['GET', 'POST'])
@login_required
def edit_DSPGPGC_workflow():
    query = ProcessGroup.query.all()

    id = request.args.get('id')
    pid = request.args.get('pid')

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

        # print('PId: ', pid)

    discipline = ProcessGroupWithDSPGPGC2.query.filter_by(id=id).first()

    if discipline:
        print('Hola')
        form = RegistrationFormProcessGroupWithDSPGPGC2(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use
       
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect('/workflow/' + pid)
        return render_template('register_discipline.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_workflow/DSPGPGC', methods=['GET', 'POST'])
@login_required
def delete_DSPGPGC_workflow():
    query = ProcessGroup.query.all()

    id = request.args.get('id')
    pid = request.args.get('pid')

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = ProcessGroupWithDSPGPGC2.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Discipline deleted successfully');

    else:
        flash('Not such discipline!');
    return redirect('/workflow/' + pid)

@app.route('/register_process_group', methods=['GET', 'POST'])
@login_required
def register_process_group():

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
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

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
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

#TecAndTools Routes
@app.route('/process_groups/<int:pid>/tecAndTools', methods=['GET', 'POST'])
@login_required
def show_tecAndTools(pid):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query1 = Tec.query.filter_by(process_id=pid)
    table = Tec_Table(query1)
    query2 = Tool.query.filter_by(process_id=pid)
    table2 = Tools_Table(query2)
    table.border = True
    table2.border = True

    query = ProcessGroup.query.all()

    return render_template('tecAndTools_list.html', title="TecAndTools List", table=table, table1=table2, processes=query, pid=pid)

#Tec Routes
@app.route('/process_groups/<int:pid>/register_Tec', methods=['GET', 'POST'])
@login_required
def register_Tec(pid):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    form = RegistrationFormTec()
    if form.validate_on_submit():
        discipline = Tec(description=form.description.data)
        discipline.process_id = pid
        db.session.add(discipline)
        db.session.commit()
        flash('New Tec added')
        return redirect(url_for('show_tecAndTools', pid=pid))
    return render_template('register_discipline.html', title='Register Tec', form=form,  discipline_type="Técnica", processes=query)

@app.route('/process_groups/<int:pid>/edit_Tec/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_Tec(pid, id):
    query = Tec.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = Tec.query.filter_by(id=id).first()

    if discipline:
        form = EditFormTec(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use

            used_description = Tec.query.filter_by(description=new_description).first()

            # if exists a different user using the same username
            if used_description:
                if used_description.id != id:
                    form.description.errors.append('Please use a different description.')
                    return render_template('edit_Tec.html', form=form)
           
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect(url_for('show_tecAndTools', pid=pid))

        query = ProcessGroup.query.all()
        return render_template('edit_Tec.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/process_groups/<int:pid>/delete_Tec/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_Tec(pid, id):
    query = Tec.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = Tec.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Discipline deleted successfully');
        return redirect(url_for('show_tecAndTools', pid=pid))

    else:
        flash('Not such discipline!');

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', pid=pid, processes=query)

#Tools Routes
@app.route('/process_groups/<int:pid>/register_Tool', methods=['GET', 'POST'])
@login_required
def register_Tool(pid):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    form = RegistrationFormTool()
    if form.validate_on_submit():
        discipline = Tool(description=form.description.data)
        discipline.process_id = pid
        db.session.add(discipline)
        db.session.commit()
        flash('New Tool added')
        return redirect(url_for('show_tecAndTools', pid=pid))
    return render_template('register_discipline.html', title='Register Tool', form=form,  discipline_type="Herramienta", processes=query)

@app.route('/process_groups/<int:pid>/edit_Tool/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_Tool(pid, id):
    query = Tool.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = Tool.query.filter_by(id=id).first()

    if discipline:
        form = EditFormTool(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use

            used_description = Tool.query.filter_by(description=new_description).first()

            # if exists a different user using the same username
            if used_description:
                if used_description.id != id:
                    form.description.errors.append('Please use a different description.')
                    return render_template('edit_Tool.html', form=form)
           
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect(url_for('show_tecAndTools', pid=pid))

        query = ProcessGroup.query.all()
        return render_template('edit_Tool.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/process_groups/<int:pid>/delete_Tool/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_Tool(pid, id):
    query = Tool.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = Tool.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Discipline deleted successfully');
        return redirect(url_for('show_tecAndTools', pid=pid))

    else:
        flash('Not such discipline!');

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)


#Parcipants Actors Routes
@app.route('/process_groups/<int:pid>/actors', methods=['GET', 'POST'])
@login_required
def show_participants_actors(pid):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    query = ParticipantsActors.query.filter_by(process_id=pid)
    table = Participants_Actors_Table(query)
    table.border = True
    query = ProcessGroup.query.all()

    return render_template('participants_actors_list.html', title="Participants Actors List", table=table, processes=query, pid=pid)


@app.route('/process_groups/<int:pid>/register_actor', methods=['GET', 'POST'])
@login_required
def register_participant_actor(pid):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    form = RegistrationFormActor()
    if form.validate_on_submit():
        actor = ParticipantsActors(name=form.name.data,lastname=form.lastname.data,role=form.role.data)
        actor.process_id = pid
        db.session.add(actor)
        db.session.commit()
        flash('New Participant Actor added')
        return redirect(url_for('show_participants_actors', pid=pid))
    return render_template('register_discipline.html', title='Register Tool', form=form,  discipline_type="Actor Participante", processes=query)

@app.route('/process_groups/<int:pid>/edit_actor/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_participant_actor(pid, id):
    query = ParticipantsActors.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    actor = ParticipantsActors.query.filter_by(id=id).first()

    if actor:
        form = RegistrationFormActor(formdata=request.form, obj=actor)
        if form.validate_on_submit():
            # save edits
            actor.name = form.name.data
            actor.lastname = form.lastname.data
            actor.role = form.role.data
            db.session.commit()
            flash('Actor updated successfully!')
            return redirect(url_for('show_participants_actors', pid=pid))

        query = ProcessGroup.query.all()
        return render_template('edit_actor.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/process_groups/<int:pid>/delete_actor/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_participant_actor(pid, id):
    query = ParticipantsActors.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    actor = ParticipantsActors.query.filter_by(id=id).first()
    if actor:
        db.session.delete(actor)
        db.session.commit()
        flash('Actor deleted successfully')
        return redirect(url_for('show_participants_actors', pid=pid))

    else:
        flash('Not such actor!');

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)

# Project Routes

@app.route('/register_project', methods=['GET', 'POST'])
@login_required
def register_project():
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    form = RegistrationFormProject()
    if form.validate_on_submit():
        discipline = Project(description=form.description.data)
       
        db.session.add(discipline)
        db.session.commit()
        flash('Nuevo Proyecto agregado')
        return redirect(url_for('show_project'))
    return render_template('register_discipline.html', title='Register project', form=form,  discipline_type="Proyecto", processes=query)


@app.route('/show_projects', methods=['GET', 'POST'])
@login_required
def show_project():

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')
    query = Project.query.all()
    table = Project_Table(query)
    table.border = True
    query = ProcessGroup.query.all()
    return render_template('project_list.html', title="project List", table=table, processes=query)


@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = Project.query.filter_by(id=id).first()

    if discipline:
        form = EditFormProject(formdata=request.form, obj=discipline)
        if form.validate_on_submit():

            new_description = form.description.data
            # check for errors with new names being in use

            used_description = Project.query.filter_by(description=new_description).first()

            # if exists a different user using the same username
            if used_description:
                if used_description.id != id:
                    form.description.errors.append('Please use a different description.')
                    return render_template('edit_project.html', form=form)
           
            # save edits
            discipline.description = new_description
            db.session.commit()
            flash('Discipline updated successfully!')
            return redirect(url_for('show_project'))

        return render_template('edit_project.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete_project/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = Project.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Project deleted successfully');
        return redirect(url_for('show_project'))

    else:
        flash('Not such discipline!');

    return render_template('index.html', title='Home Page', processes=query)

# Actividades DPGPAS

@app.route('/workflow/<int:pid>/<int:did>/DPGAS_activities', methods=['GET', 'POST'])
@login_required
def show_DPGPAS_activities(pid, did):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    query = ActivityDPGPAS.query.filter_by(process_id=pid, dpgpas_id=did)
    table = ActivityDPGPAS_Table(query)
    table.border = True
    query = ProcessGroup.query.all()

    return render_template('activityDPGPAS_list.html', title="activity List", table=table, processes=query, pid=pid, did=did)

@app.route('/workflow/<int:pid>/<int:did>/register_DPGPAS_activity', methods=['GET', 'POST'])
@login_required
def register_DPGPAS_activity(pid, did):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    
    form = RegistrationFormDPGPASActivity()
    if form.validate_on_submit():
        discipline = ActivityDPGPAS(description=form.description.data)
        discipline.process_id = pid
        discipline.dpgpas_id = did
        db.session.add(discipline)
        db.session.commit()
        flash('New Activity added')
        return redirect(url_for('show_DPGPAS_activities', pid=pid, did=did))
    return render_template('register_discipline.html', title='Register Activity', form=form,  discipline_type="Actividad", processes=query)

@app.route('/workflow/<int:pid>/<int:did>/edit_DPGPAS_activity/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DPGPAS_activity(pid, did, id):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = ActivityDPGPAS.query.filter_by(id=id).first()

    if discipline:
        form = EditFormDPGPASActivity(formdata=request.form, obj=discipline)
        if form.validate_on_submit():
            # save edits
            discipline.description = form.description.data
            db.session.commit()
            flash('Activity updated successfully!')
            return redirect(url_for('show_DPGPAS_activities', pid=pid, did=did))

        query = ProcessGroup.query.all()
        return render_template('edit_DPGPAS_activity.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/workflow/<int:pid>/<int:did>/delete_DPGPAS_activity/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DPGPAS_activity(pid, did, id):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    discipline = ActivityDPGPAS.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Actor deleted successfully')
        return redirect(url_for('show_DPGPAS_activities', pid=pid, did=did))

    else:
        flash('Not such activity!')

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)

# Actividades DSPGPGC

@app.route('/workflow/<int:pid>/<int:did>/DSPGPGC_activities', methods=['GET', 'POST'])
@login_required
def show_DSPGPGC_activities(pid, did):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    query = ActivityDSPGPGC.query.filter_by(process_id=pid, dspgpgc_id=did)
    table = ActivityDSPGPGC_Table(query)
    table.border = True
    query = ProcessGroup.query.all()

    return render_template('activityDSPGPGC_list.html', title="Activity List", table=table, processes=query, pid=pid, did=did)

@app.route('/workflow/<int:pid>/<int:did>/register_DSPGPGC_activity', methods=['GET', 'POST'])
@login_required
def register_DSPGPGC_activity(pid, did):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    
    form = RegistrationFormDSPGPGCActivity()
    if form.validate_on_submit():
        discipline = ActivityDSPGPGC(description=form.description.data)
        discipline.process_id = pid
        discipline.dspgpgc_id = did
        db.session.add(discipline)
        db.session.commit()
        flash('New Activity added')
        return redirect(url_for('show_DSPGPGC_activities', pid=pid, did=did))
    return render_template('register_discipline.html', title='Register Activity', form=form,  discipline_type="Actividad", processes=query)

@app.route('/workflow/<int:pid>/<int:did>/edit_DSPGPGC_activity/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DSPGPGC_activity(pid, did, id):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator');
        return render_template('index.html', title='Home Page')

    discipline = ActivityDSPGPGC.query.filter_by(id=id).first()

    if discipline:
        form = EditFormDSPGPGCActivity(formdata=request.form, obj=discipline)
        if form.validate_on_submit():
            # save edits
            discipline.description = form.description.data
            db.session.commit()
            flash('Activity updated successfully!')
            return redirect(url_for('show_DSPGPGC_activities', pid=pid, did=did))

        query = ProcessGroup.query.all()
        return render_template('edit_DSPGPGC_activity.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la disciplina")
        return 'Error loading #{id}'.format(id=id)

@app.route('/workflow/<int:pid>/<int:did>/delete_DSPGPGC_activity/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DSPGPGC_activity(pid, did, id):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    discipline = ActivityDSPGPGC.query.filter_by(id=id).first()
    if discipline:
        db.session.delete(discipline)
        db.session.commit()
        flash('Actor deleted successfully')
        return redirect(url_for('show_DSPGPGC_activities', pid=pid, did=did))

    else:
        flash('Not such activity!')

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)


#### Task Activities DPGPAS

@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/DPGPAS_activities_tasks', methods=['GET', 'POST'])
@login_required
def show_DPGPAS_activities_tasks(pid, did,aid):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    query = TaskActivityDPGPAS.query.filter_by(process_id=pid, dpgpas_id=did,activity_id = aid)
    table = TaskActivityDPGPAS_Table(query)
    table.border = True
    query = ProcessGroup.query.all()

    return render_template('task_activityDPGPAS_list.html', title="Task Activity List", table=table, processes=query, pid=pid, did=did,aid=aid)


@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/register_DPGPAS_activity_task', methods=['GET', 'POST'])
@login_required
def register_DPGPAS_activity_task(pid, did,aid):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    
    form = RegistrationFormDSPGPGCActivity()
    if form.validate_on_submit():
        task = TaskActivityDPGPAS(description=form.description.data)
        task.process_id = pid
        task.dpgpas_id = did
        task.activity_id = aid
        db.session.add(task)
        print(db.session.commit())
        flash('New Task added')
        return redirect(url_for('show_DPGPAS_activities_tasks', pid=pid, did=did,aid=aid))
    return render_template('register_discipline.html', title='Register Task', form=form,  discipline_type="Tarea", processes=query)

@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/edit_DPGPAS_activity_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DPGPAS_activity_task(pid, did, aid, id):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    task = TaskActivityDPGPAS.query.filter_by(id=id).first()

    if task:
        form = EditFormDPGPASActivity(formdata=request.form, obj=task)
        if form.validate_on_submit():
            # save edits
            task.description = form.description.data
            db.session.commit()
            flash('Task updated successfully!')
            return redirect(url_for('show_DPGPAS_activities_tasks', pid=pid, did=did,aid=aid))

        query = ProcessGroup.query.all()
        return render_template('edit_DPGPAS_activity_task.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la tarea")
        return 'Error loading #{id}'.format(id=id)

@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/delete_DPGPAS_activity_task/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DPGPAS_activity_task(pid, did, id, aid):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    task = TaskActivityDPGPAS.query.filter_by(id=id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully')
        return redirect(url_for('show_DPGPAS_activities_tasks', pid=pid, did=did, aid=aid))

    else:
        flash('Not such activity!')

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)


#### Task Activities DSPGPGC


@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/DSPGPGC_activities_tasks', methods=['GET', 'POST'])
@login_required
def show_DSPGPGC_activities_tasks(pid, did,aid):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    query = TaskActivityDSPGPGC.query.filter_by(process_id=pid, dspgpgc_id=did,activity_id = aid)
    table = TaskActivityDSPGPGC_Table(query)
    table.border = True
    query = ProcessGroup.query.all()

    return render_template('task_activityDSPGPGC_list.html', title="Task Activity List", table=table, processes=query, pid=pid, did=did,aid=aid)


@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/register_DSPGPGC_activity_task', methods=['GET', 'POST'])
@login_required
def register_DSPGPGC_activity_task(pid, did,aid):
    query = ProcessGroup.query.all()

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')
    
    form = RegistrationFormDSPGPGCActivity()
    if form.validate_on_submit():
        task = TaskActivityDSPGPGC(description=form.description.data)
        task.process_id = pid
        task.dspgpgc_id = did
        task.activity_id = aid
        db.session.add(task)
        print(db.session.commit())
        flash('New Task added')
        return redirect(url_for('show_DSPGPGC_activities_tasks', pid=pid, did=did,aid=aid))
    return render_template('register_discipline.html', title='Register Task', form=form,  discipline_type="Tarea", processes=query)

@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/edit_DSPGPGC_activity_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_DSPGPGC_activity_task(pid, did, aid, id):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    task = TaskActivityDSPGPGC.query.filter_by(id=id).first()

    if task:
        form = EditFormDSPGPGCActivity(formdata=request.form, obj=task)
        if form.validate_on_submit():
            # save edits
            task.description = form.description.data
            db.session.commit()
            flash('Task updated successfully!')
            return redirect(url_for('show_DSPGPGC_activities_tasks', pid=pid, did=did,aid=aid))

        query = ProcessGroup.query.all()
        return render_template('edit_DSPGPGC_activity_task.html', form=form, processes=query)
    else:
        # print("base de datos no consiguio la tarea")
        return 'Error loading #{id}'.format(id=id)

@app.route('/workflow/<int:pid>/<int:did>/<int:aid>/delete_DSPGPGC_activity_task/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_DSPGPGC_activity_task(pid, did, id, aid):

    if(current_user.rank != 'Administrator' and current_user.rank != 'Specialist' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    task = TaskActivityDSPGPGC.query.filter_by(id=id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully')
        return redirect(url_for('show_DSPGPGC_activities_tasks', pid=pid, did=did, aid=aid))

    else:
        flash('Not such activity!')

    query = ProcessGroup.query.all()
    return render_template('index.html', title='Home Page', processes=query)


### Reportes PDF
@app.route('/reporte_pdf/<int:pid>')
def pdf_template(pid):
    if(current_user.rank != 'Administrator' and current_user.rank != 'Manager'):
        flash('You are not an Administrator')
        return render_template('index.html', title='Home Page')

    process = ProcessGroup.query.filter_by(id = pid).first().description
    activity_dspgpgc = ActivityDSPGPGC.query.filter_by(process_id=pid)
    activity_dpgpas = ActivityDPGPAS.query.filter_by(process_id=pid)
    actividad_tarea_dspgpgc = []
    actividad_tarea_dpgpas = []
    for i in activity_dspgpgc:
        print(i)
        tarea = TaskActivityDSPGPGC.query.filter_by(activity_id=i.id)
        if tarea.count() > 0:
            temp = {
            'activity' : i,
            'tasks' : tarea
            }
        else:
            temp = {
                'activity': i
            }
        actividad_tarea_dspgpgc.append(temp)
    for i in activity_dpgpas:
        tarea = TaskActivityDPGPAS.query.filter_by(activity_id=i.id)
        if tarea.count() > 0:
            temp = {
                'activity' : i,
                'tasks' : tarea
            }
        else:
            temp = {
                'activity': i
            }
        actividad_tarea_dpgpas.append(temp)
    objects = {
        'process' : process,
        'dspgpgc' : actividad_tarea_dspgpgc,
        'dpgpas' : actividad_tarea_dpgpas
    }
    rendered = render_template('pdf_report.html',objects=objects)
    pdf = pdfkit.from_string(rendered,False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte.pdf'
    return response