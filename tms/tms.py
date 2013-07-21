# -*- coding: utf-8 -*-
import datetime
from openerp.osv import fields, osv

class Store(osv.osv):
    _name = "tms.store"
    _columns = {
        "name":fields.char(string="Store Name", required=True, size=200),
        "storenum":fields.char(string="Store num", required=True, size=100),
        "province_id":fields.many2one("res.country.state", string="Province"),
        "address":fields.char(string="Address", size=200, required=True),
        "contactperson":fields.char(string="Contact Person", size=100, required=True),
        "telephone":fields.char(string="Telephone", size=50, required=True),
        "mobile":fields.char(string="Mobile", size=50),
        "netusername":fields.char(string="Net User Name", size=60),
        "netuserpass":fields.char(string="Net User pwd", size=60),
        "dynamicdomain":fields.char(string="Dynamic Domain", size=200),
        "dynamicdomainpass":fields.char(string="Dynamic Domain pass", size=100),
        "dynamicdomainaddress":fields.char(string="Dynamic Domain Address", size=100),
        "dynamicdomainotheraddress":fields.char(string="Domain Other Address", size=100),
        "peanutuserpass":fields.char(string="Peanut User pass", size=100),
        "peanutvalidemail":fields.char(string="Peanut valid email", size=100),
        "peanutemailpass":fields.char(string="Peanut email pass", size=100),
        "poscdk":fields.char(string="POSCDK", size=200),
        "remark":fields.text(string="Remark")
    }
    _sql_constraints = [('storenum_uniq', 'unique(storenum)', 'Storenum must be unique!')]
Store()

class ApplyInfo(osv.osv):
    _name="tms.applyinfo"
    def get_province_name(self,cr,uid,ids,name,args,context=None):
        result=dict.fromkeys(ids,'None')
        for item in self.browse(cr,uid,ids,context=context):
            result[item.id] = item.store_id.province_id.name
        return result

    def get_province_by_store_id(self,cr,uid,store_id,context=None):
        if not store_id:
            return False
        pitem = self.pool.get("tms.store").browse(cr,uid,store_id,context=context)
        if not pitem:
            return False
        return pitem.province_id.name

    def on_change_store(self,cr,uid,ids,model_id,context=None):
        print "model_id=%s" % model_id
        if not model_id:
            return False
        item = self.pool.get("tms.store").browse(cr,uid,model_id,context=context)
        if not item :
            return False
        print item.name
        return {
            "value":{
                "province":self.get_province_by_store_id(cr,uid,item.id),
                "storenum":item.storenum,
                "telephone":item.telephone,
                "mobile":item.mobile,
                "address":item.address,
                "contactperson":item.contactperson
            }
        }

    def _get_default_processid(self,cr,uid,context):
        sequenceid=self.pool.get("ir.sequence").search(cr,uid,[('code','=','tms.applyinfo.processid')])
        sequence = self.pool.get("ir.sequence").browse(cr,uid,sequenceid,context=None)
        return sequence[0].get_id()

    def create(self,cr,uid,data,context=None):
        apply_id = super(ApplyInfo, self).create(cr, uid, data, context=context)
        print "apply_id=%s"%apply_id
        self.write(cr,uid,apply_id,{"processid":self._get_default_processid(cr,uid,context)},context)
        return apply_id

    def name_get(self,cr,uid,ids,context=None):
        res = []
        for item in self.browse(cr,uid,ids,context):
            res.append((item.id,item.processid))
        return res

    _columns = {
        "processid":fields.char(string="ProcessId",size=100,required=False),
        "store_id":fields.many2one("tms.store",string="Sotre"),
        "province":fields.function(get_province_name,type="char",string="Province"),
        "storenum":fields.related("store_id","name",type="char",string="Store Num"),
        "telephone":fields.related("store_id","telephone",type="char",string="telephone"),
        "mobile":fields.related("store_id","mobile",type="char",string="mobile"),
        "address":fields.related("store_id","address",type="char",string="Address"),
        "contactperson":fields.related("store_id","contactperson",type="char",string="Contact Person"),
        "content":fields.text(string="Content",required=True),
        "applyinfoitem_ids":fields.one2many("tms.applyinfoitem","applyinfo_id",string="ApplyInfo Items")
    }

    _defaults={
        #"processid":_get_default_processid,
    }
ApplyInfo()

class ApplyInfoItem(osv.osv):
    _name="tms.applyinfoitem"

    _columns={
        "name":fields.text(string="Remark"),
        "user_id":fields.many2one("res.users",string="Add Man"),
        "create_time":fields.datetime(string="Add time"),
        "applyinfo_id":fields.many2one("tms.applyinfo",string="ApplyInfo"),
    }

    _defaults={
        "user_id":lambda self,cr,uid,context:uid,
        "create_time":lambda self,cr,uid,context:datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
ApplyInfoItem()
