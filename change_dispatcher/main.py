import requests

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMzgzMjM2LCJqdGkiOiIwNTE4ZjRjMTM2ODg0ZmE2OTk5MzA2NDA5NWM4Mjg3MyIsInVzZXJfaWQiOjF9.teBtp0kiVPx_tpOxzuS3TxgGfWyMU3ppeMX2YLGIAo4"
global headers
headers = {'Authorization': 'Bearer ' + token}


def return_dispatcher_dict(driver_type: str) -> dict:
    dispatcher_dict: dict = {}
    next_page = 1
    while True:
        if next_page is not None:
            url = 'https://release--api.clicoh.com/api/v1/driver/drivers/?driver_type={driver_type}&page={page}' \
                .format(driver_type=driver_type, page=next_page)
            response = requests.get(url, headers=headers).json()
            next_page = response.get("next")
            for i in range(len(response["results"])):
                if response["results"][i]["is_active"]:
                    dispatcher_dict.update({
                        "{}".format(response["results"][i]["user"]["username"]):
                            "{}".format(response["results"][i]["id"])
                    })
        else:
            return dispatcher_dict

def test():
    body = {"packages":[1112235],"reference":19,"action":"change_pre_assigned_last_mile_dispatcher"}
    response = requests.post('https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/',
                        headers=headers,
                        data= body)
    print(response)
if __name__ == "__main__":
    print(return_dispatcher_dict("last_mile"))



{"packages":["1112235"],"reference":40,"action":"change_pre_assigned_last_mile_dispatcher"}