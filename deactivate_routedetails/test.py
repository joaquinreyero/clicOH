import requests
import json

url = "https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/"

payload = json.dumps({
  "packages": [
    1112235
  ],
  "reference": 105,
  "action": "change_pre_assigned_last_mile_dispatcher"
})
headers = {
  'User-Agent': 'None',
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwNDAxMDc2LCJqdGkiOiJiZDZhMzYwN2QzNDI0YWMzYjZjODQwMzA3NmQ1MmUwZCIsInVzZXJfaWQiOjF9.K_u9S_gaVWnpWsW7R3GsLkPxfTjrvc-l-DUY7BAvrUk',
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=kFFFgScSe4jpIrPPYMVoqY6LuJnuaowfwUmBSI6QPUVRpxyfYcfLIGIy3NNAYuHe'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
