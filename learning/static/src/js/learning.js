//console.log("Debug statement : file loaded ");
openerp.learning = function(instance){
	//console.log("learning module loading !");
	
	var _t = instance.web._t;
	var _lt = instance.web._lt;

	var Qweb = instance.web.qweb;

	instance.learning = {};

	instance.learning.MessageOfTheDay = instance.web.Widget.extend({
		template:"MessageOfTheDay",
		init:function(){
			this._super.apply(this,arguments);	
		},
		start : function(){
			var self = this;
			new instance.web.Model("message_of_the_day").query(["message"]).first().then(function(result){
				console.log(self.$el.find(".oe_learning_motd").length);
				self.$el.find(".oe_learning_motd").html(result.messag);
				self.$el.append(result.message);
				console.log(result.message);
			});
		}
	});

	instance.learning.Homepage = instance.web.Widget.extend({
		className : "oe_learning_homepage",
		template:"Homepage",
		init:function( ){
			this._super.apply(this,arguments);
		},
		start:function(){
			var self = this;
			var model = new instance.web.Model("message_of_the_day");
			model.call("my_method",[],{context:new instance.web.CompoundContext()})
			.then(function(result){
				console.log(result);
				self.$el.append(result['hello']);
			});

			model.call("my_method2",[],{name:"tedi",age:239,context:new instance.web.CompoundContext()})
			.then(function(result){
				console.log(result);
				self.$el.append(result["name"]);
			});
			
			var motd = new instance.learning.MessageOfTheDay(this);
			motd.appendTo(this.$el);
			/*//this.$el.append(Qweb.render("Homepage",{name:"tedi3231"}));
			var greeting = new instance.learning.GreetingWidget(this);
			greeting.appendTo(this.$el);
			//console.log(this.getChildren()[0].$el);
			//return this._super();
			var products = new instance.learning.ProductsWidget(this,["CPU","Mouse","Keyboard","Graphic card","Screen"],"#00FF00");
			products.appendTo(this.$el);
			*/
			/*this.colorInput = new instance.learning.ColorInputWidget(this);
			this.colorInput.on("change:color",this,this.color_changed);
			this.colorInput.appendTo(this.$el);
			*/
			/*
			var confirm = new instance.learning.ConfirmWidget(this);
			confirm.on("user_choose",this,this.user_choose);
			confirm.appendTo(this.$el);
			*/
		},
		color_changed:function(){
			this.$el.find(".oe_color_div").css("background-color",this.colorInput.get("color"));
		},
		user_choose:function(confirm){
			if( confirm ){
				console.log("The user agreed to continue!");
			}else{
				console.log("The user refused to continue!");
			}
		},
	});

	instance.learning.GreetingWidget = instance.web.Widget.extend({
		start : function(){
			//this.$el.addClass("oe_learning_greetings");
			//this.$el.append("<div>We are so happy can see you agin!</div>");
			this.$el.append( Qweb.render("Greeting",{model:{products:["Ipad","Leapad","Macbook"],color:"#00FFCC"}}));
		},
	});

	instance.learning.ProductsWidget = instance.web.Widget.extend({
		template : "ProductsWidget",
		init : function(parent,products,color){
			this._super(parent);
			this.products = products;
			this.color = color;
		},
		/*start : function() {
			var self = this;
			this.$el.find("span.oe_products_item").click(function(){
				console.log("abc");
				self.trigger("choose_product_item","abc");
			});
		},*/
	});

	instance.learning.ConfirmWidget = instance.web.Widget.extend({
		start : function() {
			var self = this;
			this.$el.append("<div>Are you sure you want to perform this action?</div><button class='ok_button'>OK</button><button class='cancel_button'>Cancel</button>");
			this.$el.find("button.ok_button").click(function(){
				self.trigger("user_choose",true);
			});
			
			this.$el.find("button.cancel_button").click(function(){
				self.trigger("user_choose",false);
			});
		},
	});

	instance.learning.ColorInputWidget = instance.web.Widget.extend({
		template : "ColorInputWidget",
		start : function( ) {
			var self = this;
			this.$el.find("input").change(function(){
				self.input_changed();
			});
			self.input_changed();
		},
		input_changed:function(){
			var color = "#";
			color += this.$el.find(".oe_color_red").val();
			color += this.$el.find(".oe_color_green").val();
			color += this.$el.find(".oe_color_blue").val();
			console.log(color);
			this.set("color",color);	
		},	
	});

	instance.web.client_actions.add("action.learning.homepage","instance.learning.Homepage");
}
