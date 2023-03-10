import json
import requests


def token():
    url = "https://ppointapi.clicoh.com/api/token/"

    payload = json.dumps({
        "username": "admin",
        "password": "P4t4g0n14-99"
    })

    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=kFFFgScSe4jpIrPPYMVoqY6LuJnuaowfwUmBSI6QPUVRpxyfYcfLIGIy3NNAYuHe'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    return response["access"]


def headers():
    headers = {
        'Authorization': f'Bearer {token()}',
        'Content-Type': 'application/json',
        'Cookie': 'csrftoken=kFFFgScSe4jpIrPPYMVoqY6LuJnuaowfwUmBSI6QPUVRpxyfYcfLIGIy3NNAYuHe'
    }
    return headers


def package_ok_for_add(package_code: str, route_id: str):
    url = f"https://ppointapi.clicoh.com/api/v1/pickup_points/packages/?order_by=-id&section=list_packages&search={package_code}"
    response = requests.get(url, headers=headers()).json()

    # Check if the package exists
    if response["count"] == 0:
        print(f"Package {package_code} not found")
        return False, None, None, None, None

    if response["results"][0]["code"] != package_code and response["results"][0]["reference_code"] != package_code:
        print(f'Package {package_code} not found')
        return False, None, None, None, None

    package_code = response["results"][0]["code"]
    package_id = response["results"][0]["id"]

    ok_states = [
        'traveling_mid_mile',
        'on_lookup_batch',
        '1st_mile',
        'ready',
        'at_destination',
        'dispatched',
    ]
    package_state = response["results"][0]["current_state"]["state"]["name"]

    if package_state not in ok_states:
        print(f"Package {package_code} with a invalid state {package_state}")
        return False, None, None, None, None

    return True, package_code, package_state, route_id, package_id


def route_ok_for_add(route_id: str):
    url = f"https://ppointapi.clicoh.com/api/v1/driver/routes/{route_id}/"
    response = requests.get(url, headers=headers())
    if response.status_code != 200:
        print(f"Cant find route id {route_id}")
        return False, None

    response_dic = response.json()
    route_type = response_dic["route_type"]

    if route_type != "last_mile":
        print(f"Invalid type route {route_type}")
        return False, None

    route_state = response_dic["current_state"]["state"]["name"]

    if route_state != "traveling":
        print(f"Invalid route {route_id}, state {route_state}")
        return False, None

    return True, route_id


def change_state(data: list, state: str, code: list):
    url = "https://ppointapi.clicoh.com/api/v1/pickup_points/packages/massive_changes/"
    payload = json.dumps(
        {
            "packages": data,
            "reference": state,
            "action": "change_state"
        }
    )
    response = requests.request("POST", url, headers=headers(), data=payload)

    if response.status_code != 200:
        print(f"Error trying to change {data} states to {state}")
        return
    print(f"Packages {code} transitioned successfully to {state}")


def deactivate_route_detail(route_details_id: str, package_code: str):
    url, body = f'https://ppointapi.clicoh.com/api/v1/driver/route_details/{route_details_id}/', {
        'is_active': 'false'}
    deactivate = requests.patch(url, headers=headers(), data=body)

    if deactivate.status_code == 200:
        print(f"Route details {route_details_id} deactivated of package {package_code}")
        return

    print(f'Error {deactivate.status_code} while deactivating route {route_details_id} of package {package_code}')


def get_route_details_id(route_id: str, package_code: list):
    url = f"https://ppointapi.clicoh.com/api/v1/driver/routes/{route_id}/"
    response, response_list = requests.get(url, headers=headers()), []

    if response.status_code != 200:
        print(f'Error cant find route {route_id}')
        return None

    data = response.json()
    for index, details in enumerate(data["details"]):
        if details["package"]["code"] in package_code or details["package"]["reference_code"] in package_code:
            response_list.append(details['package']['code'])
            response_list.append(details['id'])
            response_list.append(details['package']['id'])
            response_list.append(details['package']['current_state']['state']['name'])
            response_list.append(route_id)

    sublist = [response_list[i:i + 5] for i in range(0, len(response_list), 5)]
    if not sublist:
        print(f"Cant find any of these package {package_code} in the route {route_id}")
    return sublist
