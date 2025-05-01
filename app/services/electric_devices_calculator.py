class Electric_devices_calculator:
    
    def calculation_type(self, type: str, electricity_consumption: float, devices: dict):
        emission_factor = 0.438 # by the moment, change as soon as possible
        
        if type == 'basic':
            self.basic_calculation(electricity_consumption, emission_factor)
        elif type == 'accurate':
            self.accurate_calculation(devices, emission_factor)
    
    
    def basic_calculation(electricity_consumption: float, emission_factor: float):
        try:
            if electricity_consumption > 0 and emission_factor > 0:
                
                final_emission = float(electricity_consumption * emission_factor)
                
                return float(final_emission)
            else:
                return 0.0
        except TypeError as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def accurate_calculation(self, devices: dict, emission_factor: float):
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
                'device_efficiency': float(devices['device_efficiency'][i]),
            }
            #Saves each dictionary generated for each device
            devices_data.append(device_data)
            # print('Lista final', devices_data[i])
        print('Lista final', devices_data)

    
    def active_use_consum(active_power: float, active_used_hours: float):
        try:
            if active_power > 0 and active_used_hours >= 0:
                
                result = float(active_power * active_used_hours)
                
                final_active_consum = float(result / 1000)
                
                return float(final_active_consum)
            else:
                return 0.0
            
        except TypeError as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def active_energy_adjust(active_consume: float , device_efficiency: float):
        try:
            if active_consume >= 0 and device_efficiency >= 0:
                
                final_active_consume_adjusted = float(active_consume / device_efficiency)
                
                return float(final_active_consume_adjusted)
            else:
                return 0.0 
        except TypeError as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def standby_consume(device_standby_power: float, standby_used_hours: float):
        try:
            if device_standby_power > 0 and standby_used_hours >= 0:
                
                result = float(device_standby_power * standby_used_hours)
                
                final_standby_consum = float(result / 1000)
                
                return float(final_standby_consum)
            else:
                return 0.0
        except TypeError as error:
            print(f'Error found: {error}')
            return 0.0
    
    
    def standby_energy_adjust(standby_consume: float, device_efficiency: float):
        try:
            if standby_consume >= 0 and device_efficiency >= 0:
                
                final_standby_consume_adjusted = float(standby_consume / device_efficiency)
                
                return float(final_standby_consume_adjusted)
            else:
                return 0.0
        except TypeError as error:
            print(f'Error found: {error}')
            return 0.0