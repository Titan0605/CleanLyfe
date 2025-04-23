document.addEventListener("DOMContentLoaded", async function() {
    try {
        document.getElementById("form_carbonfp_transport").addEventListener("submit", async function(e){
            e.preventDefault();
            // Collect data from the form
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            console.log(data);

            fetch("/carbonfp/transport-data", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.log("show message error")
                } else {
                    console.log("show next footprint survey")
                }
            })
        })
    } catch (error) {
        console.log("Error", error)
    }
})