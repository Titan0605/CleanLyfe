document.addEventListener('DOMContentLoaded', async function() {
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
            
            // fetch('/carbonfp/get-devices-selected', {
            //     method: 'POST',
            //     headers: {
            //         "Content-Type": "application/json",
            //     },
            //     body: JSON.stringify(data),
            // })
    
            console.log(data);

            get_device_info(data);
        } catch (error) {
            console.log(error)
        }
    });
});

function get_device_info(data) {
    const container = getElementById('container');
    container.innerHTML = ``;

    const device_form = document.createElement('form');
    device_form.id = 'devices_info_form';

    data.forEach(device => {
        
    })
}