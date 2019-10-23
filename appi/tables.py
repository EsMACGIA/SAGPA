from flask_table import Table, Col, LinkCol
 
class Users_Table(Table):

    
    id = Col('Id', show=False)
    username = Col('Username')
    email = Col('Email')
    rank = Col('Rank')
    edit = LinkCol('Edit', 'edit_user', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_user', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})

class DPGPAS_Table(Table):

    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_DPGPAS', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_DPGPAS', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})

class DSPGPGC_Table(Table):

    id = Col('Id', show=False)
    description = Col('Description')
    edit = LinkCol('Edit', 'edit_DSPGPGC', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete_DSPGPGC', url_kwargs=dict(id='id'), 
                    anchor_attrs={'id': 'warning'})
    

   