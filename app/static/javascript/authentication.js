document.addEventListener("DOMContentLoaded", function () {
  const handleResponse = async (response) => {
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || "Something went wrong");
    }
    return data;
  };

  const showError = (message) => {
    alert(message);
  };

  // Sign up form handler
  const signUpForm = document.getElementById("sign_up_form");
  if (signUpForm) {
    signUpForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      try {
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        const response = await fetch("/sign_up_service", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        const result = await handleResponse(response);

        if (result.status === "success") {
          window.location.href = "/login";
        } else {
          showError(result.message);
        }
      } catch (error) {
        console.error("Sign up error:", error);
        showError(error.message);
      }
    });
  }

  // Login form handler
  const loginForm = document.getElementById("login_form");
  if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      try {
        const formData = new FormData(e.target);
        const data = Object.fromEntries(formData);

        const response = await fetch("/login_service", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        const result = await handleResponse(response);

        if (result.status === "success") {
          window.location.href = "/home";
        } else {
          showError(result.message);
        }
      } catch (error) {
        console.error("Login error:", error);
        showError(error.message);
      }
    });
  }

  // Logout handler
  const logoutButtons = document.querySelectorAll(".logout");
  if (logoutButtons) {
    logoutButtons.forEach((logoutButton) => {
      logoutButton.addEventListener("click", async function () {
        try {
          const response = await fetch("/logout", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          });

          const result = await handleResponse(response);

          if (result.status === "success") {
            window.location.href = "/";
          } else {
            showError(result.message);
          }
        } catch (error) {
          console.error("Logout error:", error);
          showError(error.message);
        }
      });
    });
  }
});
