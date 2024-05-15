from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    reviewsurl = "https://worldwide-restaurants.p.rapidapi.com/reviews"
    typeaheadurl = "https://worldwide-restaurants.p.rapidapi.com/typeahead"
    detailurl = "https://worldwide-restaurants.p.rapidapi.com/detail"
    photosurl = "https://worldwide-restaurants.p.rapidapi.com/photos"


    payload = {
        "location_id": "15333482",
        "language": "en_US",
        "currency": "USD",
        "offset": "0"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "c4bd859a3dmsh2ceb7a3e8bce312p132d4bjsn84c9a41b058a",
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    photos_response = requests.post(photosurl, data=payload, headers=headers)

    if photos_response.status_code == 200:
        photos_data = photos_response.json().get('results', {}).get('data', [])
        print("Photos Data:")
        for photo in photos_data:
            print(photo.get('images'))  # Example: Print the name of each photo
    else:
        print(f"Error: {photos_response.status_code} - {photos_response.reason}")

    detail_response = requests.post(detailurl, data=payload, headers=headers)

    if detail_response.status_code == 200:
        detail_data = detail_response.json().get('results', {}).get('data', [])
        print("\nDetail Data:")
        for item in detail_data:
            print(item.get('name'))  # Example: Print the name of each restaurant/hotel
    else:
        print(f"Error: {detail_response.status_code} - {detail_response.reason}")

    return render_template('hotels.html', detail_data=detail_data, photos_data=photos_data)

if __name__ == "__main__":
    app.run(debug=True, port=8001)

