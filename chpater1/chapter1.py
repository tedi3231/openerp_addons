# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp import tools

class Shop(osv.osv):
    _name = "chapter1.shop"

    _columns = {
        "name":fields.char(string="Name", size=200, required=True),
        "address":fields.char(string="Address", size=500, required=True),
        "description":fields.char(string="Description",size=500,required=False),
        "state":fields.selection([("running","Running"),("building","Building")],string="State"),
    }

    _defaults = {
        "state":"running",
    }
Shop()
