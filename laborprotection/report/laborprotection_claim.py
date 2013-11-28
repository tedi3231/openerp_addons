# -*- coding: utf-8 -*-
import time
from openerp.report import report_sxw

class claim(report_sxw.rml_parse):
    def __init__(self,cr,uid,name,context=None):
        print "claim __init__ called ,name is %s" % name
        super(employee,self).__init__(cr,uid,name,context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw("report.laborprotection.claim",'laborprotection.claim','laborprotection/report/laborprotection_claim.rml',parser=claim,header="external")
