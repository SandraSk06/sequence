async function showListFromDate() {

    const start_date_value = document.querySelector('.js-input-start-date').value;
    const end_date_value = document.querySelector('.js-input-end-date').value;

    try {
        // Send POST request with parameters
        const response = await fetch('http://localhost:8000/shipping/get-data-by-date', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ start_date: start_date_value, end_date: end_date_value })
        });

        // Check if the response is successful
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const data = await response.json();

        // Check if data exists
        if (data.length === 0) {
            console.log("No data found for the given date range.");
            showMessage("No data found for the given date range.");
            return;
        }

        // Display the result
        const tableBody = document.querySelector('#js-show-result tbody');

         // Clear the table body before adding new data
        tableBody.innerHTML = '';

        const initialSequenceElement = document.getElementById("sequence-diagram-container").innerHTML;

        // Iterate through each item in the JSON data
        data.forEach(item => {
            const row = document.createElement('tr'); // Create a new row

            // Selected fields
            const selectedFields = ['OrderID', 'Carrier', 'ShippingOrigin', 'OrderDate', 'OnTimeDelivery'];

            // Loop through the selected fields and append their values to the row
            selectedFields.forEach(field => {
                const cell = document.createElement('td');
                cell.textContent = item[field];
                row.appendChild(cell);
            });

            // Append the row to the table body
            tableBody.appendChild(row);

            row.addEventListener("click", ()=> {
                const popupContent = document.getElementById("sequence-diagram-container");

                popupContent.innerHTML = initialSequenceElement;
                document.getElementById("overlay").style.display = "flex";

                loadSequenceDiagram(popupContent, item);

                // document.getElementById("overlay").innerHTML='<object type="text/html" data="templates/popup.html" ></object>';
                // alert(`Order Id: ${item.OrderID}\n Shipping Origin: ${item.ShippingOrigin}`);
            });
        });


    } catch (error) {
        console.log('Error:', error);
        showMessage("Failed to load data.");
    }

}

function closePopup() {
    // Close popup functionality
    document.getElementById("overlay").style.display = "none";  // Hide the overlay
}

function showMessage(message) {
    const tableBody = document.querySelector('#js-show-result tbody');
    if (tableBody) {
        tableBody.innerHTML = `<tr><td colspan="5">${message}</td></tr>`;
    }
}

// Connect with MQTT
async function connectWithMqtt() {
    const response = await fetch('http://localhost:8000/shipping/mqtt-subscribe');
    // Check if the response is successful
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    // Parse the JSON response
    const data = await response.json();
    console.log("Data: ${data}")
}

// Receive messages from MQTT
async function getMessages() {

    const response = await fetch('http://localhost:8000/shipping/messages');
    // Check if the response is successful
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    // Parse the JSON response
    const data = await response.json();
    // Check if data exists
    if (data.length === 0) {
        console.log("No data found for the given date range.");
        showMessage("No data found for the given date range.");
        return;
    }

    // Display the result
    const tableBody = document.querySelector('#js-show-result tbody');

    // Clear the table body before adding new data
    tableBody.innerHTML = '';

     // Iterate through each item in the JSON data
     data.forEach(item => {
        const row = document.createElement('tr'); // Create a new row

        // Selected fields
        const selectedFields = ['id', 'msg'];

        // Loop through the selected fields and append their values to the row
        selectedFields.forEach(field => {
            const cell = document.createElement('td');
            cell.textContent = item[field];
            row.appendChild(cell);
        });

        // Append the row to the table body
        tableBody.appendChild(row);
     });
}


function loadSequenceDiagram(popupContent, item) {
    const diagramDesc = `${item.ShippingOrigin}->${item.OnTimeDelivery}: ${item.ActualShippingDays} days
    `;
    document.getElementById("loading").style.display = 'block';

    const myDiagram = Diagram.parse(diagramDesc);
    myDiagram.drawSVG(popupContent, { theme: 'simple' });

    setTimeout(()=> {

    document.getElementById("loading").style.display = 'none';
    }, 1000);
}