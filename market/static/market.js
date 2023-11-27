

document.addEventListener('DOMContentLoaded', function() {
    // Select elements
    const selectCrop = document.getElementById('selectCrop');
    const selectState = document.getElementById('selectState');
    const selectMarket = document.getElementById('selectMarket');
    const searchButton = document.getElementById('searchButton');
    const resultContainer = document.getElementById('resultContainer');
    const resultContainer2 = document.getElementById('resultContainer2');
    const cropImage = document.getElementById('cropImage'); // Get the img element



    // Function to populate a select element with options
    function populateSelect(selectElement, options) {
        selectElement.innerHTML = ''; // Clear existing options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.textContent = option;
            selectElement.appendChild(optionElement);
        });
    }

    // Function to read JSON data and populate selects
    function populateSelectsFromJSON() {
        fetch('data/completedict.json') // Replace with the correct JSON file path
            .then(response => response.json())
            .then(data => {
                // Populate the Crop select with data keys
                const crops = Object.keys(data);
                populateSelect(selectCrop, crops);

                // Event listener for Crop select
                selectCrop.addEventListener('change', function() {
                    const selectedCrop = this.value;
                    if (selectedCrop in data) {
                        const states = Object.keys(data[selectedCrop]);
                        populateSelect(selectState, states);
                    } else {
                        selectState.innerHTML = '<option value="">--Select State--</option>';
                        selectMarket.innerHTML = '<option value="">--Select Market--</option>';
                    }
                });

                // Event listener for State select
                selectState.addEventListener('change', function() {
                    const selectedCrop = selectCrop.value;
                    const selectedState = this.value;
                    if (selectedCrop in data && selectedState in data[selectedCrop]) {
                        const markets = data[selectedCrop][selectedState];
                        populateSelect(selectMarket, markets);
                    } else {
                        selectMarket.innerHTML = '<option value="">--Select Market--</option>';
                    }
                });
                searchButton.addEventListener('click', function() {

                });
            })
            .catch(error => console.error(error));
    }

    // Populate the selects when the page loads
    populateSelectsFromJSON();

    // Function to update table values
    function updateTableValues(data) {
    document.getElementById('avgPrice').textContent = data['Avg Price:'];
    document.getElementById('costliestPrice').textContent = data['Costliest Market Price:'];
    document.getElementById('cheapestPrice').textContent = data['Cheapest Market Price:'];
    document.getElementById('latestDate').textContent = data['Latest Price Date:'];
}
function updateTable2Values(data) {
    document.getElementById('Commodity2').textContent = data['Commodity:'];
    document.getElementById('MarketDetails2').textContent = data['Market Details:'];
    document.getElementById('avgPrice2').textContent = data['Avg Price:'];
    document.getElementById('cheapestPrice2').textContent = data['Cheapest Market Price:'];
    document.getElementById('costliestPrice2').textContent = data['Costliest Market Price:'];
    document.getElementById('Varieties2').textContent = data['Varieties:'];
    document.getElementById('Knownas2').textContent = data['Known as:'];
}

function updateTable3Values(data) {
    const table3Body = document.getElementById('table3Body');

    // Clear existing rows
    table3Body.innerHTML = '';

    // Iterate through the data and create new rows
    data.forEach(rowData => {
        const row = document.createElement('tr');

        // Iterate through each column in the row
        for (const key in rowData) {
            const cell = document.createElement('td');
            cell.textContent = rowData[key];
            row.appendChild(cell);
        }

        // Append the new row to the table body
        table3Body.appendChild(row);
    });
}

// Function to populate cards
function populateCards(data) {
    const cardContainer = document.getElementById('table3cardBody');
    cardContainer.innerHTML = ''; // Clear existing cards


    // Iterate through the data and create a card for each entry
    data.forEach(entry => {
        const card = document.createElement('div');
        card.classList.add('card');

        // Create card title with Arrival Date
        const cardTitle = document.createElement('div');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = `Arrival Date: ${entry["Arrival Date"]}`;

        card.appendChild(cardTitle);

        // Create a table within the card
        const table = document.createElement('table');
        table.classList.add('card-table');

        // Iterate through the properties of each entry (excluding Arrival Date) and create table rows
        for (const property in entry) {
            if (property !== "Arrival Date") {
                const row = document.createElement('tr');

                const labelCell = document.createElement('td');
                labelCell.textContent = property;

                const valueCell = document.createElement('td');
                valueCell.textContent = entry[property];

                row.appendChild(labelCell);
                row.appendChild(valueCell);
                table.appendChild(row);
            }
        }

        card.appendChild(table);
        cardContainer.appendChild(card);
    });
}
    function changeCropImage(selectedCrop) {
        // Assuming your image files are named the same as the crop
        const imageName = selectedCrop; // Convert to lowercase
        const imageFormats = ['jpg', 'jpeg', 'png', 'gif', 'bmp']; // List of supported image formats

        const loadImage = function (formatIndex) {
        if (formatIndex < imageFormats.length) {
            const format = imageFormats[formatIndex];
            const imagePath = `static/images/cropimage/${imageName}.${format}`;

            // Check if the image exists
            const img = new Image();
            img.src = imagePath;
            img.onload = function () {
                // Image found and loaded
                cropImage.src = imagePath; // Set the image source to the selected image
                cropImage.style.width = '200px'; // Set the width to your desired value
                cropImage.style.height = '200px';
            };

            img.onerror = function () {
                // Image not found in this format, try the next format
                loadImage(formatIndex + 1);
            };
        } else {
            cropImage.style.width = '100px'; // Set the width to your desired value
            cropImage.style.height = '100px';
            // No image found in supported formats, display a default image
            cropImage.src = 'static/images/cropimage/logo.png'; // Update to your default image path
        }
    };

    // Start loading images in supported formats
    loadImage(0);

    }
    // function to update table 1 left column
// Declare the priceChart variable
let priceChart;

function updatePriceChart(data) {
    const labels = data.map(entry => entry['Arrival Date']);
    const minPrices = data.map(entry => parseFloat(entry['Min Price']));
    const maxPrices = data.map(entry => parseFloat(entry['Max Price']));
    const modalPrices = data.map(entry => parseFloat(entry['Modal Price']));

    const ctx = document.getElementById('priceChart').getContext('2d');

    if (priceChart) {
        priceChart.destroy();
    }

    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Min Price',
                    data: minPrices,
                    borderColor: 'rgba(255, 0, 0, 1)',
                    borderWidth: 4,
                    fill: false,
                            tension: 0.4 // Adjust the tension value as needed

                },
                {
                    label: 'Max Price',
                    data: maxPrices,
                    borderColor: 'rgba(0, 255, 0, 1)',
                    borderWidth: 4,
                    fill: false,
                            tension: 0.4 // Adjust the tension value as needed

                },
                {
                    label: 'Modal Price',
                    data: modalPrices,
                    borderColor: 'rgba(0, 0, 255, 1)',
                    borderWidth:4,
                    fill: false,
                            tension: 0.4 // Adjust the tension value as needed

                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'category',
                    position: 'bottom',
                    barPercentage: 1, // Adjust the bar width
                     ticks: {
                    fontsize: 200 // Adjust the font size as needed
                }


                },
                y: {
                    beginAtZero: true,
                     ticks: {

                    fontsize: 20 // Adjust the font size as needed
                }

                }
            }
        }
    });
}


function customURIEncode(value) {
    return value.replace('/','-');
}
    function handleSearchButtonClick() {
        const selectedCrop = customURIEncode(selectCrop.value);
        const selectedMarket = customURIEncode(selectMarket.value);
        const selectedState = selectState.value;
        console.log(selectedCrop)



                    if (selectedCrop === "--Select Commodity🌾--" ){
                    alert("Please select Crop,State,Market");
                    }
                    else if (selectedState === "--Select State--") {
                     alert("Please select State,Market");
                    }else if (selectedMarket === "Select market") {
                        alert("Please select Market");
                    } else {
                        const resultText = `${selectedCrop} Price Summary in ${selectedMarket} Market`;
                        const resultText2 = `${selectedCrop} Market Rates  in ${selectedMarket} Market`;

                        resultContainer.querySelector("h3").textContent = resultText;
                        resultContainer2.querySelector("h3").textContent = resultText2;

                        var spinnerOverlay = document.getElementById("spinnerOverlay");
                        var resultSection = document.getElementById("resultContainer");
                        var resultSection2 = document.getElementById("resultContainer2");

                        spinnerOverlay.style.display = "block";

                        resultSection.style.display = "none";
                        resultSection2.style.display = "none";
                        // Set a timeout to hide the spinner and show the results after 3 seconds
                        setTimeout(function () {
                            spinnerOverlay.style.display = "none";
                            resultSection.style.display = "block";
                            resultSection2.style.display = "block";
                           }, 3000);


        const loadingSpinner = document.getElementById('loadingSpinner');
        const loadingSpinner2 = document.getElementById('loadingSpinner2');

        loadingSpinner.style.display = 'block';
        changeCropImage(selectedCrop);

           fetch('http://127.0.0.1:5000/get_prices/' + selectedCrop + '/' + selectedMarket)
            .then(response => response.json())
            .then(dat => {
                 console.log(dat);  // Log the received data to the console

                // Update the table values with the fetched data
                updateTableValues(dat.table1);

                // Update the crop image and name as you've done before
                 loadingSpinner.style.display = 'none';
                 updateTable2Values(dat.table2)
                 loadingSpinner2.style.display = 'none';
                 updateTable3Values(dat.table3)
                 populateCards(dat.table3)
                 updatePriceChart(dat.table3)

                 costli_price = dat.table1['Costliest Market Price:'];
                 mini_price=dat.table1['Cheapest Market Price:'];
                 const resultText3 = `Get the latest and updated prices of  ${selectedCrop}  in ${selectedMarket} located  in the state  ${selectedState}.As per the current market rates,maximum price of ${selectedCrop} is ${costli_price} whereas the minimum rate is ${mini_price} . `;
                 resultContainer2.querySelector("h6").textContent = resultText3;


            })
            .catch(error => console.error(error));

}
    }
    function isValidSelection(selectedCrop, selectedState, selectedMarket) {
    if (
        selectedCrop === "--Select Commodity🌾--" ||
        selectedState === "--Select State--" ||
        selectedMarket === "Select market"
    ) {
        alert("Please select Crop, State, and Market");
        return false;
    }
    return true;
}

   searchButton.addEventListener('click', handleSearchButtonClick);
});
