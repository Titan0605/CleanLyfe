const users = {
    firstName: 'admin',
    lastName: 'admin',
    userName: 'admin',
    email: 'admin@worldmatters.com',
    password: "12345678",
    memberType: 'guest | user | premium | admin',
    waterFlows: [
        ObjectId("waterflow_id"),
    ],
    active: true,
    createdAt: new Date(),
    updatedAt: [
        {
            action: "Member Update",
            date: new Date()
        }
    ],
    notifications: [{
        "notification_type": "temperature",
        "message": "The temperature is too low"
    }]
}

const waterFlows = {
    MAC: "4f:34:f4:j5",
    stateHistory: [
        {
            state: "close | open",
            date: new Date()
        }
    ],
    historytemp: [
        {
            temp: 34,
            date: new Date()
        }
    ],
    currentTemp: 34,
    autoCloseTemp: 0,
    autoClose: true,
    active: false
}

const deviceCatalog = {
  deviceName: "Vacuum",
  deviceZone: "Others",
  active: true
}

const energyDevices = {
    deviceType: ObjectId("deviceCatalog"),
    deviceActivePower: 20,
    activeUsedHours: 50,
    deviceStandbyPower: 5,
    standbyUsedHours: 8,
    deviceEfficiency: 0.80,
    activeConsume: 20,
    standbyConsume: 5,
    adjustedActiveConsume: 18,
    asjustedStandbyConsume: 2,
    totalDailyConsumption: 30,
    totalWeeklyConsumption: 210,
    weeklyCarbonEmission: 510
}

const footprintCalculations = {
    userId: ObjectId("user_id"),
    calculationType: "carbon | hydric | combined",
    createdAt: new Date(),
    active: false,
    carbonFootprint: {
        totalCarbonEmission: 30,
        transport: {
            fuelUsed: "Gas",
            cylinderRating: 4,
            vehicleYear: 2005,
            timeUsedHours: 5,
            consumedFuel: 20,
            distanceTraveled: 50,
            fuelPerfomance: 15,
            totalEmission: 2350
        },
        energy: {
            totalEnergyConsumption: 340,
            totalEmission: 230,
            devices: [ // Varios dispositivos
                ObjectId("device_id"),
            ]
        },
        products: {
            totalEmission: 340,
            productsEmissions:[ // Varios productos
                {
                    carbonProductId: ObjectId("carbon_product_id"),
                    quantity: 2,
                    totalProductEmission: 320
                }
            ]
        },
        water: {
            coldWaterLiters: 50,
            hotWaterLiters: 40,
            coldWaterEmission: 20,
            hotWaterEmission: 80,
            totalEmission: 430
        }
    },
    hydricFootprint: {
        totalHydricFootprint: 320,
        normalWaterConsumption: {
            showerConsumption: 40,
            toiletConsumption: 50,
            dishesConsumption: 30,
            washingMachineConsumption: 60,
            gardenConsumption: 10,
            houseCleaning: 43,
            totalWaterConsumption: 540 
        },
        productsWaterConsumption: {
            totalWaterConsumptionProducts: 540,
            productsConsumptions: [
                {
                    objectId: ObjectId("water_product_id"),
                    productsConsumption: 43
                }
            ]
        }
    }
}