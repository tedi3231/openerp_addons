# -*- coding: utf-8 -*-
import datetime
import time
import utildate
from openerp.osv import fields, osv
from openerp.tools.translate import _
class Store(osv.osv):
    _name = "tms.store"

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
        "province_id":fields.many2one("res.country.state", string="Province",store=True,required=True,domain=[('country_id','=',49)]),
        "address":fields.char(string="Address", size=200),
        "contactperson":fields.char(string="Contact Person", size=100),
        "telephone":fields.char(string="Telephone", size=50),
        "mobile":fields.char(string="Mobile", size=50),
        "netusername":fields.char(string="Net User Name", size=60),
        "netuserpass":fields.char(string="Net User pwd", size=60),
        "dynamicdomain":fields.char(string="Dynamic Domain", size=200),
        "dynamicdomainpass":fields.char(string="Dynamic Domain pass", size=100),
        "dynamicdomainaddress":fields.char(string="Dynamic Domain Address", size=100),
        "dynamicdomainotheraddress":fields.char(string="Domain Other Address", size=100),
        "peanutuserpass":fields.char(string="Peanut User pass", size=100),
        "peanutdomain":fields.char(string="花生壳域名",size=100),
        "peanutdomainaddress":fields.char(string="花生壳域名地址",size=100),
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
    
        if not model_id:
            return False
        item = self.pool.get("tms.store").browse(cr,uid,model_id,context=context)
        if not item :
            return False
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

    def _get_default_processid(self,cr,uid,code,context):
        sequenceid=self.pool.get("ir.sequence").search(cr,uid,[('code','=',code)])
        sequence = self.pool.get("ir.sequence").browse(cr,uid,sequenceid,context=None)
        return sequence[0].get_id()

    def create(self,cr,uid,data,context=None):
        apply_id = super(ApplyInfo, self).create(cr, uid, data, context=context)
        print "apply_id=%s"%apply_id
        #print context
        childtypename = type(self).__name__
        print childtypename
        processid = self._get_default_processid(cr,uid,"tms.applyinfo.processid",context)
        state = "unreceived"
        if childtypename=="tms.stopandmoveapplyinfo":
            print "stop and move"
            processid = self._get_default_processid(cr,uid,"tms.stopmoveapplyinfo.processid",context)
            state = "hasconfirm"
        print "create state is %s"% state
        self.write(cr,uid,apply_id,{"state":state,"processid":processid},context)
        #self.write(cr,uid,apply_id,{"state":"hasconfirm"},context)
        return apply_id

    def name_get(self,cr,uid,ids,context=None):
        res = []
        for item in self.browse(cr,uid,ids,context):
            res.append((item.id,item.processid))
        return res
    
    """def write(self,cr,uid,ids,values,context=None):
        print "call write method,parammeter values are %s" % values
        childtypename = type(self).__name__
        if childtypename =="tms.stopandmoveapplyinfo":
            return super(ApplyInfo,self).write(cr,uid,ids,values,context) 

        if self.user_has_groups(cr,uid,"tms.group_tms_applyinfo_factory",context):
            applyinfo_state = set([item.state for item in self.browse(cr,uid,ids,context)])
            current_state = applyinfo_state.pop()
            if len(applyinfo_state)==0 and( current_state=="unreceived" or current_state=='draft'):
                return super(ApplyInfo,self).write(cr,uid,ids,values,context) 
            else:
                raise osv.except_osv(_("Operation Canceld"),u"你只能修改未接收申报!")
        return super(ApplyInfo,self).write(cr,uid,ids,values,context) 
    """
    def unlink(self,cr,uid,ids,context=None):
        childtypename = type(self).__name__
        if childtypename!='tms.stopandmoveapplyinfo' and self.user_has_groups(cr,uid,"tms.group_tms_applyinfo_factory",context):
            applyinfo_state = set([item.state for item in self.browse(cr,uid,ids,context)])
            if len(applyinfo_state)>1 or applyinfo_state.pop()!="unreceived":
                raise osv.except_osv(_("Operation Canceld"),u"你只能删除未接收申报!")
        return super(ApplyInfo,self).unlink(cr,uid,ids,context)

    _columns = {
        "user_id":fields.many2one("res.users",string="Add Man"),
        "processid":fields.char(string="ProcessId",size=100,required=False),
        "store_id":fields.many2one("tms.store",string="Sotre",required=True),
        "province":fields.function(get_province_name,type="char",string="Province",store=True),
        "storenum":fields.related("store_id","storenum",type="char",string="Store Num"),
        "telephone":fields.related("store_id","telephone",type="char",string="telephone"),
        "mobile":fields.related("store_id","mobile",type="char",string="mobile"),
        "address":fields.related("store_id","address",type="char",string="Address"),
        "contactperson":fields.related("store_id","contactperson",type="char",string="Contact Person"),
        "content":fields.text(string="Content",required=True),
        "applyinfoitem_ids":fields.one2many("tms.applyinfoitem","applyinfo_id",string="ApplyInfo Items"),
        "create_time":fields.date(string="Create Time"),
        "state":fields.selection([("draft","Draft"),("unreceived","UnReceived"),("hasreceived","HasReceived"),
                                  ("hasdone","HasDone"),("hasconfirm","HasConfirm")],string="State",required=True,readonly=True),
    }

    def applyinfo_unreceived(self,cr,uid,ids,args=None,context=None):
        self.write(cr,uid,ids,{'state':'unreceived'})
        return True

    def applyinfo_hasreceived(self,cr,uid,ids,args=None,context=None):
        self.write(cr,uid,ids,{'state':'hasreceived'})
        return True

    def applyinfo_hasdone(self,cr,uid,ids,args=None,context=None):
        self.write(cr,uid,ids,{'state':'hasdone'})
        return True

    def applyinfo_hasconfirm(self,cr,uid,ids,args=None,context=None):
        self.write(cr,uid,ids,{'state':'hasconfirm'})
        return True

    _order = "processid desc"

    _defaults={
        #"processid":_get_default_processid,
        "user_id":lambda self,cr,uid,context:uid,
        "create_time":lambda self,cr,uid,context:datetime.datetime.now().strftime("%Y-%m-%d"),
        "state":lambda self,cr,uid,context:"draft",
    }
ApplyInfo()

class ApplyInfoItem(osv.osv):
    _name="tms.applyinfoitem"
    _order="create_time asc"
    
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


class StopAndMoveApplyInfo(osv.osv):
    _name="tms.stopandmoveapplyinfo"
    _inherit="tms.applyinfo"

    _columns={
        "applyinfotype":fields.selection([("move","Move"),("offnet","Off Net"),("powercut","Power Cut"),
                                          ("govermentcheck","Goverment Check"),("duetoeletricity","Due to electricity"),
                                          ("duetonet","Due to net"),("duetohouse","Due to House"),("other","Other")
                                         ],string="ApplyInfo Type",required=True),
        "create_time":fields.datetime(string="Create Time"),
        "content":fields.text(string="Content",required=False),
    }
    _defaults={
        "user_id":lambda self,cr,uid,context:uid,
        "state":lambda self,cr,uid,context:"hasconfirm",
        "create_time":lambda self,cr,uid,context:time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
    }

StopAndMoveApplyInfo()    


class FeeType(osv.osv):
    """
    费用类别
    """
    _name = "tms.feetype"
        
    _columns={
        "name":fields.char(string="Name", size=100,required=True),
        "code":fields.char(string="Code",size=100,required=True),
        "remark":fields.char(string="Remark",size=300,required=False)
    }
    
    _sql_constraints = [('name_uniq', 'unique(name)', 'FeeType name must be unique!'),
                        ('code_uniq','unique(code)','FeeType code must be unique!')
                       ]
FeeType()

class SendCompany(osv.osv):
    """
    快递公司
    """
    _name="tms.sendcompany"
    
    _columns={
        "name":fields.char(string="Company Name",size=100,required=True),
        "remark":fields.char(string="Remark",size=300)
    }

    _sql_constraints = [('name_uniq', 'unique(name)', 'SendCompany name must be unique!')]
SendCompany()

class FeeBase(osv.osv):
    """
    费用基本类型,作为维护费用来使用
    """
    _name="tms.feebase"
    def get_province_name(self,cr,uid,ids,name,args,context=None):
        print "get_province_name ,ids is %s "% ids
        result=dict.fromkeys(ids,'None')
        print self.browse(cr,uid,ids,context= context )
        for item in self.browse(cr,uid,ids,context=context):
            result[item.id] = item.store_id.province_id.name
            #print item.productname
            #result[item.id] = ''
        return result 

    def  _get_default_processid(self,cr,uid,code,context):
        sequenceid=self.pool.get("ir.sequence").search(cr,uid,[('code','=',code)])
        sequence = self.pool.get("ir.sequence").browse(cr,uid,sequenceid,context=None)
        return sequence[0].get_id()
 
    def on_change_store(self,cr,uid,ids,model_id,context=None):        
        if not model_id:
            return False
        item = self.pool.get("tms.store").browse(cr,uid,model_id,context=context)
        if not item :
            return False
        return {
            "value":{
                "province":self.get_province_by_store_id(cr,uid,item.id),
                "storenum":item.storenum,
            }
        }
    
    def get_province_by_store_id(self,cr,uid,store_id,context=None):
        if not store_id:
            return False
        pitem = self.pool.get("tms.store").browse(cr,uid,store_id,context=context)
        if not pitem:
            return False
        return pitem.province_id.name
    
    def name_get(self,cr,uid,ids,context=None):
        res = []
        for item in self.browse(cr,uid,ids,context):
            res.append((item.id,item.processid))
        return res

    def _get_accountperiod_list(self,cr,uid,context=None):
        """
        暂时不使用，账期由入账时间直接生成
        """
        res=[]
        for index in range(-6,6):
            item = utildate.getyearandmonth(index)
            period = ("%s%s"%(item[0],item[1]))
            res.append((period,period))
        return res

    def name_get(self,cr,uid,ids,context=None):
        res = []
        for item in self.browse(cr,uid,ids,context):
            res.append((item.id,item.processid))
        return res

    def create(self,cr,uid,data,context=None):
        print "create productforit ,data is %s" % data
        if type(data['store_id']) is list:
            data["store_id"] = data["store_id"][0]
        feebase_id = super(FeeBase, self).create(cr, uid, data, context=context)
        childtypename = type(self).__name__
        processid = ""
        if childtypename=="FeeBase":
            processid = self._get_default_processid(cr,uid,'tms.feebase.processid',context)
        elif childtypename =="tms.feeforsend":
            processid = self._get_default_processid(cr,uid,'tms.feeforsend.processid',context)
        elif childtypename=="tms.feeforproduct":
            processid = self._get_default_processid(cr,uid,'tms.feeforproduct.processid',context)
        elif childtypename=="tms.feeforproductit":
            processid = self._get_default_processid(cr,uid,'tms.feeforproductit.processid',context)
        elif childtypename=="tms.feeforitservice":
            processid = self._get_default_processid(cr,uid,'tms.feeforitservice.processid',context)
        elif childtypename=="tms.feeforother":
            processid = self._get_default_processid(cr,uid,'tms.feeforother.processid',context)
        self.write(cr,uid,feebase_id,{"accountperiod":data['feedate'][0:7].replace('-',''),"processid":processid},context)
        return feebase_id

    def export_data(self,cr,uid,ids,fields_to_export,context=None):
        print fields_to_export
        print "User have tms.group_tms_fee_finance %s" % self.user_has_groups(cr,uid,"tms.group_tms_fee_finance",context)

        if not self.user_has_groups(cr,uid,"tms.group_tms_fee_finance",context):
            if "amount" in fields_to_export:
                fields_to_export.remove("amount")
            if "productprice" in fields_to_export:
                fields_to_export.remove("productprice")
            if "productcount" in fields_to_export:
                fields_to_export.remove("productcount")
        return super(FeeBase,self).export_data(cr,uid,ids,fields_to_export,context)
    
    def write(self,cr,uid,ids,values,context=None):
        print "call write method,parammeter value is %s" % values
        if not self.user_has_groups(cr,uid,"tms.group_tms_fee_finance",context):
            if len(values)!=2 and sorted(values.keys())!=sorted(['oanum','state']):
                raise osv.except_osv(_("Operation Canceld"),u"您没有修改的权限!")
        return super(FeeBase,self).write(cr,uid,ids,values,context) 

    def _check_fee_state(self,cr,uid,ids,oldstate,targetstate,context=None):
        model_id = context["active_model"]
        model=self.pool.get(model_id)
        items = model.browse(cr,uid,ids,context=context)
        if targetstate!='hasback' and any([item.state!=oldstate for item in items]):
            raise osv.except_osv(_('Operation Canceld'),_('Only '+oldstate+' fee can be exported!'))
        for item in items: 
            model.write(cr,uid,item.id,{"state":targetstate})
        return True
    
    def _check_is_finance(self,cr,uid):
        uitem=self.pool.get("res.users").browse(cr,uid,uid)
        groupnames = [item.name for item in uitem.groups_id]
        print groupnames
        if "Finance Fee Manager" not in groupnames:
            raise osv.except_osv(_('Operation Canceld'),_('You are not Finance Fee Manager!'))

    def export_to_account(self,cr,uid,ids,context=None):
        self._check_is_finance(cr,uid)
        return self._check_fee_state(cr,uid,ids,'draft','hasexported',context=context)

    def set_to_hasback(self,cr,uid,ids,context=None):
        self._check_is_finance(cr,uid)
        return self._check_fee_state(cr,uid,ids,'hasoa','hasback',context=context)

    _columns={
        "processid":fields.char(string="ProcessId",size=100,required=False),        
        "applyprocessid":fields.char(string="ApplyInfo Num",size=100,required=False),
        "feedate":fields.date(string="Fee Date"),
        "store_id":fields.many2one("tms.store",string="Store"),
        "storenum":fields.related("store_id","storenum",type="char",string="Store Num"),
        "province":fields.function(get_province_name,type="char",string="Province",store=True),
        "feetype_id":fields.many2one("tms.feetype","Fee Type"),
        "payman":fields.many2one("res.users","Pay Man"),
        "amount":fields.float(string="Amount"),
        "accountamount":fields.float(string="Account Amount"),
        "accountperiod":fields.char(string="Account Period", size=20,required=False),
        "oanum":fields.char(string="OA Num",size=100),
        "feecontent":fields.char(string="Fee Content",size=100),
        "remark":fields.text(string="Remark"),
        "state":fields.selection([("draft","Draft"),("hasexported","Has Exported"),("hasoa","Has Input OANum"),("hasback","Has Back")],
                                 string="States"),
    }

    _order = "processid desc"
    _defaults={
        "feedate":lambda self,cr,uid,context:datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payman":lambda self,cr,uid,context:uid,
        "state":lambda self,cr,uid,context:'draft',
        "feecontent":lambda self,cr,uid,context:'上门服务费',
    }
FeeBase()


class FeeForSend(osv.osv):
    _inherit="tms.feebase"
    _name = "tms.feeforsend"

    _columns={
        "sendcompany":fields.many2one("tms.sendcompany","Send Company"),
        "sendordernum":fields.char(string="Send Order num",size=100,required=True),
        "sendproduct":fields.char(string="Send Product", size=200,required=True),
    }
FeeForSend()


class FeeForProduct(osv.osv):
    _inherit="tms.feebase"
    _name = "tms.feeforproduct"

    def on_change_productaccount(self,cr,uid,ids,productcount,productprice,context=None):        
        return {
            "value":{
                "amount":productcount*productprice,
                "accountproductprice":productprice,
                "accountproductcount":productcount,
                "accountamount":productcount*productprice,
            }
        }

    def on_change_accountproductaccount(self,cr,uid,ids,accountproductcount,accountproductprice,context=None):        
        return {
            "value":{
                "accountamount":accountproductprice*accountproductcount,
            }
        }

    _columns={
        "productname":fields.char(string="Product Name",size=200),
        "producttype":fields.char(string="Product Type",size=100),
        "productprice":fields.float(string="Product Price"),
        "productcount":fields.integer(string="Product Count"),
        "accountproductprice":fields.integer(string="Account Product Price"),
        "accountproductcount":fields.integer(string="Account Product Count")
    }
FeeForProduct()

class FeeForProductIt(osv.osv):
    _inherit="tms.feebase"
    _name = "tms.feeforproductit"

    def on_change_productaccount(self,cr,uid,ids,productcount,productprice,context=None):        
        return {
            "value":{
                "amount":productcount*productprice,
                "accountproductprice":productprice,
                "accountproductcount":productcount,
                "accountamount":productcount*productprice,
            }
        }

    def on_change_accountproductaccount(self,cr,uid,ids,accountproductcount,accountproductprice,context=None):        
        return {
            "value":{
                "accountamount":accountproductprice*accountproductcount,
            }
        }
    _columns={
        "productname":fields.char(string="Product Name",size=200),
        "producttype":fields.char(string="Product Type",size=200),
        "productprice":fields.float(string="Product Price",groups="tms.group_tms_fee_finance"),
        "productcount":fields.integer(string="Product Count",groups="tms.group_tms_fee_finance"),
        "accountproductprice":fields.integer(string="Account Product Price",groups="tms.group_tms_fee_accout,tms.group_tms_fee_finance"),
        "accountproductcount":fields.integer(string="Account Product Count",groups="tms.group_tms_fee_accout,tms.group_tms_fee_finance")
    }

FeeForProductIt()


class FeeForItService(osv.osv):
    _inherit="tms.feebase"
    _name = "tms.feeforitservice"

FeeForItService()


class FeeForOther(osv.osv):
    _inherit="tms.feebase"
    _name = "tms.feeforother"

FeeForOther()
