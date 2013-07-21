# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class Store(osv.osv):
    _name = "tms.store"
    _columns = {
        "name":fields.char(string="Store Name", required=True, size=200),
        "storenum":fields.char(string="Store num", required=True, size=100),
        "province_id":fields.many2one("res.country.state", domain=[('country_id', '=', '49')], string="Province"),
        "address":fields.char(string="Address", size=200, required=True),
        "contactperson":fields.char(string="Contact Person", size=100, required=True),
        "telephone":fields.char(string="Telephone", size=50, required=True),
        "mobile":fields.char(string="Mobile", size=50),
        "netusername":fields.char(string="Net User Name", size=60),
        "netuserpass":fields.char(string="Net User pwd", size=60),
        "dynamicdomain":fields.char(string="Dynamic Domain", size=200),
        "dynamicdomainpass":fields.char(string="Dynamic Domain pass", size=100),
        "dynamicdomainaddress":fields.char(string="Dynamic Domain Address", size=100),
        "dynamicdomainotheraddress":fields.char(string="Domain Other Address", size=100),
        "peanutuserpass":fields.char(string="Peanut User pass", size=100),
        "peanutvalidemail":fields.char(string="Peanut valid email", size=100),
        "peanutemailpass":fields.char(string="Peanut email pass", size=100),
        "poscdk":fields.char(string="POSCDK", size=200),
        "remark":fields.text(string="Remark")
    }
    _sql_constraints = [('storenum_uniq', 'unique(storenum)', 'Storenum must be unique!')]
Store()