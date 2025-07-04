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
                drawMessage(data);
            })
        })
    } catch (error) {
        console.log("Error", error)
    }
})

function drawMessage(data) {
    // Gets the div container
    const container = document.getElementById('container');
    // Deletes the inner content
    container.innerHTML = ``;

    // If there is an error in the response shows this
    if(data.error){
        // Creates a div
        const warning = document.createElement('div');
        // Adds the class name
        warning.className = 'bg-amber-100';
        // Adds the html needed
        warning.innerHTML = `
        <div class="bg-amber-100">
            <p class="text-5xl">${data.error}</p>
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
                <a href="/carbonfp/energy">Go devices carbon footprint</a>
            </button>
        </div>
        `;
        // Is apppended to the div container
        container.appendChild(successfull);
    }
}