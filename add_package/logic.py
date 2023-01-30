import json

import requests

global token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9" \
        ".eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMzgzMjM2LCJqdGkiOiIwNTE4ZjRjMTM2ODg0ZmE2OTk5MzA2NDA5NWM4Mjg3MyIsInVzZXJfaWQiOjF9.teBtp0kiVPx_tpOxzuS3TxgGfWyMU3ppeMX2YLGIAo4"

global headers
headers = {'Authorization': 'Bearer ' + token}


def package_ok_for_add(package_code: str, route_id: str):
    url = "https://release--api.clicoh.com/api/v1/pickup_points/packages/?order_by=-id&section=list_packages&search={}" \
        .format(package_code)

    response = requests.get(url, headers=headers).json()

    if response["count"] == 0 and response["results"][0]["code"] != package_code and response["results"][0]["reference_code"] != package_code:
        print("Package {} not found".format(package_code))
        return False, None

    package_code = response["results"][0]["code"]
    package_id = response["results"][0]["id"]

    ok_states = [
        'traveling_mid_mile',
        'on_lookup_batch',
        '1st_mile',
        'ready',
        'at_destination',
        'dispatched',
        'last_mile'
    ]
    package_state = response["results"][0]["current_state"]["state"]["name"]

    if package_state not in ok_states:
        print("Package {} with a invalid state".format(package_code))
        return False, None

    return True, package_code, package_state, route_id, package_id


def route_ok_for_add(route_id: str):
    url = "https://release--api.clicoh.com/api/v1/driver/routes/{}/".format(route_id)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error with route {}".format(route_id))
        return False, route_id, None, None

    response_dic = response.json()

    if response_dic["route_type"] != "last_mile":
        print("Invalid type route : {}".format(response_dic["route_type"]))
        return False, route_id, None, None

    ok_states = ["traveling"]
    route_state = response_dic["current_state"]["state"]["name"]

    if route_state not in ok_states:
        print("Invalid route state {}".format(route_state))
        return False, route_id, None, None

    stop_number = response_dic["progress"]["total"]

    return True, route_id, route_state, stop_number


def change_state(data, state: str):
    url = "https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/"

    payload = json.dumps(
        {
            "packages": data,
            "reference": state,
            "action": "change_state"
        }
    )
    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwNDAxMDc2LCJqdGkiOiJiZDZhMzYwN2QzNDI0YWMzYjZjODQwMzA3NmQ1MmUwZCIsInVzZXJfaWQiOjF9.K_u9S_gaVWnpWsW7R3GsLkPxfTjrvc-l-DUY7BAvrUk',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=kFFFgScSe4jpIrPPYMVoqY6LuJnuaowfwUmBSI6QPUVRpxyfYcfLIGIy3NNAYuHe'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def delete_state(data: list):
    url = "https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/"

    body = {
        "packages": data,
        "reference": "delete_last_package_state_history",
        "action": "delete_last_package_state_history"
    }

    response = requests.post(url, headers=headers, data=body)
