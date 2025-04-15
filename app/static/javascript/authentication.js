document.addEventListener("DOMContentLoaded", async function() {
    document.getElementById("sign_up_form").addEventListener("submit", async function (e) {
        e.preventDefault();
        // Collect the data from the form
        var formData = new FormData(e.target);
        var data = Object.fromEntries(formData);                  

        fetch("/sign_up", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
    })

    document.getElementById("login_form").addEventListener("submit", async function (e) {
        e.preventDefault();

        var formData = new FormData(e.target);
        var data = Object.fromEntries(formData);

        fetch("/login", {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
    })
})