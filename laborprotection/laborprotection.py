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
        oldscore = self.read(cr, uid, ids, ["score"])[0]["score"]
        emp_id = super(Employee, self).write(cr, uid, ids, values, context)
        if emp_id:
            self.__createRechareItem(cr,uid,ids[0],oldscore,values["score"])
        return emp_id
    
    _sql_constraints = [('cardnum_uniq', 'unique(cardnum)', 'Card Number must be unique!')]
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
