define([
	'underscore',
	'views/base',
	'models/category',
	'collections/category',
	'views/categoryCollection',
	'views/product'
], function(_, BaseView, CategoryModel, CategoryCollection, CategoryCollectionView, ProductView){

	var MainView = BaseView.extend({
		el: 'section#main div.block-left',
		SCROLL_TRIGGER: 90,
		initialize: function(options){
			this.osms = options.osms;
			this.categories = {};

			// Global event listening
			this.vent.on('window:scroll', this.scrollController, this);
			this.vent.on('search:results:display', this.renderSearch, this);

			var that = this;

			// Updating current osm
			this.bindTo(this.osms, 'change', function(osm, options){
				that.vent.trigger('route:category:force');
			});
		},
		addCategory: function(category_id){
			// First we have to determine if the category was already fetched from server or not.
			var category_already_fetched = false;
			var index = null

			var current_osm = this.osms.get_active_osm();
			this.categories = {};
			if (current_osm){
				if (!this.categories[current_osm.get('name')]) this.categories[current_osm.get('name')] = [];
				var categories = this.categories[current_osm.get('name')];

				_.each(categories, function(category, i){
					if(category.id == category_id){
						category_already_fetched = true;
						category.current = true;
					}else if(category.id < category_id){
						category.current = false;
					}
				}, this);

				if (!category_already_fetched){
					// If the category was not fetched, proceed
					var categoryCollection = new CategoryCollection([], {'id': category_id,'osm': current_osm.get('name'), 'vent': this.vent});
					categoryCollection.current = true;
					categories.push(categoryCollection);

					var that = this;
					categoryCollection.fetch({
						'vent': this.vent,
						success:function(collection, response, options){
							collection.each(function(model){
								model.fetch_products({'vent': that.vent});
							});
							that.render(categoryCollection)
						}
					});
				}
			}

		},
		render: function(categoryCollection){
			this.closeSubViews();
			this.$el.empty();
			var view = new CategoryCollectionView({'collection': categoryCollection, 'osms': this.osms,'vent': this.vent});
			this.addSubView(view);
			this.$el.append(view.render().el);
			categoryCollection.current ? view.$el.show() : view.$el.hide();
			return this;

		},
		renderSearch: function(options){
			this.closeSubViews();
			this.$el.empty();
			var results = options.results;

			var that = this;

			results.each(function(product, i){
				var view = new ProductView({'product': product, 'vent': that.vent});
				that.$el.append(view.render().el);
			});
			return this;
		}
	});


	return MainView;
})