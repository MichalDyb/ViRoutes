from django import template
from django.utils import timezone
import datetime
import re

register = template.Library()

@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)

@register.simple_tag
def time_add(days):
    now = timezone.now()
    next = now
    try:
        next = now + datetime.timedelta(days=days)
    except:
        return now
    return next

@register.filter(name='dict_key')
def dict_key(d, k):
    return d[k]

@register.filter(name='translate_conditions')
def translate_conditions(conditions):
    conditions = conditions
    conditions = re.sub('Blowing Or Drifting Snow', 'Zamieć śnieżna', conditions)
    conditions = re.sub('Heavy Drizzle', 'Silna mżawka', conditions)
    conditions = re.sub('Light Drizzle', 'Lekka mżawka', conditions)
    conditions = re.sub('Heavy Drizzle/Rain', 'Silna mżawka/deszcz', conditions)
    conditions = re.sub('Light Drizzle/Rain', 'Lekka mżawka/deszcz', conditions)
    conditions = re.sub('Freezing Drizzle/Freezing Rain', 'Zamarzająca mżawka/zamarzający deszcz', conditions)
    conditions = re.sub('Heavy Freezing Drizzle/Freezing Rain', 'Silna zamarzająca mżawka/zamarzający deszcz', conditions)
    conditions = re.sub('Light Freezing Drizzle/Freezing Rain', 'Lekka zamarzająca mżawka/zamarzający deszcz', conditions)
    conditions = re.sub('Freezing Fog', 'Marznąca mgła', conditions)
    conditions = re.sub('Hail Showers', 'Gradobicie', conditions)
    conditions = re.sub('Heavy Freezing Rain', 'Silny zamarzający deszcz', conditions)
    conditions = re.sub('Light Freezing Rain', 'Lekki zamarzający deszcz', conditions)
    conditions = re.sub('Heavy Snow', 'Duże opady sniegu', conditions)
    conditions = re.sub('Light Snow', 'Lekkie opady śniegu', conditions)
    conditions = re.sub('Snow Showers', 'Opady śniegu', conditions)
    conditions = re.sub('Snow And Rain Showers', 'Opady śniegu z deszczem', conditions)
    conditions = re.sub('Rain Showers', 'Oberwanie chmury', conditions)
    conditions = re.sub('Thunderstorm Without Precipitation', 'Burza z lub bez opadów', conditions)
    conditions = re.sub('Precipitation In Vicinity', 'Opady atmosferyczne', conditions)
    conditions = re.sub('Heavy Rain And Snow', 'Silny opady śniegu z deszczem', conditions)
    conditions = re.sub('Light Rain And Snow', 'Lekkie opady śniegu z deszczem', conditions)
    conditions = re.sub('Funnel Cloud/Tornado', 'Lej kondensacyjny/Tornado', conditions)
    conditions = re.sub('Sky Coverage Decreasing', 'Malejące zachmurzenie', conditions)
    conditions = re.sub('Sky Coverage Increasing', 'Rosnące zachmurzenie', conditions)
    conditions = re.sub('Sky Unchanged', 'Bezzmienne zachmurzenie', conditions)
    conditions = re.sub('Smoke Or Haze', 'Zadymienie lub zamglenie', conditions)
    conditions = re.sub('Lightning Without Thunder', 'Burza bezpiorunowa', conditions)
    conditions = re.sub('Heavy Rain', 'Silny deszcz', conditions)
    conditions = re.sub('Light Rain', 'Słaby deszcz', conditions)
    conditions = re.sub('Mist', 'Mgiełka', conditions)
    conditions = re.sub('Ice', 'Lód', conditions)
    conditions = re.sub('Thunderstorm', 'Burza z piorunami', conditions)
    conditions = re.sub('Squalls', 'Szkwał', conditions)
    conditions = re.sub('Diamond Dust', 'Diamentowy pył(słupki lodowe)', conditions)
    conditions = re.sub('Hail', 'Grad', conditions)
    conditions = re.sub('Snow', 'Opady śniegu', conditions)
    conditions = re.sub('Drizzle', 'Mżawka', conditions)
    conditions = re.sub('Rain', 'Deszcz', conditions)
    conditions = re.sub('Duststorm', 'Burza piaskowa', conditions)
    conditions = re.sub('Fog', 'Mgła', conditions)
    conditions = re.sub('Overcast', 'Pochmurnie', conditions)
    conditions = re.sub('Partially cloudy', 'Częściowe zachmurzenie', conditions)
    conditions = re.sub('Clear', 'Pogodnie', conditions)
    return conditions
