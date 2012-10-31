from django.db import connection

def dictfetchall(cursor):
		"Generator of all rows from a cursor"
		desc = cursor.description
		return [ dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall() ]

def get_product_from_short_url(short_url):
	sql_query = (" SELECT result.id, result.title, result.url, monoprix_brand.name, LEAST(result.price, telemarket_product.price) as price, LEAST(result.unit_price, telemarket_product.unit_price) as unit_price, result.unit_id, result.image_url, result.promotion, result.category_id, result.description, result.ingredients, result.valeur_nutritionnelle, result.conservation, result.conseil, result.composition FROM "
				"(SELECT monoprix_product.id, STRING_AGG(chunck.chuncks, '-') as short_url, title, url, brand_id, price, unit_price, unit_id, image_url, promotion, category_id, description, ingredients, valeur_nutritionnelle, conservation, conseil, composition "
				"FROM (SELECT regexp_split_to_table(unaccent(lower(title)), '(\W)+') as chuncks, id  FROM monoprix_product) as chunck "
				"JOIN monoprix_product ON chunck.id = monoprix_product.id "
				"GROUP BY monoprix_product.id) AS result "
				"JOIN monoprix_brand ON result.brand_id = monoprix_brand.id "
				"JOIN telemarket_product ON result.id = telemarket_product.monoprix_product_id "
				"WHERE short_url = '"+short_url+"' ")
	cursor = connection.cursor()
	cursor.execute(sql_query)
	result = dictfetchall(cursor)

	return result