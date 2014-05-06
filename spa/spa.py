# -*- coding: utf-8 -*-
#from openerp.addons.crm import crm
from datetime import datetime
from openerp.osv import fields,osv
from openerp import tools
from openerp.tools.translate import _
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

class  Employee(osv .osv):
    _inherit = 'hr.employee'

    _columns = {
        'store_id':fields.many2one("spa.store","Store",required=True),
    }

Employee()
# HR  END

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
    """
    扩展客户的信息
    """
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

    def _default_attribute_values(self,cr,uid,context=None):
        attr_values = []
        attr_rep = self.pool.get('spa.customer.attribute')
        attr_ids = attr_rep.search(cr,uid,[])
        attributes = self.pool.get('spa.customer.attribute').browse(cr,uid,attr_ids)
        for attr in attributes:
            attr_values.append({
                'name': attr.name,
                'customer_attribute_id' : attr.id,
            })
        return attr_values

    _defaults = {
        'attribute_values' : _default_attribute_values,
    }

SPA_RESERVATION_FIELDS_TO_MERGE = [
    'name',
    #'partner_id',
    #'store_id',
    #'emp_id',
    'remark',
]

SPA_RESERVATIONLINE_FIELDS_TO_MERGE = [
    #'product_id',
    'price',
    'unit',
    'count',
    'amount'
]

class Reservation(osv.osv):
    """
    客户预约
    """
    _name = "spa.reservation"

    _columns = {
        #'name' : fields.char(string="Name"),
        'name' : fields.related("partner_id","name", type="char", string="Name"),
        'partner_id' : fields.many2one('res.partner',string="Customer",required=True,domain="[('customer','=',1)]"),
        'store_id' : fields.many2one('spa.store', string = "Store" ,required = True ),
        'emp_id' : fields.many2one('hr.employee', string = "Employee", domain="[('store_id','=',store_id)]"),
        'reservationdate' : fields.datetime(string = "Reservation Date",required=True),
        'remark' : fields.char(string = "Remark"),
        'reservationlines': fields.one2many('spa.reservationline','reservation_id',string="Reservation Lines"),
        'state' : fields.selection([('draft','Draft'),('cancel','Cancel'),('complete','Complete')],string="State", readonly=True),
    }
    
    def redirect_oder_view(self,cr,uid,ids,order_id,context=None):
        models_data = self.pool.get('ir.model.data')
        dummy, form_view = models_data.get_object_reference(cr,uid,'spa','view_order_form')
        dummy, tree_view = models_data.get_object_reference(cr,uid,'spa','view_order_tree')
        return {
            'name' : _('Order'),
            'view_type' : 'form',
            'view_mode' : 'tree,form',
            'res_model' : 'spa.order',
            'res_id'  : int(order_id),
            'view_id' : False,
            'views' : [(form_view or False,'form'),
                       (tree_view or False,'tree')
                      ],
            'type' : 'ir.actions.act_window'
        }
        

    def reservation_complete(self,cr,uid,ids,context=None):
        print 'complete reservation'
        item = self.browse(cr,uid,ids,context=context)[0]
        order_item = {'orderlines':[]}
        order_lines = []

        for key in SPA_RESERVATION_FIELDS_TO_MERGE:
            order_item[key] = item[key]
        for line in item.reservationlines:
            order_line = {}
            for key in SPA_RESERVATIONLINE_FIELDS_TO_MERGE:
                order_line[key] = line[key]
            order_line['product_id'] = line['product_id'].id
            order_lines.append(order_line)
            
        order_item['partner_id'] = item['partner_id'].id
        order_item['store_id'] = item['store_id'].id
        order_item['emp_id'] = item['emp_id'].id

        order_item['source'] = 'reservation'
        order_item['ordernum'] = datetime.now().strftime('%Y%m%S')
        
        print 'convert to order form reservation %s ' % order_item
        print 'orderlines is %s ' % order_item['orderlines']
        
        order_id = self.pool.get('spa.order').create(cr,uid,order_item,context=context)
        for line in order_lines:
            line["order_id"] = order_id
            self.pool.get("spa.orderline").create(cr,uid,line,context=context)
        
        self.write(cr,uid,ids,{'state':'complete'},context=context)
        return self.redirect_oder_view(cr,uid,ids,order_id,context=context)
        
    def reservation_cancel(self,cr,uid,ids,context=None):
        return self.write(cr,uid,ids,{'state':'cancel'},context=context)

    _defaults = {
        'state':lambda self,cr,uid,context:'draft',
    }
Reservation()

class ReservationLine(osv.osv):
    """
    客户预约的产品记录
    """
    _name = "spa.reservationline"

    def _get_reservation_line_amount(self,cr,uid,ids,name,args,context=None):
        result = dict.fromkeys(ids,'None')
        for item in self.browse(cr,uid,ids,context = context ):
            total = item.product_id.price * item.count
            result[item.id] = total
        return result

    def product_id_change(self,cr,uid,ids,product_id,context=None):
        print "product_id_change ,ids is %s product_id %s" % (ids,product_id)
        products = self.pool.get("spa.product").browse(cr,uid,[product_id])
        return {
            "value":{
                "price" : products[0].price,
                "unit" : products[0].unit,
            }
        }

    def product_count_change( self,cr, uid, ids, price, count, context = None ):
        print "product_count_change %s %s " %(price,count) 
        return {
            "value": {
                "amount" : price * count,
            }
        }

    _columns = {
        #"name":fields.related("product_id","name",type="string",string="Name"),
        "reservation_id": fields.many2one("spa.reservation", string="Reservation"),
        "product_id" : fields.many2one( "spa.product", string="Product"),
        "price" : fields.float(string="Price",required=True),
        "unit" : fields.char(string="Unit"),
        "count":fields.integer(string="Product Count",required = True),
        "amount" : fields.float(string="Amount"),
        #"amount" : fields.function(_get_reservation_line_amount, string="Amount"),
    }
ReservationLine()



class Order(osv.osv):
    """
    客户订单
    """
    _name = "spa.order"

    def _amount_calc( self, cr, uid, ids, field, arg, context = None):
        res = {}
        for item in self.browse(cr,uid,ids,context=context):
            sum_amount = sum([line.price * line.count for line in item.orderlines])
            res[item.id] = sum_amount
        return res

    _columns = {
        'name' : fields.related("partner_id","name", type="char", string="Name"),
        'ordernum': fields.char(string="Order Number",type="char", required= True),
        'partner_id' : fields.many2one('res.partner',string="Customer",required=True,domain="[('customer','=',1)]"),
        'store_id' : fields.many2one('spa.store', string = "Store" ,required = True ),
        'emp_id' : fields.many2one('hr.employee', string = "Employee", domain="[('store_id','=',store_id)]"),
        'orderlines': fields.one2many('spa.orderline','order_id',string="Order Lines"),
        'source':fields.selection([("reservation","Reservation"),("reception","Reception")],string="Source",),
        'remark' : fields.char(string = "Remark"),
        'amount' : fields.function(_amount_calc, string = "Amount", type = "float"),
        'orderdate':fields.datetime(string="OrderDate",required = True),
        'state' : fields.selection([('draft','Draft'),('cancel','Cancel'),('complete','Complete')],string="State", readonly=True),
    }
    
    _defaults = {
        'state':lambda self,cr,uid,context:'draft',
        'orderdate': lambda self,cr,uid,context: datetime.now(),
    }
Order()

class OrderLine(osv.osv):
    """
    客户订单的产品记录
    """
    _name = "spa.orderline"

    def _get_order_line_amount(self,cr,uid,ids,name,args,context=None):
        result = dict.fromkeys(ids,'None')
        for item in self.browse(cr,uid,ids,context = context ):
            total = item.product_id.price * item.count
            result[item.id] = total
        return result

    def product_id_change(self,cr,uid,ids,product_id,context=None):
        print "product_id_change ,ids is %s product_id %s" % (ids,product_id)
        products = self.pool.get("spa.product").browse(cr,uid,[product_id])
        return {
            "value":{
                "price" : products[0].price,
                "unit" : products[0].unit,
            }
        }

    def product_count_change( self,cr, uid, ids, price, count, context = None ):
        print "product_count_change %s %s " %(price,count) 
        return {
            "value": {
                "amount" : price * count,
            }
        }

    _columns = {
        #"name":fields.related("product_id","name",type="string",string="Name"),
        "order_id": fields.many2one("spa.order", string="Order"),
        "product_id" : fields.many2one( "spa.product", string="Product"),
        "price" : fields.float(string="Price",required=True),
        "unit" : fields.char(string="Unit"),
        "count":fields.integer(string="Product Count",required = True),
        "amount" : fields.float(string="Amount"),
        #"amount" : fields.function(_get_reservation_line_amount, string="Amount"),
    }
OrderLine()

#----------------------------------------------------------
# Categories
#----------------------------------------------------------
class Category(osv.osv):
    
    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1]+' / '+name
            res.append((record['id'], name))
        return res

    def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
        res = self.name_get(cr, uid, ids, context=context)
        return dict(res)

    _name = "spa.category"
    _description = "产品分类"
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True, select=True),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'parent_id': fields.many2one('spa.category','Parent', select=True, ondelete='cascade'),
        'child_id': fields.one2many('spa.category', 'parent_id', string='Children'),
        'sequence': fields.integer('Sequence', select=True, help="Gives the sequence order when displaying a list of product \
                                                             categories."),
        "remark":fields.text(string="Remark")
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from spa_category where id IN %s',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, '错误！您不能循环创建目录.', ['parent_id'])
    ]

    def child_get(self, cr, uid, ids):
        return [ids]

Category()

class Product(osv.osv):
    _name = "spa.product"

    _columns = {
        "category_id":fields.many2one("spa.category",string="Category",required=True,ondelete="cascade",select=True),
        "name":fields.char(string="Name",required=True,size=200),
        "price":fields.float(string="Price",digits=(12,2)),
        "unit" : fields.char(string="Unit", required = True),
        "remark":fields.text(string="Remark"),
    }
    _defaults = {
    }
Product()
