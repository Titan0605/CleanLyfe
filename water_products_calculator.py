def water_prod_calculus(water_consumed, water_heated ):    
    
    cold_water = 0
    hot_water = 0
    #--------------------------#
    water_consumed = water_consumed
    water_heated = water_heated    
    
    if water_heated != 0:        
        hot_water = water_heated / 100 * water_consumed
    else:
        cold_water = water_consumed
    
    print('Agua fria: ', cold_water)
    print('Agua caliente', hot_water)
        
water_prod_calculus(700, 30)