import openerp.addons.web.http as http

class oe_controller(http.Controller):
    _cp_path = "/oe"

    @http.httprequest
    def say_hello(self,req,action=None,**kwargs):
        print 'req=%s,\nreq.context=%s,\naction=%s,\nkwargs=%s' %(req.params,req.context,action,kwargs)
        print 'session_id is %s' % req.session_id
        print 'session.context is %s, userid is %s' % (req.session.proxy,req.session._uid)
        return "<h1>Hello baby!</h1>"
