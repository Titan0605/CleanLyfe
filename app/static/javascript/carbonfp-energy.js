document.addEventListener("DOMContentLoaded", function () {
  show_form("basic_calculation");

  // Handle continue button click
  document.getElementById("continue-btn").addEventListener("click", async function () {
    const checkedDevices = document.querySelectorAll(".device-checkbox:checked");
    if (checkedDevices.length === 0) {
      alert("Please select at least one device");
      return;
    }

    // Get selected devices IDs
    const selectedIds = Array.from(checkedDevices).map((checkbox) => checkbox.value);

    try {
      const response = await fetch("/carbonfp/get-devices-name-selected", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ device: selectedIds }),
      });

      const result = await response.json();
      if (result.Status === "Devices collected successfully.") {
        // Show device info forms for selected devices
        checkedDevices.forEach((checkbox) => {
          const deviceWrapper = checkbox.closest(".device-wrapper");
          const deviceName = deviceWrapper.querySelector("label").textContent;

          // Create device info form
          const deviceInfo = document.createElement("div");
          deviceInfo.className = "device-info ml-4 mt-2";
          deviceInfo.setAttribute("data-device-id", checkbox.value);
          deviceInfo.innerHTML = `
                        <div class="grid grid-cols-2 gap-2">
                            <div>
                                <label class="block text-xs">Active Power (kW)</label>
                                <input type="number" name="device_active_power" step="0.01" min="0" class="w-full bg-gray-700 rounded px-2 py-1" required>
                            </div>
                            <div>
                                <label class="block text-xs">Active Hours/Day</label>
                                <input type="number" name="active_used_hours" step="0.5" min="0" max="24" class="w-full bg-gray-700 rounded px-2 py-1" required>
                            </div>
                            <div>
                                <label class="block text-xs">Standby Power (kW)</label>
                                <input type="number" name="device_standby_power" step="0.01" min="0" class="w-full bg-gray-700 rounded px-2 py-1" required>
                            </div>
                            <div>
                                <label class="block text-xs">Standby Hours/Day</label>
                                <input type="number" name="standby_used_hours" step="0.5" min="0" max="24" class="w-full bg-gray-700 rounded px-2 py-1" required>
                            </div>
                            <div class="col-span-2">
                                <label class="block text-xs">Device Efficiency (%)</label>
                                <input type="number" name="device_efficiency" min="1" max="100" class="w-full bg-gray-700 rounded px-2 py-1" value="100" required>
                            </div>
                        </div>
                    `;
          deviceWrapper.appendChild(deviceInfo);
        });

        // Hide continue button and show calculate button
        document.getElementById("continue-btn").classList.add("hidden");
        document.getElementById("calculate-btn").classList.remove("hidden");
      } else {
        alert("Error retrieving device information");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while processing your request");
    }
  });

  // Handle form submission for calculation
  document.getElementById("devices_select_form").addEventListener("submit", async function (e) {
    try {
      e.preventDefault();

      const data = {
        device_id: [],
        device_active_power: [],
        active_used_hours: [],
        device_standby_power: [],
        standby_used_hours: [],
        device_efficiency: [],
        type_calculation: ["accurate_calculation"],
        electricity_consumption: "0",
      };

      // Get all device info inputs
      const deviceInfos = document.querySelectorAll(".device-info");
      deviceInfos.forEach((deviceInfo) => {
        data.device_id.push(deviceInfo.getAttribute("data-device-id"));
        data.device_active_power.push(deviceInfo.querySelector('[name="device_active_power"]').value);
        data.active_used_hours.push(deviceInfo.querySelector('[name="active_used_hours"]').value);
        data.device_standby_power.push(deviceInfo.querySelector('[name="device_standby_power"]').value);
        data.standby_used_hours.push(deviceInfo.querySelector('[name="standby_used_hours"]').value);
        data.device_efficiency.push(deviceInfo.querySelector('[name="device_efficiency"]').value);
      });

      const response = await fetch("/carbonfp/devices/calculation-accurate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      draw_message(result);
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while processing your request - Accurate Calculation");
    }
  });

  // Basic calculation form handler
  document.getElementById("basic_calculation").addEventListener("submit", async function (e) {
    try {
      e.preventDefault();
      const formData = new FormData(e.target);
      const data = {
        type_calculation: formData.get("type_calculation"),
        electricity_consumption: formData.get("electricity_consumption"),
      };

      const response = await fetch("/carbonfp/devices/calculation-basic", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      draw_message(result);
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while processing your request - Basic Calculation");
    }
  });
});

function show_form(form_selected) {
  const forms = document.querySelectorAll(".form");
  forms.forEach((form) => {
    form.hidden = true;
  });

  // Mostrar el formulario seleccionado
  document.getElementById(form_selected).hidden = false;

  // Activar el botón correspondiente
  let botonId;
  if (form_selected === "basic_calculation") botonId = "btnBasic";
  else if (form_selected === "accurate_calculation") botonId = "btnAccurate";

  document.getElementById(botonId).hidden = false;
}

function draw_get_device_info(devices) {
  const container = document.getElementById("container");
  container.innerHTML = ``;

  const device_form = document.createElement("form");
  device_form.id = "devices_info_form";
  container.appendChild(device_form);

  devices.forEach((device) => {
    const device_questions = document.createElement("div");
    device_questions.className = "bg-amber-100 device-info";
    device_questions.setAttribute("data-device-id", device.id);
    device_questions.innerHTML = `<header class="">
                <i class=""></i>
                <h2 class="text-3xl">${device.deviceName}</h2>
            </header>
            <div>
                <input type="hidden" name="device_id" value="${device.id}">
                <div>
                    <h3 class="">What is the active power of the device?</h3>
                    <input type="number" class="" name="device_active_power" placeholder="Kw" min="1" required>
                </div>
                <div>
                    <h3 class="">Hours of active use</h3>
                    <input type="number" class="" name="active_used_hours" placeholder="Hours" min="0" required>
                </div>
                <div>
                    <h3 class="">What is the standby power of the device?</h3>
                    <input type="number" class="" name="device_standby_power" placeholder="Kw" min="1" required>
                </div>
                <div>
                    <h3 class="">Hours of standby use</h3>
                    <input type="number" class="" name="standby_used_hours" placeholder="Hours" min="0" required>
                </div>
                <div>
                    <h3 class="">What is the efficiency of the device?</h3>
                    <input type="number" class="" name="device_efficiency" placeholder="Kw" min="1" required>
                </div>
            </div>`;

    device_form.appendChild(device_questions);
  });

  const footer = document.createElement("footer");
  footer.innerHTML = `<input type="hidden" name="type_calculation" value="accurate_calculation">
            <input type="hidden" name="electricity_consumption" value="0">
            <button type="submit">Continue</button>`;

  device_form.appendChild(footer);
}

function draw_message(data) {
  // Gets the div container
  const container = document.getElementById("container");
  // Deletes the inner content
  container.innerHTML = ``;

  // If there is an error in the response shows this
  if (data.Status !== "Energy calculated successfully.") {
    // Creates a div
    const warning = document.createElement("div");
    // Adds the class name
    warning.className = "bg-amber-100";
    // Adds the html needed
    warning.innerHTML = `
        <div class="bg-amber-100">
            <p class="text-5xl">${data.Status}</p>
            <button class="bg-amber-300 cursor-pointer">
              <a href="/carbonfp/energy">Try again</a>
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
                <a href="/carbonfp/products">Go products carbon footprint</a>
            </button>
        </div>
        `;
    // Is apppended to the div container
    container.appendChild(successfull);
  }
}
