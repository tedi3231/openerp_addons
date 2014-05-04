
openerp.oepetstore = function(instance) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    instance.oepetstore = {};

    /*
    instance.oepetstore.HomePage = instance.web.Widget.extend({
        init: function (parent) {
            // body...
            this._super(parent);
            this.name = "tedi3231";
        },
        start: function() {
            //this.$el.addClass("oe_petstore_homepage");
            //console.log("pet store home page loaded");
            //this.$el.append("<div>HEllo dear Openerp user!</div>");
            //var greeting = new instance.oepetstore.GreetingsWidget(this);
            //greeting.appendTo(this.$el);
            //console.log(this.getChildren()[0].$el);        
            this.$el.append(QWeb.render("HomePageTemplate",{"name":"tedi"}));
        },
    });
    */

    instance.oepetstore.HomePage = instance.web.Widget.extend({
        template: "HomePageTemplate",
        init: function(parent) {
            this._super(parent);
            this.name = "Nicolas";
        },
        start: function() {
            var products = new instance.oepetstore.ProductWidget(this,["CPU","MOUSE","KEYBORD","SCREEN"],"#00FF00");
            products.appendTo(this.$el);
            var widget = new instance.oepetstore.ConfirmWidget(this);
            widget.on("user_choose",this,this.user_choose);
            widget.appendTo(this.$el);
        },
        user_choose : function(confirm){
            if( confirm )
                console.log("the User agreed to continue");
            else
                console.log("The user don't agree to continue");
        }
    });

    instance.oepetstore.GreetingsWidget = instance.web.Widget.extend({
        start:function () {
            // body...
            this.$el.addClass("oe_petsotre_greetings");
            this.$el.append("<div>We are so happy to see you again in this menu!</div>");
        }
    });

    instance.oepetstore.ProductWidget = instance.web.Widget.extend({
        template : "ProductsWidget",
        init : function(parent,products,color){
            this._super(parent);
            this.products = products;
            this.color = color;
        }
    });

    instance.oepetstore.ConfirmWidget = instance.web.Widget.extend({
        start : function(){
            var self = this;
            this.$el.append("<div>Are you sure you want to perform this action?</div>");
            this.$el.append("<button class='ok_button'>OK</button>");
            this.$el.append("<button class='cancel_button'>Cancel</button>");
            this.$el.find("button.ok_button").click(function(){
                self.trigger("user_choose",true);
            });
            this.$el.find("button.cancel_button").click(function(){
                self.trigger("user_choose",false);
            });
        }
    });























    
    instance.web.client_actions.add('petstore.homepage', 'instance.oepetstore.HomePage');
}