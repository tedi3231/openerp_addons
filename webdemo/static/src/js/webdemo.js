//console.log("This is from webdemo js!");
openerp.webdemo = function(instance){
	//console.log("Module loaded!");
	instance.webdemo = {};

	//instance.web.client_actions.add("webdemo.action","instance.webdemo.action");
	//instance.webdemo.action = function(parent,action){
	//	console.log("Excuted the action",action);
	//};
	//instance.webdemo.action = instance.web.Widget.extend({
	//	className : "oe_web_demo",
	//	start : function() {
	//		this.$el.text("Hello ,world!");
	//		return this._super();
	//	}
	//});
	instance.webdemo.homepage = instance.web.Widget.extend({
		template : 'homepage',
	});
};
