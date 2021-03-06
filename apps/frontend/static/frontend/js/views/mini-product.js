define([
	'underscore',
	'models/product',
	'views/base',
	'text!../../templates/mini-product.html'
	], function(_, ProductModel, BaseView, miniProductTemplate){

		var MiniProductView = BaseView.extend({
			template: _.template(miniProductTemplate),
			className: 'product-recap',
			initialize: function(options){
				options || (options = {});
				this.suggested = options.suggested;
				this.product = options.product || new ProductModel({}, {'vent': this.vent});

				this.bindTo(this.product, 'change', this.render);
			},
			render: function(){
				this.$el.empty();
				var data = this.product.toJSON();
				data['suggested'] = this.suggested;
				this.$el.append(this.template(data));
				return this;
			},
			events: {
				'click .minus': 'lessQte',
				'click .plus': 'moreQte',
				'click .replacement': 'showSubstitution',
			},
			moreQte: function(e){
				var quantity = this.product.get('quantity');
				this.product.set('quantity', quantity + 1);
				var content_id = this.product.toJSON().id;
				this.product.save(null, {'cart': true, 'quantity': 1, 'vent': this.vent, 'content_id': content_id});
			},
			lessQte: function(e){
				var quantity = this.product.get('quantity');
				if (quantity-1>=0){
					this.product.set('quantity', quantity - 1);
					var content_id = this.product.toJSON().id;
					this.product.save(null, {'cart': true, 'remove': true, 'quantity': 1, 'vent': this.vent, 'content_id': content_id});
				}

			},
			showSubstitution: function(e){
				this.vent.trigger('product:recomandation', this.product);
			}
		});

		return MiniProductView;

})