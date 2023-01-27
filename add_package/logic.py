import requests

global token 
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMzgzMjM2LCJqdGkiOiIwNTE4ZjRjMTM2ODg0ZmE2OTk5MzA2NDA5NWM4Mjg3MyIsInVzZXJfaWQiOjF9.teBtp0kiVPx_tpOxzuS3TxgGfWyMU3ppeMX2YLGIAo4"

global headers
headers = {'Authorization': 'Bearer ' + token}


def get_route(route_id):

    urlRoute = "https://release--api.clicoh.com/api/v1/driver/routes/{}/".format(str(route_id))
    routes = requests.get(urlRoute, headers = headers)

    if routes.status_code == 200:
        data = routes.json()
    else:
        print('La ruta no existe{}, error: '.format(route_id), routes.status_code)
    return

#Paquetes a rutear y id de la ruta deseada
package_to_route = [
    ['code',1],
    ['code',1],
    ['code',1],
]
for i in range(len(package_to_route)):
    print(package_to_route[i][1])


#tener en cuenta que si la ruta esta finalizada el estado puede ser delivered,pup,retornando a sucursal
route_state_dic = {
    '5' : 6,                #travelling
}

ok_package_states = [ 
    '26',                   #on_lookup_batch
    '34',                   #traveling_mid_mile
    '25',                   #1st_mile
    '11',                   #ready
    '21',                   #at_Destination
    '31',                   #dispatched
    '23',                   #last_mile
]

package_state = 23
route_state = 6


inicio = package_states_list.index('{}'.format(package_state))
final = route_state_dic['{}'.format(route_state)]


for i in range(final - inicio):
    pass
