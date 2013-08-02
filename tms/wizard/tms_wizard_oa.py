from openerp.osv import fields, osv
from openerp.tools.translate import _

#feebase wizard
class tms_wizard_oa(osv.osv_memory):
    _name = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item", "wizard_id", string="Wizard"),
        'oanum': fields.char(string='OANum',size=50, required=True),
        'feetype':fields.char(string="Feetype",size=100,)
    }
    
    def _check_fee_state(self,cr,uid,ids,oldstate,targetstate,context=None):
        model_id = context["active_model"]
        model=self.pool.get(model_id)
        items = model.browse(cr,uid,ids,context=context)
        selecteditems=dict([(item.state,item.id) for item in items])
        if not selecteditems or len(selecteditems)!=1 or not selecteditems.get(oldstate,False):
            raise osv.except_osv(_('Operation Canceld'),_('Only '+oldstate+' fee can be exported!'))
        for item in items: 
            model.write(cr,uid,item.id,{"state":targetstate})
        return True

    def default_get(self, cr, uid, fields, context=None):
        if context == None:
            context = {}            
        wizard_id = context.get('acvite_id', None)
        active_model = context.get("active_model",None)
        if not active_model:
            return False
        res = []
        product_ids = context.get('active_ids', [])
        products = self.pool.get(active_model).browse(cr, uid, product_ids, context=context)
        for pitem in products:
            res.append({
                'wizard_id':wizard_id,
                'feebase_id':pitem.id,
                #'feetype':active_model,
            })
        return {'feebase_ids':res,'feetype':active_model}
    
    def setoanum(self, cr, uid, ids,context=None):
        print context
        active_model = context.get("active_model",None)
        wizard = self.browse(cr,uid,ids,context)[0]
        feeids = [item.feebase_id.id for item in wizard.feebase_ids]        
        feebase=self.pool.get(active_model)
        products = feebase.browse(cr,uid,feeids,context=context)
        selecteditems=dict([(item.state,item.id) for item in products])
        if not selecteditems or len(selecteditems)!=1 or not selecteditems.get('hasexported',False):
            raise osv.except_osv(_('Operation Canceld'),_('Only hasexported fee can be set oa num!'))
        for id in feeids:
            feebase.write(cr,uid,id,{"state":"hasoa","oanum":wizard.oanum})
        return True

tms_wizard_oa()


class tms_wizard_item(osv.osv_memory):
    _name = "tms.wizard.item"
    _description = "FeeBase Item"
    _columns = {
        "wizard_id":fields.many2one('tms.wizard.oa', string="Wizard", required=True),
        "feebase_id":fields.many2one('tms.feebase', string="Fee", required=True),
    }
tms_wizard_item()    


#forsend wizard
class tms_wizard_oa_forsend(osv.osv_memory):
    _name = "tms.wizard.oa.forsend"
    _inherit = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item.forsend", "wizard_id", string="Wizard"),
    }
tms_wizard_oa_forsend()

class tms_wizard_item_forsend(osv.osv_memory):
    _name = "tms.wizard.item.forsend"
    _inherit="tms.wizard.item"
    _description = "FeeBase Item"
    _columns = {
        "wizard_id":fields.many2one('tms.wizard.oa.forsend', string="Wizard", required=True),
        "feebase_id":fields.many2one('tms.feeforsend', string="Fee", required=True),
    }
tms_wizard_item_forsend()    

#product wizard
class tms_wizard_oa_forproduct(osv.osv_memory):
    _name = "tms.wizard.oa.forproduct"
    _inherit = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item.forproduct", "wizard_id", string="Wizard"),
    }
tms_wizard_oa_forproduct()

class tms_wizard_item_forproduct(osv.osv_memory):
    _name = "tms.wizard.item.forproduct"
    _description = "FeeBase Item"
    _columns = {
        "wizard_id":fields.many2one('tms.wizard.oa.forproduct', string="Wizard", required=True),
        "feebase_id":fields.many2one('tms.feeforproduct', string="Fee", required=True),
    }
tms_wizard_item_forproduct()   

#product wiard
class tms_wizard_oa_forproductit(osv.osv_memory):
    _name = "tms.wizard.oa.forproductit"
    _inherit = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item.forproductit", "wizard_id", string="Wizard"),
    }
tms_wizard_oa_forproductit()

class tms_wizard_item_forproductit(osv.osv_memory):
    _name = "tms.wizard.item.forproductit"
    _description = "FeeBase Item"
    _columns = {
        "wizard_id":fields.many2one('tms.wizard.oa.forproductit', string="Wizard", required=True),
        "feebase_id":fields.many2one('tms.feeforproductit', string="Fee", required=True),
    }
tms_wizard_item_forproductit()   

#other wizard
class tms_wizard_oa_forother(osv.osv_memory):
    _name = "tms.wizard.oa.forother"
    _inherit = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item.forother", "wizard_id", string="Wizard"),
    }
tms_wizard_oa_forother()

class tms_wizard_item_forother(osv.osv_memory):
    _name = "tms.wizard.item.forother"
    _description = "FeeBase Item"
    _columns = {
        "wizard_id":fields.many2one('tms.wizard.oa.forother', string="Wizard", required=True),
        "feebase_id":fields.many2one('tms.feeforother', string="Fee", required=True),
    }
tms_wizard_item_forother()   
