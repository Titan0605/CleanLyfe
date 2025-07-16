document.addEventListener("DOMContentLoaded", async function () {
  document.getElementById("products_info_form").hidden = true;

  document.getElementById("products_select_form").addEventListener("submit", async function (e) {
    e.preventDefault();
    // Collect data from the form
    const formData = new FormData(e.target);
    const data = {};
    // Convert FormData to an object, grouping multiple values into arrays
    formData.forEach((value, key) => {
      if (!data[key]) {
        data[key] = [];
      }
      data[key].push(value);
    });

    console.log("Productos elegidos: ", data);

    fetch("/carbonfp/products/get-products-selected", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((responseData) => {
        if (responseData.Status == "Valid response.") {
          draw_products_selected(data);
        } else if (responseData.Status == "You must choose at least one.") {
          draw_message();
        }
      });
  });
});

function draw_products_selected(data) {
  // Hides the form to choose the products
  document.getElementById("products_select_form").hidden = true;
  // Shows the form of the products
  document.getElementById("products_info_form").hidden = false;
  // Select the section of each product
  const products_forms = document.querySelectorAll(".product");
  // Hides the section of each product
  products_forms.forEach((form) => {
    form.hidden = true;
  });


  // Shows the first section of the products selected
  let currentIndex = 0;
  document.getElementById(data.product[currentIndex]).hidden = false;
  document.getElementById("navigation_btns").hidden = false;

  const nextBtn = document.getElementById("next_btn");
  const prevBtn = document.getElementById("preview_btn");
  const finishBtn = document.getElementById("finish_btn");

  if (data.product.length === 1) {
    // Only one product selected: show only the finish button
    nextBtn.hidden = true;
    prevBtn.hidden = true;
    finishBtn.hidden = false;
  } else {
    // Multiple products: normal navigation
    prevBtn.hidden = true;
    finishBtn.hidden = true;
    nextBtn.hidden = false;

    nextBtn.addEventListener("click", function () {
      if (currentIndex < data.product.length - 1) {
        // Hide the current section
        document.getElementById(data.product[currentIndex]).hidden = true;
        // Move to the next section
        currentIndex++;
        // Show the next section
        document.getElementById(data.product[currentIndex]).hidden = false;

        navigation_btn(currentIndex, nextBtn, prevBtn, data);
      }
    });

    prevBtn.addEventListener("click", function () {
      if (currentIndex > 0) {
        // Hide the current section
        document.getElementById(data.product[currentIndex]).hidden = true;
        // Move to the previous section
        currentIndex--;
        // Show the previous section
        document.getElementById(data.product[currentIndex]).hidden = false;
      }

      navigation_btn(currentIndex, nextBtn, prevBtn, data);
    });
  }

  document.getElementById("products_info_form").addEventListener("submit", function (e) {
    get_products_info(e);
  });
}

async function get_products_info(e) {
  e.preventDefault();

  // Detectar qué secciones están seleccionadas
  const selectedSections = [];
  document.querySelectorAll('#products_select_form input[name="product"]:checked').forEach((cb) => {
    selectedSections.push(cb.value);
  });

  const products = [];

  // --- FOOD SECTION ---
  if (selectedSections.includes("food_section")) {
    // Carnes
    const transport = document.querySelector('input[name="meat_transport"]:checked')?.value || "";
    const packaging = document.querySelector('input[name="meat_packing"]:checked')?.value || "";
    const refrigeration = document.querySelector('input[name="meat_refrigeration"]:checked')?.value || "";
    // Beef
    const beef = parseFloat(document.querySelector('input[name="cow_meat_kg"]').value) || 0;
    if (beef > 0) {
      products.push({
        product_type: "beef",
        quantity: beef,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "beef",
      });
    }
    // Pork
    const pork = parseFloat(document.querySelector('input[name="pork_meat_kg"]').value) || 0;
    if (pork > 0) {
      products.push({
        product_type: "pork",
        quantity: pork,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "pork",
      });
    }
    // Chicken
    const chicken = parseFloat(document.querySelector('input[name="chicken_meat_kg"]').value) || 0;
    if (chicken > 0) {
      products.push({
        product_type: "chicken",
        quantity: chicken,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "chicken",
      });
    }
  }

  // --- DAIRY SECTION ---
  if (selectedSections.includes("dairy_section")) {
    const transport = document.querySelector('input[name="dairy_transport"]:checked')?.value || "";
    const packaging = document.querySelector('input[name="dairy_packing"]:checked')?.value || "";
    const refrigeration = document.querySelector('input[name="dairy_refrigeration"]:checked')?.value || "";
    // Milk
    const milk = parseFloat(document.querySelector('input[name="milk_liters"]').value) || 0;
    if (milk > 0) {
      products.push({
        product_type: "milk",
        quantity: milk,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "milk",
      });
    }
    // Cheese
    const cheese = parseFloat(document.querySelector('input[name="cheese_kg"]').value) || 0;
    if (cheese > 0) {
      products.push({
        product_type: "cheese",
        quantity: cheese,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "cheese",
      });
    }
  }

  // --- FRUITS SECTION ---
  if (selectedSections.includes("fruits_section")) {
    const transport = document.querySelector('input[name="fruits_transport"]:checked')?.value || "";
    const packaging = document.querySelector('input[name="fruits_packing"]:checked')?.value || "";
    const refrigeration = document.querySelector('input[name="fruits_refrigeration"]:checked')?.value || "";
    // Local
    const local = parseFloat(document.querySelector('input[name="local_fruits_kg"]').value) || 0;
    if (local > 0) {
      products.push({
        product_type: "local_produce",
        quantity: local,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "local_fruits",
      });
    }
    // Greenhouse
    const greenhouse = parseFloat(document.querySelector('input[name="greenhouse_fruits_kg"]').value) || 0;
    if (greenhouse > 0) {
      products.push({
        product_type: "greenhouse_produce",
        quantity: greenhouse,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "greenhouse_fruits",
      });
    }
    // Imported
    const imported = parseFloat(document.querySelector('input[name="imported_fruits_kg"]').value) || 0;
    if (imported > 0) {
      products.push({
        product_type: "imported_produce",
        quantity: imported,
        transport: mapTransport(transport),
        packaging: mapPackaging(packaging),
        refrigeration: mapRefrigeration(refrigeration),
        product_id: "imported_fruits",
      });
    }
  }

  // --- CLOTHES SECTION ---
  if (selectedSections.includes("clothes_section")) {
    // No transport/packaging/refrigeration para ropa
    const tshirt = parseInt(document.querySelector('input[name="tshirt_units"]').value) || 0;
    if (tshirt > 0) {
      products.push({
        product_type: "tshirt",
        quantity: tshirt,
        transport: "local",
        packaging: "none",
        refrigeration: "ambient",
        product_id: "tshirt",
      });
    }
    const jeans = parseInt(document.querySelector('input[name="jeans_units"]').value) || 0;
    if (jeans > 0) {
      products.push({
        product_type: "jeans",
        quantity: jeans,
        transport: "local",
        packaging: "none",
        refrigeration: "ambient",
        product_id: "jeans",
      });
    }
    const shoes = parseInt(document.querySelector('input[name="shoes_pairs"]').value) || 0;
    if (shoes > 0) {
      products.push({
        product_type: "shoes",
        quantity: shoes,
        transport: "local",
        packaging: "none",
        refrigeration: "ambient",
        product_id: "shoes",
      });
    }
  }

  // --- ELECTRICAL SECTION ---
  if (selectedSections.includes("electrical_section")) {
    const smartphone = parseInt(document.querySelector('input[name="smartphone_units"]').value) || 0;
    if (smartphone > 0) {
      products.push({
        product_type: "smartphone",
        quantity: smartphone,
        transport: "international",
        packaging: "minimal",
        refrigeration: "ambient",
        product_id: "smartphone",
      });
    }
    const laptop = parseInt(document.querySelector('input[name="laptop_units"]').value) || 0;
    if (laptop > 0) {
      products.push({
        product_type: "laptop",
        quantity: laptop,
        transport: "international",
        packaging: "minimal",
        refrigeration: "ambient",
        product_id: "laptop",
      });
    }
    const tv = parseInt(document.querySelector('input[name="tv_units"]').value) || 0;
    if (tv > 0) {
      products.push({
        product_type: "tv",
        quantity: tv,
        transport: "international",
        packaging: "minimal",
        refrigeration: "ambient",
        product_id: "tv",
      });
    }
  }

  // --- CLEANING SECTION ---
  if (selectedSections.includes("cleaning_section")) {
    const detergent = parseFloat(document.querySelector('input[name="detergent_kg"]').value) || 0;
    if (detergent > 0) {
      products.push({
        product_type: "detergent",
        quantity: detergent,
        transport: "national",
        packaging: "excessive",
        refrigeration: "ambient",
        product_id: "detergent",
      });
    }
    const softener = parseFloat(document.querySelector('input[name="softener_liters"]').value) || 0;
    if (softener > 0) {
      products.push({
        product_type: "softener",
        quantity: softener,
        transport: "national",
        packaging: "excessive",
        refrigeration: "ambient",
        product_id: "softener",
      });
    }
    const cleaner = parseFloat(document.querySelector('input[name="cleaner_liters"]').value) || 0;
    if (cleaner > 0) {
      products.push({
        product_type: "cleaner",
        quantity: cleaner,
        transport: "national",
        packaging: "excessive",
        refrigeration: "ambient",
        product_id: "cleaner",
      });
    }
  }

  // Enviar al backend
  fetch("/carbonfp/products/get-products-info", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ products }),
  })
    .then((response) => response.json())
    .then((responseData) => {
        draw_message(responseData);
    });
}

// Helpers para mapear valores del form a los valores del backend
function mapTransport(val) {
  if (val === "transport_local") return "local";
  if (val === "transport_regional") return "regional";
  if (val === "transport_national") return "national";
  if (val === "transport_international") return "international";
  return "local";
}
function mapPackaging(val) {
  if (val === "Without_packing") return "none";
  if (val === "minimun_packing") return "minimal";
  if (val === "excessive_packing") return "excessive";
  return "none";
}
function mapRefrigeration(val) {
  if (val === "ambient_temperature") return "ambient";
  if (val === "refrigerated") return "refrigerated";
  if (val === "frozen") return "frozen";
  return "ambient";
}

function navigation_btn(currentIndex, nextBtn, prevBtn, data) {
  if (currentIndex == data.product.length - 1) {
    document.getElementById("finish_btn").hidden = false;
    prevBtn.hidden = false;
    nextBtn.hidden = true;
  } else if (currentIndex == 0) {
    document.getElementById("finish_btn").hidden = true;
    prevBtn.hidden = true;
    nextBtn.hidden = false;
  } else if (currentIndex == 0 && data.product.length == 1){
    document.getElementById("finish_btn").hidden = false;
    nextBtn.hidden = true;
  } else {
    document.getElementById("finish_btn").hidden = true;
    nextBtn.hidden = false;
    prevBtn.hidden = false;
  }
}

function draw_message(data) {
  // Gets the div container
  const container = document.getElementById("container");
  // Deletes the inner content
  container.innerHTML = ``;

  // If there is an error in the response shows this
  if (data.Status !== "Products calculation successfully.") {
    // Creates a div
    const warning = document.createElement("div");
    // Adds the class name
    warning.className = "bg-amber-100";
    // Adds the html needed
    warning.innerHTML = `
        <div class="bg-amber-100">
            <p class="text-5xl">${data.Status}</p>
            <button class="bg-amber-300 cursor-pointer">
                <a href="/carbonfp/products">Try again</a>
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
            <p class="text-5xl">Form answered correctly, advance to the next form.</p>
            <button class="bg-amber-300 cursor-pointer">
                <a href="/carbonfp/water">Go water carbon footprint</a>
            </button>
        </div>
        `;
    // Is apppended to the div container
    container.appendChild(successfull);
  }
}
