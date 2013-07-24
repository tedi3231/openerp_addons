from osv import osv,fields

class ParamList(osv.Model):
    _name = 'bpm.paramlist'
    _columns = {
        'name':fields.char(string="Display Name",size=50,requried=True,translate=True),
        'value':fields.char(string="ParamList Value",size=100,requried=True,translate=True),
        'sortnum':fields.integer(string="Sort Num",requried=False),
        #'parentlist':fields.char(string="Parent List",size=50,requried=False,translate=False),
        #'paramitems':fields.many2one(string='Param Items',)
    }
    
    def _check_value(self,cr,uid,ids):
        """
        check paramlist value exists
        """
        print '_check_value ids=%s'%ids
        items = self.browse(cr,uid,ids)
        print 'items=%s'%items
        if not items:
            return False
        current_item=items[0]
        print current_item.name 
        result=self.search(cr,uid,[('value','=',current_item.value),('id','!=',ids[0])])
        print 'result=%s'%result
        if not result:
            return True
        return False

    _constraints = [(_check_value,'Paramlist value has been exists!',['value'])]


class ParamItem(osv.Model):
    _name = 'bpm.paramitem'
    _columns={
        'text':fields.char(string="Display Name",size=100,requried=True,translate=True),
        'value':fields.char(string="Param Value",size=100,requried=True,translate=False),
        #'parentvalue':fields.char(string="Parent Value",size=100,requried=False),
        'sortnum':fields.integer(string="Sort Num"),
        'parentlistid':fields.many2one('bpm.paramlist','ParamList Name')
    }


class ApproveComment(osv.Model):
    _name='bpm.approvecomment'
    _columns = {
        'processid':fields.many2one('bpm.processbase',string='Process Instance'),
        'comment':fields.text(string='Comment')
    }

class Process(osv.Model):
    _name = 'bpm.process'
    _columns ={
        'name':fields.char(string='Process Name',size=100,requried=True,tanslate=True),
        'code':fields.char(string='Process code',size=100,requried=True,tanslate=True),
    }
    _sql_constraints = [('name','unique(name)','Process name must be unique'),('code','unique(code)','Process code must be unique')]

PROCESS_STATUS=[('return','Return'),('pendding','Pendding'),('approved','Approved'),('reject','Rejected')]

class ProcessBase(osv.Model):
    _name = 'bpm.processbase'
    
    def _get_default_user_id(self,cr,uid,context=None):
        return uid

    _columns ={
        'processid':fields.char(string="Process Id",size=50,requried=True,translate=True),
        'processname':fields.char(string='Process Name',size=100,requried=True,translate=True),
        'status':fields.selection(string="Status",selection=PROCESS_STATUS),
        'applyperson':fields.many2one('res.users','Apply Person'),
        #'approvecomments':fields.one2many('bpm.approvecomment','ApproveComments')
    }

    _defaults = {
        'applyperson':_get_default_user_id,
        'status':'pendding',
    }

    _sql_constraints=[('processid','unique(processid)','ProcessId must be unique!')]

class Person(osv.osv):
    _name = "bpm.person"
    _columns={
        "name":fields.char(string="Name",size=200),
        "cardid":fields.char(string="Card Id",size=100),
    }
Person()

class Student(osv.osv):
    _name="bpm.person"
    _inherit="bpm.person"
    _columns={
        "age":fields.integer("Age"),
        "sex":fields.selection([('male','Male'),('female','Female')],"Sex")
    }
Student()