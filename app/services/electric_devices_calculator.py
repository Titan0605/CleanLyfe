from flask import jsonify
class Electric_devices_calculator:
    
    def calculation_type(self, type_calculation: str, electricity_consumption: float, devices: dict):
        try:
            emission_factor = 0.438 # by the moment, change as soon as possible
            
            match type_calculation:
                case 'basic_calculation':
                    self.basic_calculation(electricity_consumption, emission_factor)
                case 'accurate_calculation':
                    self.accurate_calculation(devices)
                case _:
                    return jsonify({'Status': 'Failed electrical calculation.'})
        
            return jsonify({'Status': 'Electric calculation successfully.'})
        except (Exception, TypeError) as error:
            print(f'Error found: {error}')
            return jsonify({'Status': 'Failed electrical calculation.'})
    
    
    def basic_calculation(electricity_consumption: float, emission_factor: float):
        try:
            if electricity_consumption > 0 and emission_factor > 0:
                
                final_emission = float(electricity_consumption * emission_factor)
                
                return float(final_emission)
            else:
                return 0.0
        except Exception as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def accurate_calculation(self, devices: dict):
        try:
            # Order the devices for easier handling
            devices = self.order_devices(devices)
            
            if devices:
                # List that stores each device with its total emissions
                devices_emissions = []
                # Total sum of all devices emissions
                total_final_emission = 0
                
                for device in devices:
                    final_active_use_consume = self.active_use_consume(device['active_power'], device['active_hours'])
                    # this
                    final_active_energy_adjust = self.active_energy_adjust(final_active_use_consume, device['device_efficiency'])
                    
                    final_standby_consume = self.standby_consume(device['standby_power'], device['standby_hours'])
                    # this
                    final_standby_energy_adjust = self.standby_energy_adjust(final_standby_consume, device['device_efficiency'])
                    
                    total_emission = round(final_active_energy_adjust + final_standby_energy_adjust, 3)
                    
                    devices_data = {
                        'id': int(device['id']),
                        'active_energy_consumed': round(final_active_energy_adjust, 3),
                        'standby_energy_consumed': round(final_standby_energy_adjust, 3),
                        'total_emission': total_emission
                    }
                    
                    for device in devices_emissions:
                        
                        total_final_emission = round(total_final_emission + device['total_emission'], 3)
                    
                    devices_emissions.append(devices_data)
                
                return total_final_emission
            else:
                return None
        except Exception as error:
            print(f'Error found: {error}')
            return None
    
    def order_devices(self, devices: list):
        try:
            # list to save each data of each device individually
            devices_data = []
            
            #Iterate each device data collected
            for i in range(len(devices['device_id'])):
                device_data = {
                    'id': int(devices['device_id'][i]),
                    'active_power': float(devices['device_active_power'][i]),
                    'active_hours': float(devices['active_used_hours'][i]),
                    'standby_power': float(devices['device_standby_power'][i]),
                    'standby_hours': float(devices['standby_used_hours'][i]),
                    'device_efficiency': float(devices['device_efficiency'][i]) / 100,
                }
                #Saves each dictionary generated for each device
                devices_data.append(device_data)
            
            return devices_data
        except Exception as error:
            print(f'Error found: {error}')
            return []
    
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