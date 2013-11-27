# -*- coding: utf-8 -*-
import time
from openerp.report import report_sxw

class employee(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        print "employee __init__ called ,name is %s" % name
        super(employee,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw("report.laborprotection.employee",'laborprotection.employee','laborprotection/report/laborprotection_employee.rml',parser=employee,header="external")
