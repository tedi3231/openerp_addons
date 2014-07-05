# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools

class Shop(osv.osv):
    _name = "shop.shop"
    #_table = "shop_shop"

    _columns = {
        "name":fields.char(string="Name",required=True,size=100),
        "address":fields.char(string="Address",required=True,size=500),
        "state":fields.selection([("run","Run"),("stop","Stop")],string="State"),
    }

    _defaults = {
        "state":"run",
    }
Shop()

class Worker(osv.osv):
    _name = "shop.worker"

    def _cal_fullname(self,cr,uid,ids,field,arg,context=None):
        result = {}
        for item in self.browse(cr,uid,ids):
            result[item.id] = "%s %s" %(item.firstname,item.lastname)
        return result

    def get_shop_name(self,cr,uid,ids,shop_id,context=None):
        if not shop_id:
            return False
        shopRep = self.pool.get("shop.shop")
        item = shopRep.browse(cr,uid,[shop_id])
        print item
        return {
            "value":{
                "shopname":item[0].name,
            }
        }

    _columns = {
        #"name":fields.char(string="Full Name", size=100,required=True),
        "name":fields.function(_cal_fullname,type="char",string="Full Name"),
        "lastname":fields.char(string="Last Name", size=50,required=True),
        "firstname":fields.char(string="First Name", size=50,required=True),
        "shop_id":fields.many2one("shop.shop",string="Shop"),
        #"shopname":fields.char(string="Shop Name",size=100),
        "shopname":fields.related("shop_id","name",type="char",string="shopname"),
    }
Worker()

class Employee(osv.osv):
    _name = "shop.employee"

    def _get_full_name(self,cr,uid,ids,field,arg,context=None):
        result = {}
        for item in self.browse(cr,uid,ids):
            result[item.id] = "%s-%s" % (item.firstname,item.lastname)
        return result
    
    def get_shop_name(self,cr,uid,ids,model_id,context=None):
        if not model_id:
            return False
        item = self.pool.get("shop.shop").browse(cr,uid,[model_id],context=context)
        if not item:
            return False
        return {
            "value":{
                "shopname":"abc",
            }
        }
        #return {"shopname":"abc"}

    _columns = {
        #"name" : fields.char(string="Name",size=100),
        "name":fields.function(_get_full_name,type="char",string="Name"),
        "firstname":fields.char(string="First Name",size=100,required=True),
        "lastname":fields.char(string="Last Name",size=100,required=True),
        "shopname":fields.char(string="Shop Name",size=100,required=True),
        "shop_id":fields.many2one("shop.shop",string="Shop"),
    }

Employee()
