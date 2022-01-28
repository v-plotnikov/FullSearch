from io import BytesIO

import requests


def check_response(resp):
    if not resp:
        verd = f"Ошибка выполнения запроса:\n{resp.url}\nСтатус: {resp.status_code} {resp.reason}"
        raise Exception(verd)


def correct_scale_value(kind):
    if kind == "house" or kind == "metro":
        return "0.005,0.005"
    if kind == "street":
        return "0.007, 0.007"
    if kind == "district":
        return "0.01, 0.01"
    if kind == "locality":
        return "0.05, 0.05"


def get_points(*places):
    return map(get_description, places)


def get_description(place: str):
    description = f"{get_place_info(place)}"
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
    kind = toponym["metaDataProperty"]["GeocoderMetaData"]["kind"]

    return {"coords": ll.replace(" ", ","), "kind": kind}


def get_image(info: dict, points=None):
    if points is None:
        points = []
    static_map_url = "http://static-maps.yandex.ru/1.x/"
    params = {"ll": info["coords"],
              "spn": correct_scale_value(info["kind"]),
              "pt": "~".join(points),
              "l": "map"}

    response = requests.get(static_map_url, params)
    check_response(response)
    return BytesIO(response.content)
