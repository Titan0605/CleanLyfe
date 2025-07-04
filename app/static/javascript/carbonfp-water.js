document.getElementById("water_emission_form").addEventListener("submit", (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);
  const data = Object.fromEntries(formData.entries());

  Object.keys(data).forEach((key) => {
    if (!isNaN(Number(data[key]))) {
      data[key] = Number(data[key]);
    }
  });

  console.log(data);

  fetch("/carbonfp/water/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      draw_message(data);
    })
    .catch((error) => {
      console.error(error);
    });
});

function draw_message(data) {
  // Gets the div container
  const container = document.getElementById("container");
  // Deletes the inner content
  container.innerHTML = ``;

  // If there is an error in the response shows this
  if (data.Status !== "Water calculation successfully.") {
    // Creates a div
    const warning = document.createElement("div");
    // Adds the class name
    warning.className = "bg-amber-100";
    // Adds the html needed
    warning.innerHTML = `
        <div class="bg-amber-100">
            <p class="text-5xl">${data.Status}</p>
            <button class="bg-amber-300 cursor-pointer">
              <a href="/carbonfp/water">Try again</a>
            </button>
        </div>
        `;
    // Is apppended to the div container
    container.appendChild(warning);
  } else {
    // Gets the div container
    const successfull = document.createElement("div");
    // Adds the class name
    successfull.className = "bg-amber-100";
    // Adds the html needed
    successfull.innerHTML = `
        <div class="bg-blue-500">
            <p class="text-5xl">${data.Status}</p>
            <p class="text-5xl">${data.message}</p>
            <button class="bg-amber-300 cursor-pointer">
                <a href="/home">Return to Home</a>
            </button>
        </div>
        `;
    // Is apppended to the div container
    container.appendChild(successfull);
  }
}