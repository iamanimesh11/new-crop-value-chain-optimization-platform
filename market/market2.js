        const selectCrop = document.getElementById("selectCrop");
        const selectState = document.getElementById("selectState");
        const selectMarket = document.getElementById("selectMarket");

        // Function to populate options from JSON file
        async function populateSelectFromJSON(file, selectElement) {
            try {
                const response = await fetch(file);
                const data = await response.json();

                // Populate the select element with options
                for (const key in data) {
                    const option = document.createElement("option");
                    option.value = key;
                    option.textContent = key;
                    selectElement.appendChild(option);
                }
            } catch (error) {
                console.error(error);
            }
        }

        // Populate the "Select Crop" dropdown from the JSON file
        populateSelectFromJSON('data/completedict.json', selectCrop);

        // Event listener for "Select Crop" change
        selectCrop.addEventListener("change", () => {
            const selectedCrop = selectCrop.value;
            const stateOptions = data[selectedCrop];

            // Clear existing state and market options
            selectState.innerHTML = "<option value=''>--Select State--</option>";
            selectMarket.innerHTML = "<option value=''>--Select Market--</option>";

            if (stateOptions) {
                // Populate state options
                for (const state in stateOptions) {
                    const option = document.createElement("option");
                    option.value = state;
                    option.textContent = state;
                    selectState.appendChild(option);
                }
            }
        });

        // Event listener for "Select State" change
        selectState.addEventListener("change", () => {
            const selectedCrop = selectCrop.value;
            const selectedState = selectState.value;
            const marketOptions = data[selectedCrop][selectedState];

            // Clear existing market options
            selectMarket.innerHTML = "<option value=''>--Select Market--</option>";

            if (marketOptions) {
                // Populate market options
                for (const market of marketOptions) {
                    const option = document.createElement("option");
                    option.value = market;
                    option.textContent = market;
                    selectMarket.appendChild(option);
                }
            }
        });