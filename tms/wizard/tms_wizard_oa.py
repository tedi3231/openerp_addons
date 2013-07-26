from openerp.osv import fields, osv
from openerp.tools.translate import _

class tms_wizard_oa(osv.osv_memory):
    _name = "tms.wizard.oa"
    _description = "Set oa"    

    _columns = {
        "feebase_ids":fields.one2many("tms.wizard.item", "wizard_id", string="Wizard"),
        'oanum': fields.char(string='OANum',size=50, required=True),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context == None:
            context = {}            
        wizard_id = context.get('acvite_id', None)
        res = []
        product_ids = context.get('active_ids', [])
        products = self.pool.get('tms.feebase').browse(cr, uid, product_ids, context=context)
        for pitem in products:
            res.append({
                'wizard_id':wizard_id,
                'feebase_id':pitem.id
            })
        return {'feebase_ids':res}
    
    def setoanum(self, cr, uid, ids,context=None):
        wizard = self.browse(cr,uid,ids,context)[0]
        #print "setoanum() params ids is %s,context is %s"%(ids,context)
        print 'wizard is %s '%wizard
        fees = wizard.feebase_ids
        print 'fees list is %s'%fees
        feebase=self.pool.get("tms.feebase")
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
