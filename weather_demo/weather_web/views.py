from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def get_weather_comment(temperature, unit):
    # Comments change based on weather
    if unit == 'metric':
        if temperature < 0:
            return "Brr! Better bundle up!"
        elif 0 <= temperature < 15:
            return "A bit chilly, do not forget your coat!"
        elif 15 <= temperature < 25:
            return "Perfect weather for a stroll!"
        elif 25 <= temperature < 35:
            return "Getting warm! Stay hydrated!"
        else:
            return "It's a scorcher! Find some shade!"
    else:  # Fahrenheit
        if temperature < 32:
            return "Brr! Better bundle up!"
        elif 32 <= temperature < 59:
            return "A bit chilly, do not forget your coat!"
        elif 59 <= temperature < 77:
            return "Perfect weather for a stroll!"
        elif 77 <= temperature < 95:
            return "Getting warm! Stay hydrated!"
        else:
            return "It's a scorcher! Find some shade!"

def index(request):
    url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    api_key = '<USE YOUR API_KEY>'
    err_msg = ''
    message = ''
    message_class = ''
    

    temperature_unit = request.POST.get('temperature_unit', 'metric')

    if request.method == 'POST':
        # Check if a new city is being added
        if 'name' in request.POST:  
            form = CityForm(request.POST)
            if form.is_valid():
                new_city = form.cleaned_data['name']
                existing_city_count = City.objects.filter(name=new_city).count()
                if existing_city_count == 0:
                    r = requests.get(url.format(new_city, api_key)).json()
                    if r['cod'] == 200:
                        form.save()
                        message = 'City added Successfully!'
                        message_class = 'is-success'
                    else:
                        err_msg = 'City does not exist!'
                else:
                    err_msg = 'City already exists!'
            
            if err_msg:
                message = err_msg
                message_class = 'is-danger'
        else:
            # Handle temperature unit change
            message = 'Temperature unit changed successfully!'
            message_class = 'is-success'
    
    form = CityForm()
    cities = City.objects.all()
    weather_data = []
    
    for city in cities:
        r = requests.get(url.format(city, api_key)).json()
        temperature = round(r['main']['temp'] - 273.15) if temperature_unit == 'metric' else round((r['main']['temp'] - 273.15) * 9/5 + 32)  # Convert to Fahrenheit
        comment = get_weather_comment(temperature, temperature_unit)
        city_weather = {
            'city': city.name,
            'temperature': temperature,
            'comment': comment,
            'icon': r['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data, 
        'form': form,
        'message': message,
        'message_class': message_class,
        'temperature_unit': temperature_unit
    }
    return render(request, 'weather_web/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
