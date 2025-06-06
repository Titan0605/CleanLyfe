document.addEventListener('DOMContentLoaded', async function () {
    show_form('basic_calculation')

    document.getElementById('devices_select_form').addEventListener('submit', async function (e) {
        try {
            e.preventDefault();
            // Collect data from the form
            const formData = new FormData(e.target);
            const data = {};
            // Convert FormData to an object, grouping multiple values into arrays
            formData.forEach((value, key) => {
                if (!data[key]) {
                    data[key] = [];
                }
                data[key].push(value);
            });

            fetch('/carbonfp/get-devices-name-selected', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then(response => response.json())
                .then(responseData => {
                    if (responseData.Status = "Devices collected successfully.") {
                        draw_get_device_info(responseData.devices);
                    }
                })

        } catch (error) {
            console.log(error)
        }
    });

    document.getElementById('container').addEventListener('submit', async function (e) {
        if (e.target && e.target.id === 'devices_info_form') {
            try {
                e.preventDefault();

                const formData = new FormData(e.target)
                const data = {}

                formData.forEach((value, key) => {
                    if (!data[key]) {
                        data[key] = [];
                    }
                    data[key].push(value);
                });

                console.log('Entro a accurate calculation url: ', data)

                fetch('/carbonfp/devices/calculation-accurate', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data) {
                            draw_message(data)
                        }
                    })

            } catch (error) {
                console.log(error);
            }
        } else if (e.target && e.target.id === 'basic_calculation') {
            try {
                e.preventDefault();

                const formData = new FormData(e.target)
                const data = Object.fromEntries(formData)

                console.log('Entro a basic calculation url: ', data)

                fetch('/carbonfp/devices/calculation-basic', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(data),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data) {
                            draw_message(data)
                        }
                    })

            } catch (error) {
                console.log(error);
            }
        }
    });
});

function show_form(form_selected){

    const forms = document.querySelectorAll('.form');
    forms.forEach(form => {
        form.hidden = true
    });

    // Mostrar el formulario seleccionado
    document.getElementById(form_selected).hidden = false;

    // Activar el botón correspondiente
    let botonId;
    if (form_selected === 'basic_calculation') botonId = 'btnBasic';
    else if (form_selected === 'accurate_calculation') botonId = 'btnAccurate';
    
    document.getElementById(botonId).hidden = false;

}

function draw_get_device_info(devices) {
    const container = document.getElementById('container');
    container.innerHTML = ``;

    const device_form = document.createElement('form');
    device_form.id = 'devices_info_form';

    container.appendChild(device_form);
    const form_div = document.createElement('div');
    device_form.appendChild(form_div);

    devices.forEach(device => {
        const device_questions = document.createElement('div');
        device_questions.className = 'bg-amber-100';
        device_questions.innerHTML = `<header class="">
                <i class=""></i>
                <h2 class="text-3xl">${device.name}</h2>
            </header>
            <div>
                <input type="hidden" name="device_id" value="${device.id}">
                <div>
                    <h3 class="">What is the active power of the device?</h3>
                    <input type="number" class="" name="device_active_power" placeholder="Kw" min="1" required>
                </div>
                <div>
                    <h3 class="">Hours of active use</h3>
                    <input type="number" class="" name="active_used_hours" placeholder="Hours" min="0" required>
                </div>
                <div>
                    <h3 class="">What is the standby power of the device?</h3>
                    <input type="number" class="" name="device_standby_power" placeholder="Kw" min="1" required>
                </div>
                <div>
                    <h3 class="">Hours of standby use</h3>
                    <input type="number" class="" name="standby_used_hours" placeholder="Hours" min="0" required>
                </div>
                <div>
                    <h3 class="">What is the efficiency of the device?</h3>
                    <input type="number" class="" name="device_efficiency" placeholder="Kw" min="1" required>
                </div>
            </div>`;

        device_form.appendChild(device_questions);
    })
    
    const footer = document.createElement('footer');
    footer.innerHTML = `<input type="hidden" name="type_calculation" value="accurate_calculation">
            <input type="hidden" name="electricity_consumption" value="0">
            <button type="submit">Continue</button>`

    device_form.appendChild(footer)
}

function draw_message(data) {
    // Gets the div container
    const container = document.getElementById('container');
    // Deletes the inner content
    container.innerHTML = ``;

    // If there is an error in the response shows this
    if (data.Status !== 'Carbonfp successfully.') {
        // Creates a div
        const warning = document.createElement('div');
        // Adds the class name
        warning.className = 'bg-amber-100';
        // Adds the html needed
        warning.innerHTML = `
        <div class="bg-amber-100">
            <p class="text-5xl">${data.Status}</p>
            <button class="bg-amber-300 cursor-pointer">Try again</button>
        </div>
        `;
        // Is apppended to the div container
        container.appendChild(warning);
    } else {
        // Gets the div container
        const successfull = document.createElement('div');
        // Adds the class name
        successfull.className = 'bg-amber-100';
        // Adds the html needed
        successfull.innerHTML = `
        <div class="bg-blue-500">
            <p class="text-5xl">Form answered correctly, advance to the next form.</p>
            <button class="bg-amber-300 cursor-pointer">
                <a href="/carbonfp/products">Go products carbon footprint</a>
            </button>
        </div>
        `;
        // Is apppended to the div container
        container.appendChild(successfull);
    }
}