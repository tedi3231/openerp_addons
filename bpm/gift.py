from openerp.osv import osv,fields

class GiftProcess(osv.Model):
    _name='bpm.process.giftprocess'
    _inherit='bpm.processbase'
    _columns={
        'giftname':fields.char(string="Gift Name",size=100,requried=True)
    }

    _defaults = {
        'processname':'giftapplication'
    }

class Gift(osv.Model):
    _name='bpm.process.gift'
    def _amount_calc(self,cr,uid,ids,field,arg,context=None):
        res={}
        records = self.browse(cr,uid,ids,context=context)
        for record in records:
            if record:
                res[record.id] = record.inventory*record.price
        return res

    _columns={
        'name':fields.char(string="Name",size=200,requried=True,translate=True),
        'price':fields.float(string="Price",digits=(10,2),requried=True),
        'inventory':fields.integer(string="Inventory",requried=True),
        'amount':fields.function(_amount_calc,type='float'),
        'remark':fields.char(string="Remark",size=200,requried=False)
    }

    def _check_inventory(self,cr,uid,ids):
        items = self.read(cr,uid,ids,['inventory'])
        print items
        if not items:
            return False
        print 'inventory is %s,less than zero %s'%  (items[0]['inventory'],items[0]['inventory']<=0)
        if items[0]['inventory']<=0:
            return False
        return True
    
    _constraints=[(_check_inventory,'Inventory can not be less than zero!',['inventory'])]

class ApplyGift(osv.Model):
    _name='bpm.process.applygift'
    _columns={
        'processid':fields.many2one('bpm.process.giftprocess','Process Name'),
        'giftid':fields.many2one('bpm.process.gift','Gift'),
        'applycount':fields.integer(string="Apply Count",requried=True),
    }
