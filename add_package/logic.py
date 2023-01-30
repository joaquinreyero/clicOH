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

    if response["count"] == 0:
        print("Package {} not found".format(package_code))
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
        'last_mile'
    ]
    package_state = response["results"][0]["current_state"]["state"]["name"]

    if package_state not in ok_states:
        print("Package {} with a invalid state".format(package_code))
        return False, None, None, None, None

    return True, package_code, package_state, route_id, package_id


def route_ok_for_add(route_id: str):
    url = "https://release--api.clicoh.com/api/v1/driver/routes/{}/".format(route_id)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Cant find route id: {}".format(route_id))
        return False, None, None, None

    response_dic = response.json()

    if response_dic["route_type"] != "last_mile":
        print("Invalid type route : {}".format(response_dic["route_type"]))
        return False, None, None, None

    ok_states = ["traveling"]
    route_state = response_dic["current_state"]["state"]["name"]

    if route_state not in ok_states:
        print(f"Invalid route {route_id}, state :{route_state}")
        return False, None, None, None

    stop_number = response_dic["progress"]["total"]

    return True, route_id, route_state, stop_number


def change_state(data: list, state: str):
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


def deactivate_route_detail(route_details_id: str):
    url = 'https://release--api.clicoh.com/api/v1/driver/route_details/{}/'.format(route_details_id)
    body = {'is_active': 'false'}

    deactivate = requests.patch(url, headers=headers, data=body)

    if deactivate.status_code == 200:
        return print("Route details {} deactivated".format(route_details_id))
    else:
        print('Error:', deactivate.status_code)


def get_route_details_id(route_id: str, package_code: list):
    response_list = []
    route_details_id = []
    package_id = []
    package_state = []

    url = "https://release--api.clicoh.com/api/v1/driver/routes/{}/".format(route_id)

    response = requests.get(url, headers=headers)

    if response.status_code != 200:

        print('Error with route {}'.format(route_id))
    else:
        data = response.json()

        for i in range(len(data['details'])):

            for j in range(len(package_code)):

                if data['details'][i]['package']['code'] == package_code[j] or data['details'][i]['package']['reference_code'] == package_code[j]:

                    response_list.append(package_code[j])
                    response_list.append((data['details'][i]['id']))
                    response_list.append(data['details'][i]['package']['id'])
                    response_list.append(data['details'][i]['package']['current_state']['state']['name'])

        sublist = [response_list[i:i + 4] for i in range(0, len(response_list), 4)]

        return sublist


