from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

def calculate_delivery_fee(cart_value: float,
                           delivery_distance: int,
                           number_of_items: int,
                           order_time: datetime):
    
    delivery_fee = 0

    #calculating the surcharge depending on the cart_value
    surcharge_cart_value = max(0, 1000 - cart_value)
    delivery_fee += surcharge_cart_value

    #fee for the first 1000m
    delivery_fee += 200 

    #additional fee 1€ for every 500m that goes beyound the first km
    additional_distance = max(0, delivery_distance - 1000)
    delivery_fee += ((additional_distance +499) // 500) * 100

    #additional fee for 5 or more items
    if number_of_items >= 5:
        item_surcharge = 50 * (number_of_items - 4)
        delivery_fee += item_surcharge

    #additional fee for more than 12 items 
    if number_of_items > 12:
        bulk = 120
        delivery_fee += bulk

    #rush hour multiplayer on fridays from 3 PM to 7 PM UTC
    if 15 <= order_time.hour <= 19 and order_time.weekday() == 4:
        delivery_fee *= 1.2 

    #delivery fee 0€ if cart value equal/more than 200
    if cart_value >= 20000:
        delivery_fee = 0

    delivery_fee = min(delivery_fee, 1500)  # Delivery fee cannot be more than 15€

    return round(delivery_fee / 100, 4)  # Convert to euros 

#defining a route for the calculate_delivery_fee end
@app.route('/calculate_delivery_fee', methods=['POST'])
def calculate_delivery_fee_end():
    try:
        #parse the JSON data from the request
        data = request.get_json()

        #get the relevant information
        cart_value = float(data.get('cart_value'))
        delivery_distance = int(data.get('delivery_distance'))
        number_of_items = int(data.get('number_of_items'))
        order_time = datetime.fromisoformat(data.get('time'))

        #calling the calculating function
        delivery_fee = calculate_delivery_fee(cart_value, delivery_distance, number_of_items, order_time)
        
        #return the calculated delivery fee in the response
        return jsonify({'delivery_fee': delivery_fee})
    except Exception as e:
        # Handle exceptions and return an error response with status code 500
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)