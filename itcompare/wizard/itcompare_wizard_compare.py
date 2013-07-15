from openerp.osv import fields, osv

class itcompare_wizard_compare(osv.TransientModel):
    _name = "itcompare.wizard.compare"
    _description = "compare product"    

    _columns = {
        "product_ids":fields.one2many("itcompare.wizard.compareitem","wizard_id",string="Products"),        
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context == None:
            context = {}            
        product_ids = context.get('active_ids',[])
        wizard_id = context.get('acvite_id',None)
        res=[]
        products = self.pool.get('itcompare.product').browse(cr,uid,product_ids,context=context)
        print products
        for pitem in products:
            res.append({
                'wizard_id':wizard_id,
                'productid':pitem.id
            })
        return {'product_ids':res}
    
    def compare(self,cr,uid,ids,context=None):
        wizard = self.browse(cr,uid,ids,context)[0]
        if not wizard:
            return False
        products= [item.productid for item in wizard.product_ids]
        #must be two products or more to comare
        if len(products)<=1:
            return False
        #must be some Category
        if products[0].product_category.id !=products[1].product_category.id:
            return False

        product_attrtypes = [item for item in  products[0].product_category.product_attr_type]
        product_attrs =[]
        for item in product_attrtypes:
            product_attrs.extend(item.product_attr)
        attrids = [item.id for item in product_attrs]
        #for item in product_attrs:
        #    print item.name,item.formatname
        result = []
        for pitem in products:
            row = {}
            #init one row with all attributes
            for attritem in product_attrs:
                row[attritem.name]="None"

            for field in pitem.product_fields:
                if field.product_attr.id in attrids:
                    row[field.product_attr.name] = field.value
            result.append(row)
        from xlwt import Workbook
        book=Workbook()
        sheet1=book.add_sheet(products[0].product_category.name)
        colindex =1
        for pitem in products:
            sheet1.write(0,colindex,pitem.name)
            colindex=colindex+1
        rowindex=1
        for key in result[0].keys():
            colindex=0
            sheet1.write(rowindex,colindex,key)
            for row in result:
                colindex=colindex+1
                sheet1.write(rowindex,colindex,row[key])
            rowindex=rowindex+1
        book.save("/Users/tedi/demo.xls")
        return False 
    
itcompare_wizard_compare()

class itcompare_wizard_compareitem(osv.TransientModel):
    _name="itcompare.wizard.compareitem"
    _description="compareitem"
    _columns ={
        "wizard_id":fields.many2one('itcompare.wizard.compare',string="Wizard",required=True),
        "productid":fields.many2one('itcompare.product',string="Product",required=True),        
    }
itcompare_wizard_compareitem()    
