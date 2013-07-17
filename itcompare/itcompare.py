# -*- coding: utf-8 -*-
from openerp.osv import fields,osv

class product_brand(osv.osv):
    """
    品牌
    """
    _name='itcompare.product_brand'
    
    _columns = {
        'name':fields.char(string="Brand Name",size=100,required=True),
        'image':fields.binary(string="Logo",help="Please upload brand icon"),
        'remark':fields.char(string="Remark",size=300)
    }
    
product_brand()

class product_category(osv.osv):
    """
    产品分类
    """
    _name="itcompare.product_category"
    _columns={
        'name':fields.char(string="Category Name",size=100,required=True,translate=True),
        'remark':fields.char(string="Remark",size=300),
        'product_attr_type':fields.one2many('itcompare.product_attr_type','categoryid',string="Product Attributes")        
    }
product_category()

class product_attr_type(osv.osv):
    """
    产品属性分类
    """
    _name="itcompare.product_attr_type"
    _columns={
        'name':fields.char(string="Name",size=100,required=True),
        'categoryid':fields.many2one('itcompare.product_category',string="Category"),
        'product_attr':fields.one2many('itcompare.product_attr','product_attr_type_id','产品属性分类'),
        'remark':fields.char(string="Remark",size=300)
    }
product_attr_type()

class product_attr(osv.osv):
    """
    产品属性
    """
    _name="itcompare.product_attr"
    
    def _get_product_type_name(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids,'None')
        for item in self.browse(cr,uid,ids,context):
            res[item.id]=item.product_attr_type_id.categoryid.name+'/'+item.product_attr_type_id.name+'/'+item.name
        return res     
    
    def _get_product_format_name(self, cr, uid, ids, odometer_id, arg, context):
        res = dict.fromkeys(ids,'None')
        for item in self.browse(cr,uid,ids,context):
            res[item.id]=item.product_attr_type_id.categoryid.name+'/'+item.product_attr_type_id.name+'/'+item.name
        return res      
    
    _columns={
        'name':fields.char(string="Name",size=100,required=True),
        'formatname':fields.function(_get_product_format_name,type="string",string="Format Name"),
        'value':fields.char(string="Value",size=300),
        'product_attr_type_id':fields.many2one('itcompare.product_attr_type',string="Product Attribute"),        
        'product_attr_type_name':fields.function(_get_product_type_name,type="string",string="Product Attribute Type Name")
    }
product_attr()

class product_field(osv.osv):
    """
    产品的一个字段
    """
    _name="itcompare.product_field"
    _columns={
        #"name":fields.char(string="Name",size=100),
        "product_id":fields.many2one("itcompare.product",string="Product"),
        "product_attr":fields.many2one("itcompare.product_attr",string="Attribute Name"),
        "value":fields.char(string="Value",size=300)
    }
product_field()

class product(osv.osv):
    """
    产品
    """
    _name="itcompare.product"
    def on_change_category(self, cr, uid, ids, product_category_id, context=None):
        if not product_category_id:
            return {}        
        #when update should remove old fileds 
        print "product_category_id=%s"%product_category_id
        product_attr =self.pool.get('itcompare.product_attr')
        product_field = self.pool.get('itcompare.product_field')
        attrids = product_attr.search(cr, uid, [('product_attr_type_id.categoryid','=',product_category_id)])
        attrs = product_attr.browse(cr,uid,attrids)
        if not attrs:
            return {}
        product_fields = []
        for attr in attrs:            
            #field = product_field.create(cr,uid,{'product_attr':attr.id,'value':'None'})            
            #product_fields.append(field)
            product_fields.append({
                "product_attr":attr.id,
                "value":"None"
            })                
        print product_fields
        return {
            'value': {
                'product_fields': product_fields,                
            }
        }
        
    _columns={
        "name":fields.char(string="Product Name",size=100,required=True),
        "product_category":fields.many2one("itcompare.product_category",string="Product Category"),
        "product_brand":fields.many2one("itcompare.product_brand",string="Product Brand"),
        "product_fields":fields.one2many("itcompare.product_field","product_id",string="产品字段"),
        "remark":fields.char(string="Remark",size=300)
    }
product()

