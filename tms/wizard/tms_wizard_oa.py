from openerp.osv import fields, osv
from openerp.tools.translate import _

class tms_wizard_oa(osv.osv_memory):
    _name = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item", "wizard_id", string="Wizard"),
        'oanum': fields.char(string='OANum',size=50, required=True),
        'feetype':fields.char(string="Feetype",size=100,)
    }
    
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
                'feetype':active_model,
            })
        return {'feebase_ids':res,'feetype':active_model}
    
    def setoanum(self, cr, uid, ids,context=None):
        print context
        active_model = context.get("active_model",None)
        wizard = self.browse(cr,uid,ids,context)[0]
        fees = wizard.feebase_ids
        feebase=self.pool.get(active_model)
        for item in fees:
            feebase.write(cr,uid,item.feebase_id.id,{"state":"hasoa","oanum":wizard.oanum})            
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
    _description = "FeeBase Item"
    _columns = {
        "wizard_id":fields.many2one('tms.wizard.oa.forsend', string="Wizard", required=True),
        "feebase_id":fields.many2one('tms.feeforsend', string="Fee", required=True),
    }
tms_wizard_item_forsend()    
