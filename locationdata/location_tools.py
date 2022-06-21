import requests
from django.conf import settings
from geopy import distance

from locationdata.models import Location


def fetch_coordinates(address):
    base_url = 'https://geocode-maps.yandex.ru/1.x'
    response = requests.get(base_url, params={
        'geocode': address,
        'apikey': settings.YANDEX_GEOCODER_API,
        'format': 'json',
    })
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(' ')
    return lat, lon


def get_distance(order, locations):
    order_coordinates = locations.get(order.address)
    for restaurant in order.restaurant_with_product:
        restaurant_coordinates = locations.get(restaurant.address)
        restaurant.distance_for_order = round(distance.distance(
            order_coordinates, restaurant_coordinates).km, 3)
    return order


def get_locations(*addresses):
    locations = {
        location.address: (location.lat, location.lon)
        for location in Location.objects.filter(address__in=addresses)
    }
    new_locations = list()
    for address in addresses:
        if address in locations.keys():
            continue
        coordinates = fetch_coordinates(address)
        if coordinates:
            lat, lon = coordinates
            location = Location(
                address=address,
                lat=lat,
                lon=lon,
            )
            locations[location.address] = (location.lat, location.lon,)
            new_locations.append(location)
    Location.objects.bulk_create(new_locations)
    return locations
