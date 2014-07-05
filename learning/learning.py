#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
#
# Copyright 2013 SOABER, Inc.
#

from openerp.osv import osv,fields

class message_of_the_day(osv.osv):
    _name = "message_of_the_day"

    def my_method(self,cr,uid,context=None):
        return {"hello":"world"}

    def my_method2( self, cr,uid, name, age , context=None):
        print "name is %s , age is %d" %(name,age)
        print "context is %s " % context
        return {"name":name,"age":age}

    _columns = {
        "message":fields.char(string="Message",size=100),
        "color":fields.char(string="Color",size=100),
    }
message_of_the_day()

# vim: tabstop=4 shiftwidth=4 softtabstop=4

