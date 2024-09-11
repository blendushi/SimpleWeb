//define an asynchronous function to calculate the delivery fee
async function calculateDeliveryFee() {
    
    //extract input values from the HTML elements
    const cartValueEuros: number = parseFloat((<HTMLInputElement>document.getElementById('cartValue')).value);
    const deliveryDistance: number = parseInt((<HTMLInputElement>document.getElementById('deliveryDistance')).value);
    const numberOfItems: number = parseInt((<HTMLInputElement>document.getElementById('numberOfItems')).value);
    const orderTime: string = (<HTMLInputElement>document.getElementById('orderTime')).value;
    

    //input values for debugging purposes
    console.log('Sending request...', cartValueEuros, deliveryDistance, numberOfItems, orderTime);

    try {
        //send a post request to the backend API
        const response = await fetch('http://localhost:5500/calculate_delivery_fee', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ // Converting data to JSON string for backend processing
                cart_value: Math.round(cartValueEuros * 100),  // Convert euros to cents for backend processing
                delivery_distance: deliveryDistance,
                number_of_items: numberOfItems,
                time: orderTime,
            }),
        });
        //the response for debugging purposes
        console.log('Response received:', response);

        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        // Parse the JSON data from the response
        const data = await response.json();
        console.log('Data received:', data);

        // Display the calculated delivery fee in the HTML result element
        const resultElement: HTMLElement | null = document.getElementById('result');
        if (resultElement !== null) {
            resultElement.innerHTML = `<p>Delivery Fee: ${data.delivery_fee} €</p>`;
        }
    } catch (error) {
        // Handle errors and display an error message in the HTML result element
        console.error('Error calculating delivery fee:', error);
        const resultElement: HTMLElement | null = document.getElementById('result');
        if (resultElement !== null) {
            resultElement.innerHTML = '<p>Error calculating delivery fee</p>';
        }
    }
}