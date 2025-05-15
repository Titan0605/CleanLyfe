document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('hidric_form').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission
    
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());
        let products = {}
        
        Object.keys(data).forEach((key) => {
            if(!isNaN(Number(data[key]))) {
                data[key] = Number(data[key]);
            }

            key_parts = key.split('_')
            if(key_parts[0] == 'product') {
                products[key_parts[1]] = data[key]
                delete data[key]
            }
        });

        data['products'] = products

        // console.log('Products List:', products)
        // console.log('Form data:', data); // Log the form data to the console

        fetch('/hidricfp/calculation', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            window.location.href = '/home'
            // console.log('Success:', result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});