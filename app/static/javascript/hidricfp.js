document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('hidric_form').addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent the default form submission
    
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());
        
        Object.keys(data).forEach((key) => {
            if(!isNaN(Number(data[key]))) {
                data[key] = Number(data[key]);
            }
        });

        console.log('Form data:', data); // Log the form data to the console

        fetch('/hidricfp/calculation', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            console.log('Success:', result);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});