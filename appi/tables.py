from flask_table import Table, Col, LinkCol
 
class Users_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    username = Col('Usuario')
    email = Col('Email')
    rank = Col('Tipo')
    project_id = Col('Proyecto')
    edit = LinkCol('Edit', 'edit_user', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})

class DPGPAS_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_DPGPAS', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_DPGPAS', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})

class DSPGPGC_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_DSPGPGC', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_DSPGPGC', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})
    
class ProcessGroup_Table(Table):
    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_process_group', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_process_group', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})

class EnablingDisciplines_Table(Table):
    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    dpgpas_id = Col('Disciplina')
    process_id = Col('No', show=False)
    activities = LinkCol('Actividades', 'show_DPGPAS_activities', url_kwargs=dict(did='id', pid='process_id'))
    edit = LinkCol('Edit', 'edit_DPGPAS_workflow', url_kwargs=dict(id='id', pid='process_id'))
    delete = LinkCol('Delete', 'delete_DPGPAS_workflow', url_kwargs=dict(id='id', pid='process_id'), 
                    anchor_attrs={'id': 'warning'})

class SupportingDisciplines_Table(Table):
    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    dspgpgc_id = Col('Disciplina')
    process_id = Col('No', show=False)
    activities = LinkCol('Actividades', 'show_DSPGPGC_activities', url_kwargs=dict(did='id', pid='process_id'))
    edit = LinkCol('Edit', 'edit_DSPGPGC_workflow', url_kwargs=dict(id='id', pid='process_id'))
    delete = LinkCol('Delete', 'delete_DSPGPGC_workflow', url_kwargs=dict(id='id', pid='process_id'), 
                    anchor_attrs={'id': 'warning'})
   
   
class Tec_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_Tec', url_kwargs=dict(id='id', pid='process_id'))
    delete = LinkCol('Delete', 'delete_Tec', url_kwargs=dict(id='id', pid='process_id'), 
                    anchor_attrs={'id': 'warning'})

class Tools_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_Tool', url_kwargs=dict(id='id', pid='process_id'))
    delete = LinkCol('Delete', 'delete_Tool', url_kwargs=dict(id='id', pid='process_id'), 
                    anchor_attrs={'id': 'warning'})

class Participants_Actors_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    name = Col('Nombre')
    lastname = Col('Apellido')
    role = Col('Rol')
    edit = LinkCol('Edit', 'edit_participant_actor', url_kwargs=dict(id='id', pid='process_id'))
    delete = LinkCol('Delete', 'delete_participant_actor', url_kwargs=dict(id='id', pid='process_id'), 
                    anchor_attrs={'id': 'warning'})

class Project_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_project', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_project', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})

class ActivityDPGPAS_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    dpgpas_id = Col('Disciplina')
    process_id = Col('No', show=False)
    edit = LinkCol('Edit', 'edit_DPGPAS_activity', url_kwargs=dict(id='id', pid='process_id', did='dpgpas_id'))
    delete = LinkCol('Delete', 'delete_DPGPAS_activity', url_kwargs=dict(id='id', pid='process_id', did='dpgpas_id'), 
                    anchor_attrs={'id': 'warning'})

class ActivityDSPGPGC_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    description = Col('Description')
    dspgpgc_id = Col('Disciplina')
    process_id = Col('No', show=False)
    edit = LinkCol('Edit', 'edit_DSPGPGC_activity', url_kwargs=dict(id='id', pid='process_id', did='dspgpgc_id'))
    delete = LinkCol('Delete', 'delete_DSPGPGC_activity', url_kwargs=dict(id='id', pid='process_id', did='dspgpgc_id'), 
                    anchor_attrs={'id': 'warning'})