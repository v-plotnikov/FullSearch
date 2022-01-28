from io import BytesIO

import requests


def check_response(resp):
    if not resp:
        verd = f"Ошибка выполнения запроса:\n{resp.url}\nСтатус: {resp.status_code} {resp.reason}"
        raise Exception(verd)


def correct_scale_value(bounded_by):
    lon1, lat1 = map(float, bounded_by["upperCorner"].split())
    lon2, lat2 = map(float, bounded_by["lowerCorner"].split())
    return f"{abs(lon1 - lon2)},{abs(lat1 - lat2)}"


def get_points(*places):
    return map(get_description, places)


def get_description(place: str):
    description = f"{get_place_info(place)['coords']}"
    return description


def get_place_info(place: str):
    geocode_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
              "geocode": f"{place}",
              "format": "json"}
    response = requests.get(geocode_url, params)
    check_response(response)
    r = response.json()
    toponym = r["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    ll = toponym["Point"]["pos"]
    bounded_by = toponym["boundedBy"]["Envelope"]

    return {"coords": ll.replace(" ", ","), "bounded_by": bounded_by}


def get_image(info: dict, points=None):
    if points is None:
        points = []
    static_map_url = "http://static-maps.yandex.ru/1.x/"
    params = {"ll": info["coords"],
              "spn": correct_scale_value(info["bounded_by"]),
              "pt": "~".join(points),
              "l": "map"}

    response = requests.get(static_map_url, params)
    check_response(response)
    return BytesIO(response.content)
