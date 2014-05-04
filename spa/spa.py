# -*- coding: utf-8 -*-
#from openerp.addons.crm import crm
from openerp.osv import fields,osv
from openerp import tools

# HR START 
class Store(osv.osv):
    _name = "spa.store"

    def name_get(self,cr,uid,ids,context=None):
        res=[]
        display_widget=None
        if context:
            display_widget = context.get("display_widget",None)
        for r in self.read(cr,uid,ids,['name','storenum']):
            if display_widget =="dropdownlist":
                res.append((r['id'],'(%s)%s'%(r['storenum'],r['name'])))
            else:
                res.append((r['id'],r['name']))
        return res

    def name_search(self,cr,uid,name="",args=None,operator="ilike",context=None,limit=100):
        if not args:
            args=[]
        if not context:
            context={}
        ids=[]
        if name:
            ids = self.search(cr, uid, [('storenum',operator,name)]+ args, limit=limit, context=context)
        if not ids:
            ids = self.search(cr, uid, [('name',operator,name)]+ args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context=context)

    _columns = {
        "name":fields.char(string="Store Name", required=True, size=200),
        "storenum":fields.char(string="Store num", required=True, size=100),
        "country_id":fields.many2one("res.country", string="Country",store=True,required=True),
        "province_id":fields.many2one("res.country.state", string="Province",store=True,required=True,domain=[('country_id','=',49)]),
        "address":fields.char(string="Address", size=200),
        "contactperson":fields.char(string="Contact Person", size=100),
        "telephone":fields.char(string="Telephone", size=50),
        "mobile":fields.char(string="Mobile", size=50),
        "email":fields.char(string="Email", size=200),
        "xCoordinate":fields.char(string="X", size=200),
        "yCoordinate":fields.char(string="Y", size=200),
        "remark":fields.text(string="Remark")
    }
    _sql_constraints = [('storenum_uniq', 'unique(storenum)', 'Storenum must be unique!')]

Store()

class  Employee(osv.osv):
    _inherit = 'hr.employee'

    _columns = {
        'store_id':fields.many2one("spa.store","Store",required=True),
    }

Employee()
# HR  END


#res_partner()

#CRM START 
#class res_partner(osv.osv):
#    _inherit = "res.partner"
#
#    _columns = {
#        "language":fields.char(string="Language", size="200"),
#        "age": fields.integer(string="Age"),
#        "hasMarried": fields.boolean(string="Has Married"),
#        "hasChildren" : fields.boolean(string="Has Children"),
#        "carbrand": fields.char(string="Car Brand"),
#    }
#
#    _defaults = {
#        'age': lambda *args: 0,
#    }
#CRM END
class spa_customer_attribute_category(osv.osv):
    """
    客户属性分类
    """
    _name="spa.customer.attribute.category"
    _columns={
        'name':fields.char(string="Category Name",size=100,required=True,translate=True),
        'remark':fields.char(string="Remark",size=300),
        'customer_attributes':fields.one2many('spa.customer.attribute','categoryid',string="Customer Attributes")        
    }
spa_customer_attribute_category()

class spa_customer_attribute(osv.osv):
    """
    客户具体属性名称
    """
    _name="spa.customer.attribute"
    _columns={
        'name':fields.char(string="Name",size=100,required=True),
        'categoryid':fields.many2one('spa.customer.attribute.category',string="Category"),
        'remark':fields.char(string="Remark",size=300)
    }
spa_customer_attribute() 

class spa_customer_attribute_value(osv.osv):
    """
    客户具体的属性值
    """
    _name="spa.customer.attribute.value"
    
    def _get_customer_attribute_name(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids,'None')
        for item in self.browse(cr,uid,ids,context):
            res[item.id]=item.customer_attribute_id.categoryid.name+'/'+item.customer_attribute_id.name+'/'+item.name
        return res
    
    _columns={
        'parent_id':fields.many2one("res.partner",string="Customer"),
        'name':fields.char(string="Name",size=100,required=True),
        'formatname':fields.function(_get_customer_attribute_name,type="string",string="Format Name"),
        'value':fields.char(string="Value",size=1000),
        'customer_attribute_id':fields.many2one('spa.customer.attribute',string="Customer Attribute"),        
        'customer_attribute_type_name':fields.function(_get_customer_attribute_name,type="string",string="Customer Attribute Name")
    }
spa_customer_attribute_value()

class res_partner(osv.osv):
    _inherit= 'res.partner'

    _columns = {
        "introducer": fields.many2one("res.partner",string="Introducer",domain="[('customer','=',1),('id','!=',id)]"),
        "language":fields.char(string="Language", size=200),
        "hasMarried": fields.boolean(string="Has Married"),
        "hasChildren" : fields.boolean(string="Has Children"),
        "carbrand": fields.char(string="Car Brand"),
        "age": fields.integer(string="Age"),
        "attribute_values": fields.one2many("spa.customer.attribute.value","parent_id",string="Attributes"),
    }
