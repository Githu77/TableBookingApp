import requests

reviewsurl = "https://sky-scrapper.p.rapidapi.com/api/v1/hotels/getHotelReviews"

p
querystring = {"hotelId":"106005202","currency":"USD","market":"en-US","countryCode":"US"}

headers = {
	"X-RapidAPI-Key": "c4bd859a3dmsh2ceb7a3e8bce312p132d4bjsn84c9a41b058a",
	"X-RapidAPI-Host": "sky-scrapper.p.rapidapi.com"
}

review = requests.get(reviewsurl, headers=headers, params=querystring)

print(review.json())

if review.status_code == 200:
    api_data = review.json()  # Convert the content to a dictionary
    print(api_data['results']['data'][0])

else:
    print(f"Error: {review.status_code} - {review.reason}")
