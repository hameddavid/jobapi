def retrieve_products_that_meet_filtering_criteria(productsToFilter,request):
	if "category" in request:
				if isinstance(request["category"], int):
					iCat = request["category"]
					if iCat > 0:
						from marketplace.domain.models.ProductCategories import ProductCategories
						rs = ProductCategories.objects.filter(id = iCat)
						productsToFilter = \
							 productsToFilter.filter(
								  productSubCategory__productCategory__in = rs ) 
	elif  "subCategory" in request:
		if isinstance(request["subCategory"], int):
			iSubCat = request["subCategory"]					
			if iSubCat > 0:
				from marketplace.domain.models.ProductSubCategories import ProductSubCategories
				rs = ProductSubCategories.objects.filter(id = iSubCat)
				productsToFilter = \
					 productsToFilter.filter(
						  productSubCategory__in = rs )
	return productsToFilter