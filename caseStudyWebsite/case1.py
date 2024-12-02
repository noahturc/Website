print('\n\n\n')
import pandas as pd
bikes = pd.read_csv(r"c:\Noah\gitProjects\publicNoahRepo\caseStudyWebsite\caseStudyPhotosAndData\case1\archive (3)\london_merged.csv")

#bikes.info()
#print(bikes.shape)
#print(bikes)
# count the unique values in the specified column
#print(bikes.weather_code.value_counts())
#print(bikes.weather.value_counts())

bikes.columns = ["time", "count", "realTemp", "feelsLikeTemp", "humidityPercent", "windSpeedKPH", "weather", "isHoliday", "isWeekend", "season"]

# mapping the floats to the actual values
seasons = {'0.0': 'spring', '1.0': 'summer', '2.0': 'fall', '3.0': 'winter'}
weathers = {
    '1.0': 'clear', '2.0': 'scattered clouds', '3.0': 'broken clouds', '4.0': 'cloudy',
    '7.0': 'rain', '10.0': 'rain with thunderstorm', '26.0': 'snowfall', '94.0': 'freezing fog'
    }

bikes.season = bikes.season.astype('str')
bikes.weather = bikes.weather.astype('str')
bikes.season = bikes.season.map(seasons)
bikes.weather = bikes.weather.map(weathers)



#print(bikes.head())
#print(bikes.weather.value_counts())
#print((bikes['weather'] == 94.0).sum())

bikes.to_excel('london_bikes_final.xlsx', sheet_name='Data')