define([
	'models/base'
	], function(BaseModel){

		var OsmModel = BaseModel.extend({
			url:'/api/osm',
			defaults:{
				name: 'monoprix',
				price: 0,
				active: true
			},
			initialize: function(attributes, options){
				this.vent.on('osm:current', function(osm){
					var active = (osm.name === this.get('name'));
					this.set('active', active);
				}, this);
				
			},
			save: function(attributes, options){
				attributes || (attributes = {});
				options || (options = {});
				var that = this;
				var vent = that.vent;
				options.emulateJSON = true;
				vent.trigger('osm:current', this.toJSON());

				options.data = {
					'new_name': this.get('name')
				}

				options.error = function(jqXHR, textStatus, errorThrown){
					console.log(jqXHR);
					console.log(textStatus);
					console.log(errorThrown);
				}

				return BaseModel.prototype.save.apply(this, [attributes, options]);
			}
		});

		return OsmModel;

})