import pyowm
import twitter
import datetime

# Function to parse a OWM Weather/Location object and create an update tweet
def createWeatherTweet(bulk):
    # Get the weather and location objects from OWM object (minimal calls to API)
    weather = bulk.get_weather()
    location = bulk.get_location()

    # Get the location string
    city = location.get_name()
    country = location.get_country()
    loc_str = str(city) + ", " + str(country)

    # Get the current time
    currentDT = datetime.datetime.now()
    date_str = currentDT.strftime("%a, %b %d, %Y") + " at " + currentDT.strftime("%I:%M:%S %p")

    # Get the different properties of the weather object and format the tweet
    head_str = "Here is a weather update for " + loc_str + " on " + date_str  + ":\n"
    temp_str = "Temperature: " + str(weather.get_temperature(unit='fahrenheit')['temp_max']) + " degrees Fahrenheit\n"
    status_str = "Status: " + weather.get_status().lower() + "\n"
    humid_str = "Humidity: " + str(weather.get_humidity()) + "%\n"
    wind_str = "Wind: " + str(weather.get_wind()['speed']) + " mph\n"
    tail_str = "Stay tuned for more updates. #WeatherGuyUpdates #WeatherGuyIn" + city

    # Return the tweet
    king_str = head_str + temp_str + humid_str + wind_str + status_str + tail_str

    # Make sure the tweet is tweetable
    return king_str[:280]

def main():
    # Define keys necessary for apis (left out for privacy)
    TWITTER_CONSUMER_KEY = ""
    TWITTER_CONSUMER_SECRET_KEY = ""
    TWITTER_ACCESS_TOKEN = ""
    TWITTER_ACCESS_TOKEN_SECRET = ""
    OWM_KEY = ""

    # Get the OWM object
    owm = pyowm.OWM(OWM_KEY)

    # Get the ID for Yerevan, Armenia (Obtained via a registry lookup)
    city_id = 616051

    # Get the weather and location objects from the API and parse it to make a tweet
    bulk = owm.weather_at_id(city_id)
    tweet = createWeatherTweet(bulk)

    # Authenticate to Twitter
    my_auth = twitter.OAuth(TWITTER_ACCESS_TOKEN,TWITTER_ACCESS_TOKEN_SECRET,TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET_KEY)
    twit = twitter.Twitter(auth=my_auth)

    # Send the tweet
    print("Sending tweet...")
    twit.statuses.update(status=tweet)
    print("Tweet sent.")

if __name__ == '__main__':
    main()
