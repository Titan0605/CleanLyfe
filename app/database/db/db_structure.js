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
    ]
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

const energyDevices = {
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
        totalEmission: 30,
        transport: {
            idFuelUsed: ObjectId("fuel_id"),
            cylinderRatingId: ObjectId("cylinder_id"),
            vehicleYearId: ObjectId("year_id"),
            timeUsedHours: 5,
            consumedFuel: 20,
            distanceTraveled: 50,
            fuelPerfomance: 15,
            transportEmission: 2350
        },
        energy: {
            totalEnergyConsumption: 340,
            energyEmission: 230,
            devices: [ // Varios dispositivos
                ObjectId("device_id"),
            ]
        },
        products: {
            totalProductsEmission: 340,
            productsEmissions:[ // Varios productos
                {
                    carbonProductId: ObjectId("carbon_product_id"),
                    quantity: 2,
                    totalProductEmission: 320
                }
            ]
        },
        water: {
            hotWaterVolume: 40,
            coldWaterVolume: 50,
            hotWaterEmission: 80,
            coldWaterEmission: 20,
            waterEmission: 430
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