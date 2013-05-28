define([
	'underscore',
	'collections/base',
	'models/osm'
	], function(_, BaseCollection, OsmModel){

		var OsmsCollections = BaseCollection.extend({
			url:'/api/osm',
			model: OsmModel,
			initialize: function(){
			},
			get_active_osm: function(){
				var active_osm = _.find(this.models, function(osm, i){
					return osm.get('active');
				}, this);
				return active_osm;
			},
			get_min_osm: function(){
				var min_osm = this.min(function(osm){
					return osm.get('price');
				}, this)
				return min_osm;

			},
			get_price_to_save: function(){
				var min_osm = this.get_min_osm();
				var active_osm = this.get_active_osm();
				return min_osm.get('price') - active_osm.get('price');
			}
		});

		return OsmsCollections;
})