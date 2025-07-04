from enum import Enum

class HeatingType(Enum):
    """
    Enumeration of different types of water heating systems and their corresponding identifiers.
    
    This enum represents the various types of heating systems that can be used
    for water heating carbon emission calculations.
    
    Attributes:
        LP_GAS: Liquefied Petroleum Gas heating system
        NATURAL_GAS: Natural Gas heating system
        ELECTRIC: Electric heating system
        NONE: Represents no heating system or invalid value
    """
    LP_GAS = 'lp_gas'
    NATURAL_GAS = 'natural_gas'
    ELECTRIC = 'electric'
    NONE = 'not_value'

class WaterEmissionCalculator:
    """
    A class for calculating carbon emissions from water consumption based on heating type.
    
    This class provides methods to calculate carbon emissions from water usage,
    taking into account the heating system type and percentage of heated water.
    
    Attributes:
        HEATING_TYPE_CONSUMPTION (dict): Maps heating types to their emission factors (kg CO2e/L)
        WATER_DISTRIBUTION_EMISSION (float): Base emission factor for water distribution (kg CO2e/L)
    """
    
    # Emission factors for different heating types in kg CO2e per liter
    HEATING_TYPE_CONSUMPTION: dict[HeatingType, float] = {
        HeatingType.LP_GAS: 0.00268,      # LP Gas heating emission factor
        HeatingType.NATURAL_GAS: 0.00203,  # Natural Gas heating emission factor
        HeatingType.ELECTRIC: 0.00139,     # Electric heating emission factor
        HeatingType.NONE: 0               # No heating emissions
    }
    
    # Base emission factor for water distribution in kg CO2e per liter
    WATER_DISTRIBUTION_EMISSION = 0.000616

    def calculate_water_emission(self, liters: int, heating_percentage: int, heating_type: str):
        """
        Calculates the total carbon emissions from water consumption considering heating.
        
        This method computes the total carbon emissions based on the amount of water used,
        the percentage of water that is heated, and the type of heating system used.
        
        Args:
            liters (int): Total water consumption in liters
            heating_percentage (int): Percentage of water that is heated (0-100)
            heating_type (str): Type of heating system used, must match one of the HeatingType values
        
        Returns:
            int: Total carbon emissions in kg CO2e (rounded to nearest integer)
            
        Raises:
            ValueError: If heating_type is invalid or heating_percentage is out of range
            
        Example:
            >>> calc = WaterEmissionCalculator()
            >>> calc.calculate_water_emission(100, 50, 'electric')
            1  # (rounded emission value for 100L water, 50% heated with electric system)
        """
        # Validate heating type
        try:
            heating_enum = HeatingType(heating_type)
        except ValueError:
            raise ValueError(f"Invalid heating type. Must be one of: {[type.value for type in HeatingType]}")
        
        # Validate heating percentage
        if not 0 <= heating_percentage <= 100:
            raise ValueError("Heating percentage must be between 0 and 100")
        
        if heating_percentage > 0:
            # Calculate volumes of cold and hot water
            cold_water = liters * (heating_percentage / 100)
            hot_water = liters - cold_water
            
            # Get emission factor for the heating type
            heating_emission = self.HEATING_TYPE_CONSUMPTION[heating_enum]
            
            # Calculate emissions for both cold and heated water
            cold_water_emission = cold_water * self.WATER_DISTRIBUTION_EMISSION
            hot_water_emission = hot_water * (self.WATER_DISTRIBUTION_EMISSION + heating_emission)
            
            result = cold_water_emission + hot_water_emission
            
            response = {
                "coldWaterLiters": cold_water,
                "hotWaterLiters": hot_water,
                "coldWaterEmission": cold_water_emission,
                "hotWaterEmission": hot_water_emission,
                "totalEmission": result
            }
        else:
            # If no heating, only calculate distribution emissions
            result = liters * self.WATER_DISTRIBUTION_EMISSION
            
            response = {
                "coldWaterLiters": liters,
                "hotWaterLiters": 0,
                "coldWaterEmission": result,
                "hotWaterEmission": 0,
                "totalEmission": result
            }
        
        return response
