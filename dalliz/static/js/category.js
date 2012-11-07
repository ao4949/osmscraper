$(document).ready(function(){
	// Filter by brand
	$("input:checkbox[name=brands_options]").click(function() {
		var all_is_checked = $($("input:checkbox[name=brands_options][id='brand_0']")[0]).is(':checked');
		if (all_is_checked) {
			$('.product').show()
		}else{
			$('.product').hide();
			$("input:checkbox[name=brands_options]:not([id='brand_0'])").each(function(){
				var id_brand = $(this).val();
				if ($(this).is(':checked')) {
					$('.product[data-brand='+id_brand+']').show();
				}else{
					$('.product[data-brand='+id_brand+']').hide();
				}
			})
		}
	});

	// Filter by price
	function filter_by_price_low_to_high(products){
		// var products = $('.product');
		// $('.product').remove();
		var sorted_products = products;
		var sorted = false;
		while(!sorted){
			sorted = true;
			for (var i=0; i<products.length-1; i++){
				// console.log(($(products[i]).attr('data-price')));
				// console.log(($(products[i+1]).attr('data-price')));

				if( parseFloat( $(products[i]).attr('data-price') ) > parseFloat( $(products[i+1]).attr('data-price') ) ) {
					temp_i = products[i];
					temp_i1 = products[i+1];
					sorted_products[i] = temp_i1;
					sorted_products[i+1] = temp_i;
					sorted = false;
					break;
				}
			}
			products = sorted_products;
			// console.log(products);
			// console.log(sorted);
		}
		return products;

		// products.each(function(){$('.products').append($(this))})
	}

	// Filter by price
	function filter_by_price_high_to_low(products){
		$.fn.reverse = [].reverse;
		return filter_by_price_low_to_high(products).reverse();
	}

	// Events handlers:
	$('#prix_croissant').click(function(){
		$("#text_filter").html($(this).text()+'<b class="caret"></b>');
		var products = $('.product:visible');
		$('.product:visible').remove();
		products = filter_by_price_low_to_high(products);
		products.each(function(){$('.products').append($(this))})
	});

	$('#prix_decroissant').click(function(){
		$("#text_filter").html($(this).text()+'<b class="caret"></b>');
		var products = $('.product:visible');
		$('.product:visible').remove();
		products = filter_by_price_high_to_low(products);
		products.each(function(){$('.products').append($(this))})
	});

	// Number of products init
	$("input[id^='brand_']").each(function(){
		var id = $(this).data('id');
		if (id===0){
			var count = $('.product').length
			$(this).find("+label").html($(this).find("+label").text()+' <span>('+count+')</span>');			
		}else{
			var count = $('div[data-brand='+id+']').length
			$(this).find("+label").html($(this).find("+label").text()+' <span>('+count+')</span>');
		}
	})
});