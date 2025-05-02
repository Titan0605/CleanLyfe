from enum import Enum

class ShowerType(Enum):
    """
    Enumeration of different types of shower installations and their corresponding identifiers.
    
    This enum represents the various types of shower installations that can be used
    for water consumption calculations.
    
    Attributes:
        TRADITIONAL: Standard shower head with typical water flow
        WATER_SAVING: Eco-friendly shower head with reduced water flow
        BATHTUB: Standard bathtub installation
        NONE: Represents no shower installation or invalid value
    """
    TRADITIONAL = 'traditional_shower'
    WATER_SAVING = 'water_saving_shower'
    BATHTUB = 'bathtub'
    NONE = 'not_value'

class DishWashingType(Enum):
    """
    Enumeration of different methods for washing dishes and their corresponding identifiers.
    
    This enum represents the various ways dishes can be washed, each with different
    water consumption patterns.
    
    Attributes:
        HAND_WASHING: Traditional hand washing with running water
        FILLED_SINK: Washing dishes in a filled sink
        DISHWASHER: Using a dishwashing machine
        NONE: Represents no dish washing or invalid value
    """
    HAND_WASHING = 'hand_washing'
    FILLED_SINK = 'filled_sink'
    DISHWASHER = 'dishwasher'
    NONE = 'not_value'
    
class ClothesWashingType(Enum):
    """
    Enumeration of different types of clothes washing methods and machines.
    
    This enum represents the various types of washing machines and their
    water consumption patterns based on their loading type.
    
    Attributes:
        FRONT_LOADING: Front-loading washing machine (more water efficient)
        TOP_LOADING: Top-loading washing machine (traditional type)
        AVERAGE: Average consumption when type is unknown
        NONE: Represents no clothes washing or invalid value
    """
    FRONT_LOADING = 'front_loading'
    TOP_LOADING = 'top_loading'
    AVERAGE = 'average'
    NONE = 'not_value'
    
class GardenWateringType(Enum):
    """
    Enumeration of different methods for watering gardens and their corresponding identifiers.
    
    This enum represents the various ways gardens can be watered, each with different
    water consumption patterns and efficiency levels.
    
    Attributes:
        HOSE: Traditional garden hose watering method
        SPRAYING: Sprinkler system watering method
        DRIPPING: Drip irrigation system method
        BOTTLE: Manual watering using bottles or containers
        NONE: Represents no garden watering or invalid value
    """
    HOSE = 'hose'
    SPRAYING = 'spraying'
    DRIPPING = 'dripping'
    BOTTLE = 'bottle'
    NONE = 'not_value'

class FoodProductType(Enum):
    """
    Enumeration of different food and beverage products with their water footprint values.
    
    This enum represents various food and beverage products and their corresponding
    water consumption in liters per unit (kg, L, or piece).
    
    Attributes:
        COFFEE: Coffee consumption (140.24 L/cup)
        TEA: Tea consumption (30.24 L/cup)
        COW_MEAT: Beef consumption (15500 L/kg)
        CHICKEN_MEAT: Chicken consumption (4300 L/kg)
        PORK_MEAT: Pork consumption (6000 L/kg)
        RICE: Rice consumption (3000 L/kg)
        SUGAR: Sugar consumption (1500 L/kg)
        CHEESE: Cheese consumption (940 L/kg)
        EGGS: Eggs consumption (135 L/piece)
        MILK: Milk consumption (1000 L/L)
        BEER: Beer consumption (300 L/L)
        PROCESSED_JUICE: Juice consumption (850 L/L)
        SODA: Soda consumption (175 L/L)
        BREAD: Bread consumption (40 L/slice)
    """
    COFFEE = ('coffee', 140.24)  # L/cup
    TEA = ('tea', 30.24)  # L/cup
    COW_MEAT = ('cow_meat', 15500)  # L/kg
    CHICKEN_MEAT = ('chicken_meat', 4300)  # L/kg
    PORK_MEAT = ('pork_meat', 6000)  # L/kg
    RICE = ('rice', 3000)  # L/kg
    SUGAR = ('sugar', 1500)  # L/kg
    CHEESE = ('cheese', 940)  # L/kg
    EGGS = ('eggs', 135)  # L/piece
    MILK = ('milk', 1000)  # L/L
    BEER = ('beer', 300)  # L/L
    PROCESSED_JUICE = ('processed_juice', 850)  # L/L
    SODA = ('soda', 175)  # L/L
    BREAD = ('bread', 40)  # L/slice

    def __init__(self, id: str, water_footprint: float):
        self.id = id
        self.water_footprint = water_footprint

class HidricCalculator:
    """
    A class for calculating water consumption based on different water usage activities.
    
    This class provides methods to calculate water usage for different household activities,
    taking into account factors like duration, frequency, and method of use.
    
    Attributes:
        TRADITIONAL_SHOWER_LITERS_PER_MIN (int): Water consumption rate for traditional showers in L/min
        WATER_SAVING_SHOWER_LITERS_PER_MIN (int): Water consumption rate for eco-friendly showers in L/min
        BATHTUB_LITERS (int): Standard water capacity of a bathtub in liters
        HAND_WASHING_DISHES_LITERS_PER_MIN (int): Water consumption rate for hand washing dishes with running water
        FILLED_SINK_DISHES_LITERS (int): Water consumption for washing dishes in a filled sink
        DISHWASHER_LITERS (int): Water consumption per dishwasher cycle
    """

    # Constantes para el consumo de agua en duchas
    TRADITIONAL_SHOWER_LITERS_PER_MIN = 15
    WATER_SAVING_SHOWER_LITERS_PER_MIN = 8
    BATHTUB_LITERS = 150

    # Constantes para el consumo de agua en lavado de platos
    HAND_WASHING_DISHES_LITERS_PER_MIN = 12
    FILLED_SINK_DISHES_LITERS = 20
    DISHWASHER_LITERS = 15
    
    # Constantes para el consumo de agua en el lavado de ropa
    FRONT_LOADING_WASHING_CLOTHES_LITERS_PER_MIN = 50
    TOP_LOADING_WASHING_CLOTHES_LITERS_PER_MIN = 80
    AVERAGE_WASHING_CLOTHES_LITERS_PER_MIN = 65
    
    #constantes para el consumo de agua en el riego de jardines
    HOSE_LITERS_PER_MIN = 19

    # Mapeo de tipos de riego a su consumo
    HOSE_CONSUMPTION: dict[GardenWateringType, int] = {
        GardenWateringType.HOSE: HOSE_LITERS_PER_MIN,
        GardenWateringType.NONE: 0
    }
    
    # Mapeo de tipos de ducha a su consumo
    SHOWER_CONSUMPTION: dict[ShowerType, int] = {
        ShowerType.TRADITIONAL: TRADITIONAL_SHOWER_LITERS_PER_MIN,
        ShowerType.WATER_SAVING: WATER_SAVING_SHOWER_LITERS_PER_MIN,
        ShowerType.BATHTUB: BATHTUB_LITERS,
        ShowerType.NONE: 0
    }

    # Mapeo de tipos de lavado de platos a su consumo
    DISHES_CONSUMPTION: dict[DishWashingType, int] = {
        DishWashingType.HAND_WASHING: HAND_WASHING_DISHES_LITERS_PER_MIN,
        DishWashingType.FILLED_SINK: FILLED_SINK_DISHES_LITERS,
        DishWashingType.DISHWASHER: DISHWASHER_LITERS,
        DishWashingType.NONE: 0
    }
    
    # Mapeo de tipos de lavado de ropa a su consumo
    CLOTHES_CONSUMPTION: dict[ClothesWashingType, int] = {
        ClothesWashingType.FRONT_LOADING: FRONT_LOADING_WASHING_CLOTHES_LITERS_PER_MIN,
        ClothesWashingType.TOP_LOADING: TOP_LOADING_WASHING_CLOTHES_LITERS_PER_MIN,
        ClothesWashingType.AVERAGE: AVERAGE_WASHING_CLOTHES_LITERS_PER_MIN,
        ClothesWashingType.NONE: 0
    }

    def calculate_liters_per_week(self, liters: int, multiplier: int, minutes: int = 1, days: int = 7) -> int:
        """
        Calculates the total amount of water used (in liters) over a specified number of days.

        This method computes total water consumption based on usage frequency and duration.
        It includes validation to ensure all input parameters are non-negative.

        Args:
            liters (int): Water consumption rate in liters
            multiplier (int): Number of times the activity is performed each day
            minutes (int, optional): Duration of water usage in minutes per activity. Defaults to 1.
            days (int, optional): Number of days to calculate for. Defaults to 7.

        Returns:
            int: Total water usage in liters over the specified time period

        Raises:
            ValueError: If any of the input parameters are negative
        """
        if any(x < 0 for x in [liters, multiplier, minutes, days]):
            raise ValueError("All input values must be non-negative")
            
        return ((minutes * liters) * multiplier) * days
        
    def showers(self, shower_minutes: int, times_per_day: int, shower_type: str) -> int: 
        """
        Calculates the total weekly water usage (in liters) based on the type of shower used.

        This method handles different types of shower installations and calculates their
        water consumption based on usage patterns. It includes special handling for
        bathtubs and cases where no shower is installed.

        Args:
            shower_minutes (int): Duration of each shower in minutes
            times_per_day (int): Number of showers taken per day
            shower_type (str): Type of shower used, must match one of the ShowerType values

        Returns:
            int: Estimated total water usage in liters for the week
            
        Raises:
            ValueError: If inputs are negative or shower_type is invalid

        Example:
            >>> calc = HidricCalc()
            >>> calc.showers(10, 1, 'traditional_shower')
            1050  # (15L/min * 10min * 1time * 7days)
        """
        try:
            shower_enum = ShowerType(shower_type)
        except ValueError:
            raise ValueError(f"Invalid shower type. Must be one of: {[type.value for type in ShowerType]}")

        if shower_minutes < 0 or times_per_day < 0:
            raise ValueError("Shower minutes and times per day must be non-negative")

        consumption: int = self.SHOWER_CONSUMPTION[shower_enum]
        
        if shower_enum == ShowerType.BATHTUB:
            return self.calculate_liters_per_week(consumption, times_per_day)
        elif shower_enum == ShowerType.NONE:
            return 0
        else:
            return self.calculate_liters_per_week(consumption, times_per_day, shower_minutes)

    def dishes(self, washing_minutes: int, times_per_day: int, washing_type: str) -> int:
        """
        Calculates the total weekly water usage (in liters) for washing dishes.

        This method handles different dish washing methods and calculates their
        water consumption based on usage patterns. It includes special handling for
        different washing methods like hand washing, filled sink, and dishwasher.

        Args:
            washing_minutes (int): Duration of each dish washing session in minutes
                                (ignored for filled_sink and dishwasher methods)
            times_per_day (int): Number of dish washing sessions per day
            washing_type (str): Type of dish washing method, must match one of the DishWashingType values

        Returns:
            int: Estimated total water usage in liters for the week
            
        Raises:
            ValueError: If inputs are negative or washing_type is invalid

        Example:
            >>> calc = HidricCalc()
            >>> calc.dishes(15, 1, 'hand_washing')
            1260  # (12L/min * 15min * 1time * 7days)
            >>> calc.dishes(0, 2, 'dishwasher')
            210   # (15L * 2times * 7days)
        """
        try:
            washing_enum = DishWashingType(washing_type)
        except ValueError:
            raise ValueError(f"Invalid washing type. Must be one of: {[type.value for type in DishWashingType]}")

        if washing_minutes < 0 or times_per_day < 0:
            raise ValueError("Washing minutes and times per day must be non-negative")

        consumption: int = self.DISHES_CONSUMPTION[washing_enum]

        if washing_enum == DishWashingType.HAND_WASHING:
            return self.calculate_liters_per_week(consumption, times_per_day, washing_minutes)
        elif washing_enum == DishWashingType.NONE:
            return 0
        else:
            return self.calculate_liters_per_week(consumption, times_per_day)
        
    def washing_clothest(self, cycles_per_week: int, washing_machine_type: str) -> int:
        """
        Calculates the total weekly water usage (in liters) for washing clothes.

        This method handles different types of washing machines and calculates their
        water consumption based on the machine type and number of cycles. It includes
        special handling for different machine types and unknown machine types.

        Args:
            cycles_per_week (int): Number of washing cycles per week
            washing_machine_type (str): Type of washing machine, must match one of the ClothesWashingType values

        Returns:
            int: Estimated total water usage in liters for the week
            
        Raises:
            ValueError: If inputs are negative or washing_machine_type is invalid

        Example:
            >>> calc = HidricCalculator()
            >>> calc.washing_clothest(3, 'front_loading')
            150  # (50L * 3cycles)
            >>> calc.washing_clothest(2, 'top_loading')
            160  # (80L * 2cycles)
        """
        try:
            washing_machine_enum = ClothesWashingType(washing_machine_type)
        except ValueError:
            raise ValueError(f"Invalid washing type. Must be one of: {[type.value for type in ClothesWashingType]}")
        
        if cycles_per_week < 0:
            raise ValueError("Washing cycles per week must be non-negative")
        
        consumption: int = self.CLOTHES_CONSUMPTION[washing_machine_enum]
        
        if washing_machine_enum == ClothesWashingType.NONE:
            return 0
        else:
            return self.calculate_liters_per_week(consumption, cycles_per_week, days=1)
        
    def garden_watering(self, minutes: int, times_per_week: int, watering_type: str, 
                       area: float = 0, liters: int = 0, 
                       number_of_drippers: int = 0, dripper_flow_rate: float = 0) -> int:
        """
        Calculates the total weekly water usage (in liters) for garden watering.

        This method handles different garden watering methods and calculates their
        water consumption based on the method used and various parameters like area,
        time, and frequency. Each method has its own calculation formula.

        Args:
            minutes (float): Duration of each watering session in minutes
            times_per_week (float): Number of watering sessions per week
            watering_type (str): Type of watering method, must match one of the GardenWateringType values
            area (float, optional): Garden area in square meters (needed for spraying method). Defaults to 0.
            liters (float, optional): Liters used per session (for bottle method). Defaults to 0.
            number_of_drippers (float, optional): Number of drippers in the system (for dripping method). Defaults to 0.
            dripper_flow_rate (float, optional): Flow rate per dripper in L/hour (for dripping method). Defaults to 0.

        Returns:
            float: Estimated total water usage in liters for the week
            
        Raises:
            ValueError: If inputs are negative or watering_type is invalid

        Example:
            >>> calc = HidricCalculator()
            >>> # Calculate water usage for hose watering
            >>> calc.garden_watering(30, 3, 'hose')
            1710.0  # (19L/min * 30min * 3times)
            >>> # Calculate water usage for drip system
            >>> calc.garden_watering(60, 2, 'dripping', number_of_drippers=10, dripper_flow_rate=2)
            20.0  # (10drippers * 2L/hour * 1hour * 2times)
        """
        try:
            watering_enum = GardenWateringType(watering_type)
        except ValueError:
            raise ValueError(f"Invalid watering type. Must be one of: {[type.value for type in GardenWateringType]}")

        if any(x < 0 for x in [minutes, times_per_week, area, liters, number_of_drippers, dripper_flow_rate]):
            raise ValueError("All input values must be non-negative")

        match watering_enum:
            case GardenWateringType.HOSE:
                return self.calculate_liters_per_week(self.HOSE_LITERS_PER_MIN, times_per_week, minutes)
                
            case GardenWateringType.SPRAYING:
                # Convert area from square meters to square feet
                area_foots: float = area * 10.764
                # Formula: water flow * area * depth of irrigation
                gallons: float = 0.62337 * area_foots * 0.5
                # Convert gallons to liters
                liters_per_session: float = gallons * 3.785
                return self.calculate_liters_per_week(int(liters_per_session), times_per_week, minutes)
                
            case GardenWateringType.DRIPPING:
                # Formula: number of drippers * flow rate * time in hours
                liters_per_hour: float = float(number_of_drippers) * dripper_flow_rate
                return self.calculate_liters_per_week(int(liters_per_hour / 60), times_per_week, minutes, 1)
                
            case GardenWateringType.BOTTLE:
                return liters * times_per_week
                
            case GardenWateringType.NONE:
                return 0
    
    def house_cleaning(self, liters_by_bucket: int, buckets: int, mopping_per_day: int) -> int:
        return self.calculate_liters_per_week((liters_by_bucket * buckets), mopping_per_day)
    
    def calculate_food_product_water(self, quantity: int, product_type: str) -> int:
        """
        Calculates the water footprint for food and beverage products.

        This method calculates the total water consumption for various food and beverage
        products based on their quantity and type. Each product has a specific water
        footprint per unit.

        Args:
            quantity (float): Amount of product (in appropriate unit - kg, L, pieces, or cups)
            product_type (str): Type of product, must match one of the FoodProductType values

        Returns:
            float: Total water footprint in liters

        Raises:
            ValueError: If quantity is negative or product_type is invalid

        Example:
            >>> calc = HidricCalculator()
            >>> # Calculate water footprint for 1kg of beef
            >>> calc.calculate_food_product_water(1, 'cow_meat')
            15500.0
            >>> # Calculate water footprint for 2 cups of coffee
            >>> calc.calculate_food_product_water(2, 'coffee')
            280.48
        """
        try:
            # Find the enum member where id matches product_type
            product_enum: FoodProductType = next(member for member in FoodProductType if member.id == product_type)
        except StopIteration:
            raise ValueError(f"Invalid product type. Must be one of: {[type.id for type in FoodProductType]}")

        if quantity < 0:
            raise ValueError("Quantity must be non-negative")
        
        return self.calculate_liters_per_week(int(product_enum.water_footprint), quantity)

if __name__ == '__main__':
    hidric_calc = HidricCalculator()
    print(hidric_calc.showers(10, 10, 'traditional_shower'))
    print(hidric_calc.dishes(15, 2, 'hand_washing'))
    print(hidric_calc. washing_clothest(2,'top_loading'))
    print(hidric_calc.calculate_food_product_water(1, 'cow_meat'))  # 15500L for 1kg of beef
    print(hidric_calc.calculate_food_product_water(2, 'coffee'))    # 280.48L for 2 cups of coffee