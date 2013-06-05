define([
	'underscore',
	'modernizr',
	'collections/products',
	'views/base',
	'views/product',
	'text!../../templates/products.html',
	'text!../../templates/plus.html'
	],
	function(_, Modernizr, ProductsCollection, BaseView, ProductView, productsTemplate, plusTemplate){

		var ProductsView = BaseView.extend({
			// This variable controlls whether or not to fetch products from server when requested
			fetching: false, 

			// Products width
			PRODUCT_WIDTH: 175,
			PRODUCT_WIDTH_NO_TOUCH: null,
			rendered: false,

			tagName:'div',
			className: 'products',
			template: _.template(productsTemplate),

			initialize: function(options){
				options || (options = {});
				this.products = options.products || new ProductsCollection([], {'vent': this.vent});
				this.products_per_page = this.products.PRODUCTS_PER_PAGE;
				this.page = this.products.page;
				var that = this;
				this.bindTo(this.products, 'request', function(){
					that.fetching = true;
				});

				this.bindTo(this.products, 'sync', function(){
					this.fetching = false;
				});

				this.bindTo(this.products, 'add', this.render);
			},
			render: function(product){
				if(typeof product !== 'undefined'){
					var view = new ProductView({'product': product, 'vent': this.vent})
					this.addSubView(view);
					this.$el.append(view.render().el);
				}else{
					this.closeSubViews();
					this.$el.empty();
					var that = this;
					this.products.each(function(product){
						var view = new ProductView({'product': product, 'vent': this.vent})
						that.$el.append(view.render().el);
					});
				}

				// Adding plus button if more products are available to fetch
				if(!Modernizr.touch){

					var outerWidth = this.$el.find('.product').outerWidth();
					if(outerWidth){
						if (!this.PRODUCT_WIDTH_NO_TOUCH) this.PRODUCT_WIDTH_NO_TOUCH = outerWidth;
						outerWidth = this.PRODUCT_WIDTH_NO_TOUCH;
						// Setting width
						this.$el.find('.product').width(outerWidth+'px')
						var products_count = this.$el.find('.product').length;
						this.$el.width(outerWidth*products_count*1.1);
					}
				};

				if(Modernizr.touch){
					this.$el.parent().addClass('touch');
					if (this.products.length>5) this.$el.width(this.products.length*this.PRODUCT_WIDTH);
				}


				this.$el.parent().bind( 'scroll', {context: this}, this.touchSwipeListener);

				
				return this;
			},
			events: {
				'click div.add-box': 'getMoreProducts',
			},
			touchSwipeListener: function(e){
				e.preventDefault();
				
				try{
					var that = e.data.context;
					var $el = that.$el;
					var base_width = $el.parent().outerWidth();
					var width = $el.outerWidth();
					var left = $el.find('.product').offset().left;
					var calculus = (left+width-base_width)/base_width;
					if(calculus<.5){
						that.getMoreProducts();

					}
				}catch(err){
					console.log(err);
				}
			},
			getMoreProducts: function(callback){
				var vent = this.vent;
				if (!this.fetching){
					this.products.fetch({
						more: true,
						'vent': vent,
						'callback': callback
					});
				}
			},
			more: function(callback){
				var nb_products_max = this.products.count;
				var current_nb_products = this.products.length;
				var current_page = this.page;
				var products_per_page = this.products_per_page;
				var nb_max_pages = Math.ceil(nb_products_max/products_per_page);
				var max_current_page = Math.ceil(current_nb_products/products_per_page);

				if(max_current_page === current_page && current_page < nb_max_pages && current_nb_products<nb_products_max){
					// Fetch more product
					this.getMoreProducts();
					this.translation(1);
				}else if(current_page < nb_max_pages){
					this.translation(1);
					this.products.page = this.products.page +1;
					if (callback) callback();
				}
			},
			less: function(callback){
				var nb_products_max = this.products.count;
				var current_nb_products = this.products.length;
				var current_page = this.page;
				var products_per_page = this.products_per_page;
				var nb_max_pages = Math.ceil(nb_products_max/products_per_page);
				var max_current_page = Math.ceil(current_nb_products/products_per_page);

				if(current_page>1){
					// Fetch more product
					this.translation(-1);
				}

				this.products.page = (this.products.page > 1 ? this.products.page - 1: 1);

				if (callback) callback();
			},
			translation: function(direction){
				var width = this.PRODUCT_WIDTH_NO_TOUCH;
				this.$el.css('position', 'relative');
				var current_page = this.page;
				var products_per_page = this.products_per_page;
				if (direction === 1){
					var left_offset = -current_page*products_per_page*this.PRODUCT_WIDTH_NO_TOUCH;
					this.$el.css('left', left_offset+'px');
					this.page = current_page +1;
				}else{
					var left_offset = -(current_page-2)*products_per_page*this.PRODUCT_WIDTH_NO_TOUCH;
					if(left_offset<0) this.$el.css('left', left_offset+'px');
					this.page = current_page - 1;
					if (this.page<1) this.page = 1;
					if(left_offset>=0) this.$el.css('left', '0px');
					
				}
			}
		})

		return ProductsView;
})