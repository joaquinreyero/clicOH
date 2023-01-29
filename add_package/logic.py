import requests

global token
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMzgzMjM2LCJqdGkiOiIwNTE4ZjRjMTM2ODg0ZmE2OTk5MzA2NDA5NWM4Mjg3MyIsInVzZXJfaWQiOjF9.teBtp0kiVPx_tpOxzuS3TxgGfWyMU3ppeMX2YLGIAo4"

global headers
headers = {'Authorization': 'Bearer ' + token}


def package_ok(package_code: str):
    url = "https://release--api.clicoh.com/api/v1/pickup_points/packages/?order_by=-id&section=list_packages&search={}".format(
        package_code)

    response = requests.get(url, headers=headers).json()

    if response["count"] == 0 or response["results"][0]["code"] != package_code:
        print("Package {} not found".format(package_code))
        return False, None

    ok_states = [
        'traveling_mid_mile',
        'on_lookup_batch',
        '1st_mile',
        'ready',
        'at_destination',
    ]
    package_state = response["results"][0]["current_state"]["state"]["name"]

    if package_state not in ok_states:
        print("Package {} have a invalid state".format(package_code))
        return False, None

    return True, package_state


def route_ok(route_id: str):
    url = "https://release--api.clicoh.com/api/v1/driver/routes/{}/".format(route_id)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error with route {}".format(route_id))
        return False, None

    response_dic = response.json()

    if response_dic["route_type"] != "last_mile":
        print("Invalid type route")
        return False, None

    ok_states = ["traveling", "ready"]
    route_state = response_dic["current_state"]["state"]["name"]

    if route_state not in ok_states:
        print("Invalid route state")
        return False, None

    stop_number = response_dic["progress"]["total"]

    return True, route_state, stop_number


def change_package_state(package: list, state: str, package_type: str):
    state_flow_lh = [
        'traveling_mid_mile',
        'at_destination',
        'dispatched',
        'last_mile'
    ]

    state_flow = [
        'on_lookup_batch',
        '1st_mile',
        'ready',
        'at_destination',
        'dispatched',
        'last_mile'
    ]

    index = state_flow.index('{}'.format(state))

    for i in range(len(state_flow) - index):
        return


def change_state(data: list, state: str):
    url = "https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/"

    body = {
        "packages": data,
        "reference": state,
        "action": "change_state"
    }
    response = requests.post(url, headers=headers, data=body)


