def product_carbon_emission(product_weight, product_emission_factor, transport_factor, packaging_factor, refrigeration_factor):
    
    final_product_emission = product_weight * product_emission_factor * (1 + transport_factor + packaging_factor + refrigeration_factor)
    return final_product_emission