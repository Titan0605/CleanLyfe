document.addEventListener("DOMContentLoaded", async function() {
    // Sign up
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
                console.log('Error:', error);
                alert("Something went wrong when signing up. Try later.");
            });
        });    
    } catch (error) {
        console.log(error);
    }

    // Log in
    try {
        document.getElementById("login_form").addEventListener("submit", async function (e) {
            e.preventDefault();
    
            var formData = new FormData(e.target);
            var data = Object.fromEntries(formData);
    
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
                    alert(data.Status);
                }
            })
            .catch((error) => {
                console.log('Error:', error);
                alert(data.Status);
            });
        });    
    } catch (error) {
        console.log(error);
    }    

    // Log out
    try {
        document.getElementById("logout").addEventListener("click", async function () {
            console.log("Log out clicked")
            fetch("/logout", {
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data =>{
                if(data.Status === "Log out successfull."){
                    // redirect to root
                    window.location.href = "/"
                }
            })
        })
    } catch (error) {
        console.log('Error:', error);
    }
})