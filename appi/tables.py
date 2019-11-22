from flask_table import Table, Col, LinkCol
 
class Users_Table(Table):

    classes = ["table table-hover"]
    id = Col('Id', show=False)
    username = Col('Username')
    email = Col('Email')
    rank = Col('Rank')
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