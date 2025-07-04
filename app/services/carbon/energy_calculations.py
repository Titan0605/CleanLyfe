from flask import jsonify
from typing import Dict, List, Union, Optional

class Electric_devices_calculator:
    def __init__(self):
        self.emission_factor = 0.438  # kgCO2e/kWh
    
    def calculation_type(self, type_calculation: str, electricity_consumption: float, devices: Dict) -> str:
        try:
            match type_calculation:
                case 'basic_calculation':
                    result = self.basic_calculation(electricity_consumption, self.emission_factor)
                    return 'Electric calculation successfully.' if result > 0 else 'Failed electrical calculation.'
                case 'accurate_calculation':
                    result = self.accurate_calculation(devices)
                    return 'Electric calculation successfully.' if result else 'Failed electrical calculation.'
                case _:
                    return 'Failed electrical calculation.'
        except (Exception, TypeError) as error:
            print(f'Error found in calculation_type: {error}')
            return 'Failed electrical calculation.'
    
    
    def basic_calculation(self, electricity_consumption: float, emission_factor: float):
        try:
            if electricity_consumption > 0 and emission_factor > 0:
                
                final_emission = float(electricity_consumption * emission_factor)
                
                print(f'Total basic: {final_emission}')
                return float(final_emission)
            else:
                return 0.0
        except Exception as error:
            print(f'Error found: {error}')
            return 0.0
    
    def accurate_calculation(self, devices: Dict) -> Dict:
        try:
            ordered_devices = self._process_device_data(devices)
            if not ordered_devices:
                return {}
            
            devices_emissions = []
            total_emission = 0.0
            total_consumption = 0
            
            for device in ordered_devices:
                device_emission = self._calculate_single_device_emission(device)
                devices_emissions.append(device_emission)
                total_emission += device_emission['weeklyCarbonEmission']
                total_consumption += device_emission['totalWeeklyConsumption']
            
            print(f'Devices emissions: {devices_emissions}')
            print(f'Total weekly emission: {total_emission} kgCO2e')
            print(f'Total weekly consumption: {total_consumption} Kw')
            
            calculations = {
                "devices": devices_emissions,
                "totalEmission": round(total_emission, 2),
                "totalConsumption": round(total_consumption, 2)
            }
            
            return calculations
        except Exception as error:
            print(f'Error found in calculate_devices_emissions: {error}')
            return {}
        
    def active_use_consume(self, active_power: float, active_used_hours: float):
        try:
            if active_power > 0 and active_used_hours >= 0:
                
                result = float(active_power * active_used_hours)
                
                final_active_consum = float(result / 1000)
                
                return float(final_active_consum)
            else:
                return 0.0
            
        except (Exception, TypeError) as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def active_energy_adjust(self, active_consume: float , device_efficiency: float):
        try:
            if active_consume >= 0 and device_efficiency >= 0:
                
                final_active_consume_adjusted = float(active_consume / device_efficiency)
                
                return float(final_active_consume_adjusted)
            else:
                return 0.0 
        except (Exception, TypeError) as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def standby_consume(self, device_standby_power: float, standby_used_hours: float):
        try:
            if device_standby_power > 0 and standby_used_hours >= 0:
                
                result = float(device_standby_power * standby_used_hours)
                
                final_standby_consum = float(result / 1000)
                
                return float(final_standby_consum)
            else:
                return 0.0
        except (Exception, TypeError) as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def standby_energy_adjust(self, standby_consume: float, device_efficiency: float):
        try:
            if standby_consume >= 0 and device_efficiency >= 0:
                
                final_standby_consume_adjusted = float(standby_consume / device_efficiency)
                
                return float(final_standby_consume_adjusted)
            else:
                return 0.0
        except (Exception, TypeError) as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def _process_device_data(self, devices: Dict) -> List[Dict]:
        try:
            devices_data = []
            device_ids = devices.get('device_id', [])
            
            for i in range(len(device_ids)):
                device_data = {
                    'id': str(devices.get('device_id', [])[i]),
                    'active_power': float(devices.get('device_active_power', [])[i]),
                    'active_hours': float(devices.get('active_used_hours', [])[i]),
                    'standby_power': float(devices.get('device_standby_power', [])[i]),
                    'standby_hours': float(devices.get('standby_used_hours', [])[i]),
                    'device_efficiency': float(devices.get('device_efficiency', [])[i]) / 100,
                }
                devices_data.append(device_data)
            
            return devices_data
        except Exception as error:
            print(f'Error found in _process_device_data: {error}')
            return []
    
    def _calculate_single_device_emission(self, device: Dict) -> Dict:
        device_data = {
            'id': device['id'],
            'deviceActivePower': device['active_power'],
            'activeUsedHours': device['active_hours'],
            'deviceStandbyPower': device['standby_power'],
            'standbyUsedHours': device['standby_hours'],
            'deviceEfficiency': device['device_efficiency'],
        }
        
        # Calculate consumptions
        active_consume = self.active_use_consume(device['active_power'], device['active_hours'])
        device_data['activeConsume'] = round(active_consume, 2)
        
        standby_consume = self.standby_consume(device['standby_power'], device['standby_hours'])
        device_data['standbyConsume'] = round(standby_consume, 2)
        
        # Calculate adjusted consumptions
        adjusted_active = self.active_energy_adjust(active_consume, device['device_efficiency'])
        device_data['adjustedActiveConsume'] = round(adjusted_active, 2)
        
        adjusted_standby = self.standby_energy_adjust(standby_consume, device['device_efficiency'])
        device_data['adjustedStandbyConsume'] = round(adjusted_standby, 2)
        
        # Calculate total daily and weekly consumption
        daily_consumption = adjusted_active + adjusted_standby
        device_data['totalDailyConsumption'] = round(daily_consumption, 2)
        device_data['totalWeeklyConsumption'] = round(daily_consumption * 7, 2)
        
        # Calculate weekly carbon emission
        device_data['weeklyCarbonEmission'] = round(device_data['totalWeeklyConsumption'] * self.emission_factor, 2)
        
        return device_data