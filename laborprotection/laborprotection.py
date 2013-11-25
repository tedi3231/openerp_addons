# -*- coding: utf-8 -*-
import datetime
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _

class Employee(osv.osv):
    _name = "laborprotection.employee"

    _columns = {
        "name":fields.char(string="员工名称", required=True, size=200, help="员工名称"),
        "cardnum":fields.char(string="员工卡卡号", required=True, size=100, help="员工卡卡号"),
        "sex":fields.selection([('female', '男'), ('male', '女')], string="员工性别", required=False, help="员工性别"),
        "position":fields.char(string="现在职位", required=False, size=100, help="职位"),
        "telephone":fields.char(string="联系电话", required=False, size=100),
        "email":fields.char(string="邮件地址", required=False, size=100),
        "score":fields.integer(string="当前积分", required=True, help="当前可用分值"),
        "active":fields.boolean(string="是否激活"),
        "remark":fields.text(string="备注")
    }
    
    def __createRechareItem(self,cr,uid,emp_id,oldscore,newscore):
        emp =  self.read(cr,uid,[emp_id],["name","score"])[0]
        emp_name = emp["name"]
        rep = self.pool.get("laborprotection.rechargeitem")
        itemid = rep.create(cr, uid, {"employee_id":emp_id,
            "adduser_id":uid,
            "addvalue":newscore - oldscore,
            "name":emp_name,
        })
        print "itemid is %d" % itemid
    
    def create(self, cr, uid, data, context=None):
        emp_id = super(Employee, self).create(cr, uid, data, context=context)
        if emp_id:
            self.__createRechareItem(cr,uid,emp_id,0,data["score"])
        return emp_id
    
    def write(self, cr, uid, ids, values, context=None):
        print "context is %s" % context
        oldscore = self.read(cr, uid, ids, ["score"])[0]["score"]
        emp_id = super(Employee, self).write(cr, uid, ids, values, context)
        if emp_id:
            if not context.get("isoutstock",False):
                self.__createRechareItem(cr,uid,ids[0],oldscore,values["score"])
        return emp_id
    
    _sql_constraints = [('cardnum_uniq', 'unique(cardnum)', 'Card Number must be unique!')]
    
    _defaults = {
        "active":lambda self,cr,uid,context: True,
    }
    
Employee()

class RechargeItem(osv.osv):
    """
    员工的充值记录
    """
    _name = "laborprotection.rechargeitem"
    
    def get_employee_name(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, 'None')
        for item in self.browse(cr, uid, ids, context=context):
            result[item.id] = item.employee_id.name
        return result
    
    _columns = {
        "name":fields.char(string="充值记录",size=200),
        "adduser_id":fields.many2one("res.users", string="添加人"),
        "employee_id":fields.many2one("laborprotection.employee", string="员工"),
        "employee_name":fields.function(get_employee_name, string="员工名称", type="char", store=True),
        "addvalue":fields.integer(string="添加分值"),
        "addtime":fields.datetime(string="添加时间"),
    }
    
    _order="addtime desc, employee_id asc"

    
    _defaults = {
        "addtime":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
RechargeItem()

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

    _name = "laborprotection.category"
    _description = "产品分类"
    _columns = {
        'name': fields.char('分类名称', size=64, required=True, translate=True, select=True),
        'complete_name': fields.function(_name_get_fnc, type="char", string='产品全称'),
        'parent_id': fields.many2one('laborprotection.category','父类型', select=True, ondelete='cascade'),
        'child_id': fields.one2many('laborprotection.category', 'parent_id', string='子类型'),
        'sequence': fields.integer('序号', select=True, help="Gives the sequence order when displaying a list of product \
                                                             categories."),
        "remark":fields.text(string="备注")
        #'type': fields.selection([('view','View'), ('normal','Normal')], 'Category Type', help="A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
        #'parent_left': fields.integer('Left Parent', select=1),
        #'parent_right': fields.integer('Right Parent', select=1),
    }

    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('select distinct parent_id from laborprotection_category where id IN %s',(tuple(ids),))
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
    _name = "laborprotection.product"

    _columns = {
        "category_id":fields.many2one("laborprotection.category",string="产品类型",required=True,ondelete="cascade",select=True),
        "name":fields.char(string="产品名称",required=True,size=200),
        "supplier":fields.char(string="供应商名称",required=False,size=200),
        "code":fields.char(string="产品编码",required=True,size=200),
        "price":fields.float(string="产品价格",digits=(12,2)),
        "score":fields.integer("产品分值",required=True),
        "stock":fields.integer("产品库存",required=True),
        "addtime":fields.datetime(string="创建时间"),
        "remark":fields.text(string="备注"),
    }
    _defaults = {
        "addtime":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
Product()


class InStockItem(osv.osv):
    """
    入库项
    """
    _name = "laborprotection.instockitem"


    def get_product_name(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, 'None')
        for item in self.browse(cr, uid, ids, context=context):
            result[item.id] = item.product_id.name
        return result

    def create(self, cr, uid, data, context=None):
        """
        创建入库项成功后将对应的产品个数更新
        """
        instock_id = super(InStockItem, self).create(cr, uid, data, context=context)
        if instock_id:
            proItem = self.pool.get("laborprotection.product").read(cr,uid,[data['product_id']],["stock"])
            self.pool.get("laborprotection.product").write(cr,uid,[data['product_id']],{'stock':proItem[0]['stock'] + data['incount']})
        
        return instock_id

    _columns = {
        "product_id":fields.many2one("laborprotection.product",string="入库产品",required=True),
        "name":fields.function(get_product_name,string="产品名称"),
        "incount":fields.integer(string="入库数量"),
        "addtime":fields.datetime(string="入库时间"),
        "adduser_id":fields.many2one("res.users",strin="入库人"),
        "remark":fields.text(string="备注"),
    }
    
    _defaults = {
        "addtime":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "adduser_id":lambda self,cr,uid,context:uid,
    }
InStockItem()

class OutStockItem(osv.osv):
    """
    出库项
    """
    _name = "laborprotection.outstockitem"
    

    def create(self, cr, uid, data, context=None):
        """
        创建出库项成功后将对应的产品个数更新
        """
        #判断用户是否有足够的分值
        empRep = self.pool.get("laborprotection.employee")
        empItem = empRep.read(cr,uid,[data["receiveemp_id"]],['id','score'])
        proRep = self.pool.get("laborprotection.product")
        proItem = proRep.read(cr,uid,[data['product_id']],["score","stock"])

        if proItem[0]['stock'] < data['outcount']:
            raise osv.except_osv(_("Operation Canceld"),u"对不起，产品数量不足，无法认领!")

        totalScore = data['outcount'] * proItem[0]['score']
        if empItem[0]['score'] < totalScore:
            raise osv.except_osv(_("Operation Canceld"),u"对不起，您的积分不足，无法认领!")
        
        outstock_id = super(OutStockItem, self).create(cr, uid, data, context=context)
        if outstock_id:
            #减少库存
            proRep.write(cr,uid,[data['product_id']],{'stock':proItem[0]['stock'] - data['outcount']})
            #减少用户的分值
            if not context:
                context = {}
            context["isoutstock"]=True
            empRep.write(cr,uid,[data['receiveemp_id']],{'score':empItem[0]['score'] - totalScore},context=context)
        return outstock_id

    def get_product_name(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, 'None')
        for item in self.browse(cr, uid, ids, context=context):
            result[item.id] = item.product_id.name
        return result

    _columns = {
        "product_id":fields.many2one("laborprotection.product",string="出库产品",required=True),
        "name":fields.function(get_product_name,string="产品名称"),
        "outcount":fields.integer(string="出库数量"),
        "adduser_id":fields.many2one("res.users",strin="出库人"),
        "receiveemp_id":fields.many2one("laborprotection.employee",string="领料人"),
        "addtime":fields.datetime(string="出库时间"),
        "remark":fields.text(string="备注"),
    }
    
    _defaults = {
        "addtime":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "adduser_id":lambda self,cr,uid,context:uid,
    }
OutStockItem()

class Claim(osv.osv):
    """
    领料记录
    """
    _name = "laborprotection.claim"

    def on_change_employee(self,cr,uid,ids,emp_id,context=None):
        if not emp_id:
            return False
        item = self.pool.get("laborprotection.employee").browse(cr,uid,emp_id,context=context)
        if not item :
            return False
        return {
            "value":{
                "currentscore":item.score,
            }
        }

    def on_change_claimitemids(self,cr,uid,ids,itemids,context=None):
        if not itemids:
            return False
        for item in itemids:
            print item
        proRep = self.pool.get("laborprotection.product")
        totalscore = sum([item[2]["outcount"] * proRep.read(cr,uid,[item[2]["product_id"]],["score"])[0]["score"] for item in itemids])
        totalproductCount = sum([item[2]["outcount"] for item in itemids])
        #item = self.pool.get("laborprotection.employee").browse(cr,uid,emp_id,context=context)
        #if not item :
        #    return False
        return {
            "value":{
                "totalscore":totalscore,
                "totalcount":totalproductCount,
            }
        }

    def get_product_totalcount(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, 'None')
        for item in self.browse(cr, uid, ids, context=context):
            total = sum([citem.outcount for citem in item.claimitem_ids])
            result[item.id] = total
        return result

    def get_totalscore(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, 'None')
        for item in self.browse(cr, uid, ids, context=context):
            total = sum([citem.outcount*citem.product_id.score for citem in item.claimitem_ids])
            result[item.id] = total
        return result

    _columns = {
        "name":fields.related("employee_id","name",type="char",string="名称"),
        "employee_id":fields.many2one("laborprotection.employee",string="领料人"),
        "currentscore":fields.related("employee_id","score",type="integer",string="当前积分",readonly=True),
        "claimitem_ids":fields.one2many("laborprotection.claimitem","claim_id",string="领料详细"),
        "adduser_id":fields.many2one("res.users",string="操作人"),
        "addtime":fields.datetime(string="领料时间"),
        "totalscore":fields.function(get_totalscore,string="共需积分"),
        "totalcount":fields.function(get_product_totalcount,string="产品总数"),
        "remark":fields.text(string="备注"),
    }
    _defaults = {
        "addtime":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "adduser_id":lambda self,cr,uid,context:uid,
    }
Claim()

class ClaimItem(osv.osv):
    """
    领料详细
    """
    _name = "laborprotection.claimitem"

    def get_product_name(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, 'None')
        for item in self.browse(cr, uid, ids, context=context):
            result[item.id] = item.product_id.name
        return result

    _columns = {
        "claim_id":fields.many2one("laborprotection.claim",string="领料记录"),
        "product_id":fields.many2one("laborprotection.product",string="出库产品",required=True),
        "name":fields.related("product_id","name",type="char",string="产品名称"),
        "outcount":fields.integer(string="出库数量"),
        "adduser_id":fields.many2one("res.users",strin="操作人"),
        "addtime":fields.datetime(string="出库时间"),
        "remark":fields.text(string="备注"),
    }

    _defaults = {
        "addtime":lambda self, cr, uid, context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "adduser_id":lambda self,cr,uid,context:uid,
    }

ClaimItem()