#In this file is going to be all the calculus of different products and variables to see what is their water footprint and carbon footprint
def showers(shower_minutes, shower_type, times_per_day):
    total = 0
    #The variables that will be used for calculating are going to be converted in an int variable, 'cause the server takes the variables as string variables
    shower_minutes = int(shower_minutes)
    times_per_day = int(times_per_day)
    
    #it depends of the shower if it spends more water or not
    match shower_type:
        case 'traditional_shower':
            #The liters per minute that are spent by a traditional shower are 15 liters
            total = shower_minutes * 15
            total = total * times_per_day * 7
        case 'water_saving_shower':
            #The liters per minute that are spent by a water-saving shower are 8 liters
            total = shower_minutes * 8
            total = total * times_per_day * 7
        case 'bathtub':
            #The liters that are spent in a bathtub are 150 liters 
            total = 150 * times_per_day * 7
        case 'not_value':
            total = 0
    
    return total

def toilet(times_per_day, toilet_type):
    total = 0
    #The variables that will be used for calculating are going to be converted in an int variable
    times_per_day = int(times_per_day)
    
    #there are two standard types of toilet, traditional and water_saving
    match toilet_type:
        case 'traditional_toilet':
            #Each use spends 16 liters
            total = times_per_day * 16 * 7
        case 'water_saving_toilet':
            #Each use spends 5 liters
            total = times_per_day * 5 * 7
        case 'not_value':
            total = 0
            
    return total

def dishes(wash_type, times_per_day, minutes, faucet_open, liters_used):
    total = 0
    #The variables that will be used for calculating are going to be converted in an int variable
    minutes = int(minutes)
    faucet_open = int(faucet_open)
    liters_used = int(liters_used)
    times_per_day = int(times_per_day)
    
    match wash_type:
        case 'dishwasher':
            #A dishwasher uses 10 liters by each wash
            total = times_per_day * 10 * 7
        case 'by_hand':
            if faucet_open == 0:
                #Washing by hand spends 8 liters per minute when the faucet is always open
                total = minutes * 8 * times_per_day * 7
            elif faucet_open == 1:
                #When the faucet is not open while you are soaping the dishes, it reduces 30 percent of the water
                total = minutes * 8 * times_per_day * 7
                total = float(total - (total * .30))
                
            elif faucet_open == 2:
                #This else means when the user use a exactly number of liters
                total = liters_used * times_per_day * 7
        case 'not_value':
            total = 0
    
    return total

def washing_clothest(cycles_per_week, washing_machine_type, user_knows):
    total = 0
    #The variables that will be used for calculating are going to be converted in an int variable
    cycles_per_week = int(cycles_per_week)
    user_knows = int(user_knows)
    
    if user_knows == 1:
        match washing_machine_type:
            case 'front_loading':
                #The average of a front loading is 50 liters per cycle
                total = cycles_per_week * 50
            case 'top_loading':
                #The average of a top loading is 80 liters per cycle
                total = cycles_per_week * 80
            case 'not_value':
                total = 0
                
    elif user_knows == 0:
        #If the user does not know, the application will use the average in general which is 65 liters
        total = cycles_per_week * 65
        
    return total

def garden_watering(minutes, watering_type, liters, times_per_week, area, number_of_drippers, dripper_flow_rate):
    total = 0.0
    #The variables that will be used for calculating are going to be converted in a float variable
    minutes = float(minutes)
    liters = float(liters)
    times_per_week = float(times_per_week)
    area = float(area)
    dripper_flow_rate = float(dripper_flow_rate)
    #This is in ca
    area = area * 10.764
    
    match watering_type:
        case 'hose':
            #The average in watering with a hose is 19 liters per minute
            total = minutes * times_per_week * 19
        case 'spraying':
            #I'm converting from meters to inches to use the formula
            area = area * 10.764
            #this is the formula, the 0.62337 is the water flow, and the 0.5 is the depth on the garden
            formula = 0.62337 * area * 0.5
            #This part is for converting to liters the galons
            total = formula * 3.785
            
            total = total * times_per_week * minutes
        case 'dripping':
            #The formula for the dripping system is the number of drippers times the flow rate times the minutes over 60
            total = number_of_drippers * dripper_flow_rate * (minutes/60)
            
            total = total * times_per_week
        case 'bottle':
            #The user will insert the liters he uses in case he waters the garden with a bottle
            total = liters * times_per_week
        case 'not_value':
            total = 0
            
    return total

def house_cleaning(liters_by_bucket, buckets, mopping_per_day):
    total = 0
    #The variables that will be used for calculating are going to be converted in a float variable
    liters_by_bucket = int(liters_by_bucket)
    mopping_per_day = int(mopping_per_day)
    buckets = int(buckets)
    
    total = liters_by_bucket * buckets * mopping_per_day  * 7 
    return total

def coffe(cups_per_week):
    water_total = 0.0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in a float variable
    cups_per_week = float(cups_per_week)

    #each cup of coffe uses 7 mg aprox of coffe, and to make 1 kg of coffe is necessary 21000 liters of water, it means that one cup needs 140 literls plus the water promedium in a cup (0.24)
    water_total = cups_per_week * (140 + 0.24)
    
    
    return water_total

def tea(cups_per_week):
    water_total = 0.0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in a float variable
    cups_per_week = float(cups_per_week)
    
    #Each cup of tea needs 30 liters (production) of water plus the water in the cup
    cups_per_week = cups_per_week * (30 + 0.24)
    return water_total

def cow_meat(kg):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    kg = int(kg)
    
    #To produce 200 kg of cow meat, it's necesary 3,100,000 of water, that means 1 kg needs 15,500 of water
    water_total = kg * 15500
    
    return water_total

def chicken_meat(kg):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    kg = int(kg)
    
    #To produce one kg of chicken meat, it's necessary 4300 liters of water
    water_total = kg * 4300
    
    return water_total

def pork_meat(kg):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    kg = int(kg)
    
    #To produce one kg of chicken meat, it's necessary 4300 liters of water
    water_total = kg * 6000
    return water_total

def rice(kg):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    kg = int(kg)
    
    #To produce one kg of rice, it's necessary 2500 liters of water
    water_total = kg * 3000
    
    return water_total

def sugar(kg):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    kg = int(kg)
    
    #To produce one kg of sugar, it's necessary 1500 liters of water
    water_total = kg * 1500
    
    return water_total

def cheese(kg):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    kg = float(kg)
    
    #To produce one kg of cheese, it's necessary 940 liters of water
    water_total = kg * 940
    return water_total

def eggs(pieces):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    pieces = float(pieces)
    
    #To produce one egg, it's necessary 135 liters of water
    water_total = pieces * 135
    return water_total

def milk(liters):
    water_total = 0.0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    liters = float(liters)
     #To produce one liter of milk, it's necessary 200 liters of water
    water_total = liters * 1000
    return water_total

def beer(liters):
    water_total = 0.0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    liters = float(liters)
     #To produce one liter of beer, it's necessary 200 liters of water
    water_total = liters * 300
    return water_total

def processed_juice(liters):
    water_total = 0.0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    liters = float(liters)
     #To produce one liter of processed juice, it's necessary 200 liters of water
    water_total = liters * 850
    return water_total

def soda(liters):
    water_total = 0.0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    liters = float(liters)
     #To produce one liter of soda, it's necessary 175 liters of water
    water_total = liters * 175
    return water_total

def bread_slices(pieces):
    water_total = 0
    carbon_total = 0.0
    
    #The variables that will be used for calculating are going to be converted in the respective variable
    pieces = float(pieces)

    #To produce one slide og bread, it's necessary 40 liters of water
    water_total = pieces * 40
    return water_total