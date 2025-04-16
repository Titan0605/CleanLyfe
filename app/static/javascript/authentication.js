document.addEventListener("DOMContentLoaded", async function() {
    try {
        document.getElementById("sign_up_form").addEventListener("submit", async function (e) {
            e.preventDefault();
            // Collect the data from the form
            var formData = new FormData(e.target);
            var data = Object.fromEntries(formData);                  
    
            fetch("/sign_up_service", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {            
                if (data.Status === "Sign up successfull.") {
                    // redirect to home
                    window.location.href = '/login';
                } else {
                    // error login manage
                    alert("Fail sign up. Verify your password confirmation.");
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert("Conection error. Try later.");
            });
        });    
    } catch (error) {
        console.log(error);
    }

    try {
        document.getElementById("login_form").addEventListener("submit", async function (e) {
            e.preventDefault();
    
            var formData = new FormData(e.target);
            var data = Object.fromEntries(formData);
    
            console.log(data);
    
            fetch("/login_service", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {            
                if (data.Status === "Login successfull.") {
                    // redirect to home
                    window.location.href = '/home';
                } else {
                    // error login manage
                    alert("Fail login. Verify your credentials.");
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert("Conection error. Try later.");
            });
        });    
    } catch (error) {
        console.log(error);
    }    
})