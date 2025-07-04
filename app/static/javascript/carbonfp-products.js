document.addEventListener('DOMContentLoaded', async function () {
    
    document.getElementById('products_info_form').hidden = true;

    document.getElementById('products_select_form').addEventListener('submit', async function (e) {
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

        console.log('Productos elegidos: ', data)

        fetch('/carbonfp/products/get-products-selected', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(responseData => {
            if(responseData.Status == 'Valid response.'){
                draw_products_selected(data);
            } else if (responseData.Status == 'You must choose at least one.'){
                draw_message();
            }
        });
    });
});

function draw_products_selected(data) {
    // Hides the form to choose the products
    document.getElementById('products_select_form').hidden = true;
    // Shows the form of the products
    document.getElementById('products_info_form').hidden = false;
    // Select the section of each product
    const products_forms = document.querySelectorAll('.product')
    // Hides the section of each product
    products_forms.forEach(form => {
        form.hidden = true
    });
    
    // Shows the first section of the products selected
    let currentIndex = 0;
    document.getElementById(data.product[currentIndex]).hidden = false;
    document.getElementById('navigation_btns').hidden = false;

    // Navigation buttons
    const nextBtn = document.getElementById('next_btn');
    const prevBtn = document.getElementById('preview_btn');
    prevBtn.hidden = true;

    nextBtn.addEventListener('click', function () {
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

    prevBtn.addEventListener('click', function () {
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

    document.getElementById('products_info_form').addEventListener('submit', function(e){
        get_products_info(e);
    })

}


async function get_products_info(e){
    e.preventDefault();

    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    fetch('/carbonfp/products/get-products-info', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(responseData => {
        if(responseData.Status == 'Products calculation successfully.'){
            draw_message(responseData)
        }
    })
}

function navigation_btn(currentIndex, nextBtn, prevBtn, data){
    if(currentIndex == data.product.length - 1){
        document.getElementById('finish_btn').hidden = false;
        prevBtn.hidden = false;
        nextBtn.hidden = true;
    } else if (currentIndex == 0) {
        document.getElementById('finish_btn').hidden = true;
        prevBtn.hidden = true;
    }
    else {
        document.getElementById('finish_btn').hidden = true;
        nextBtn.hidden = false;
        prevBtn.hidden = false;
    }
}

function draw_message(data) {
    // Gets the div container
    const container = document.getElementById('container');
    // Deletes the inner content
    container.innerHTML = ``;

    // If there is an error in the response shows this
    if (data.Status !== 'Products calculation successfully.') {
        // Creates a div
        const warning = document.createElement('div');
        // Adds the class name
        warning.className = 'bg-amber-100';
        // Adds the html needed
        warning.innerHTML = `
        <div class="bg-amber-100">
            <p class="text-5xl">${data.Status}</p>
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
        // successfull.innerHTML = `
        // <div class="bg-blue-500">
        //     <p class="text-5xl">Carbon footprint finished, congratulations!!</p>
        //     <button class="bg-amber-300 cursor-pointer">
        //         <a href="/carbonfp">Finish</a>
        //     </button>
        // </div>
        // `;

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

