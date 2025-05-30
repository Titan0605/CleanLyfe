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
    .then((result) => {
      console.log("Succes:", result);
      window.location.href = "/home";
    })
    .catch((error) => {
      console.error(error);
    });
});
