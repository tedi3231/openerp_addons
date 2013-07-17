from openerp.osv import fields, osv
from openerp.tools.translate import _

class itcompare_wizard_compare(osv.osv_memory):
    _name = "itcompare.wizard.compare"
    _description = "compare product"    

    _columns = {
        "product_ids":fields.one2many("itcompare.wizard.compareitem", "wizard_id", string="Products"),
        'data': fields.binary('File', readonly=True),
        'name': fields.char('Filename', 16, readonly=True),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context == None:
            context = {}            
        product_ids = context.get('active_ids', [])
        wizard_id = context.get('acvite_id', None)
        res = []
        products = self.pool.get('itcompare.product').browse(cr, uid, product_ids, context=context)
        print products
        for pitem in products:
            res.append({
                'wizard_id':wizard_id,
                'productid':pitem.id
            })
        return {'product_ids':res}
    
    def compare(self, cr, uid, ids, context=None):
        wizard = self.browse(cr, uid, ids, context)[0]
        if not wizard:
            return False
        products = [item.productid for item in wizard.product_ids]
        #must be two products or more to comare
        if len(products) <= 1:
            return False
        #must be some Category
        if products[0].product_category.id != products[1].product_category.id:
            raise osv.except_osv(_('Not same category !'),_("You must select products which have same product category !") )
            #return False

        product_attrtypes = [item for item in products[0].product_category.product_attr_type]
        product_attrs = []
        for item in product_attrtypes:
            product_attrs.extend(item.product_attr)
        attrids = [item.id for item in product_attrs]
        #for item in product_attrs:
        # print item.name,item.formatname
        result = []
        for pitem in products:
            row = {}
            #init one row with all attributes
            for attritem in product_attrs:
                row[attritem.name] = "None"

            for field in pitem.product_fields:
                if field.product_attr.id in attrids:
                    row[field.product_attr.name] = field.value
            result.append(row)
        from xlwt import Workbook
        book = Workbook()
        sheet1 = book.add_sheet(products[0].product_category.name)
        colindex = 1
        
        for pitem in products:
            sheet1.write(0, colindex, pitem.name)
            colindex = colindex + 1        
        
        rowindex = 1
        for key in result[0].keys():
            colindex = 0
            sheet1.write(rowindex, colindex, key)
            for row in result:
                colindex = colindex + 1
                sheet1.write(rowindex, colindex, row[key])
            rowindex = rowindex + 1
        #book.save("/home/tedi3231/demo.xls")
        
        import base64  
        import StringIO
        file_data=StringIO.StringIO()
        o=book.save(file_data)       
        out=base64.encodestring(file_data.getvalue())
             
        attachmentid = self.pool.get("ir.attachment").create(cr,uid,{
            "name":'_'.join(([pitem.name for pitem in products]))+"_compareresult.xls" ,
            "res_model":"itcompare.product",
            "datas_fname":"itcompare.product.compare.xls",
            "description":"Compare product file",
            "type":"binary",
            "datas":out
        })
        print "str(attachmentid) =%s"% str(attachmentid)
        return {
                'domain': "[('id','=','"+str(attachmentid)+"')]",
                'name': 'Compare Results',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'ir.attachment',                
                'context': "{}",
                'type': 'ir.actions.act_window'
        }        
        
itcompare_wizard_compare()

class itcompare_wizard_compareitem(osv.osv_memory):
    _name = "itcompare.wizard.compareitem"
    _description = "compareitem"
    _columns = {
        "wizard_id":fields.many2one('itcompare.wizard.compare', string="Wizard", required=True),
        "productid":fields.many2one('itcompare.product', string="Product", required=True),
    }
itcompare_wizard_compareitem()    
