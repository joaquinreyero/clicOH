import requests


#Retorna Route detail a desactivar
def RdID(data,package):
        for key in range (len(data['details'])):
            if data['details'][key]['package']['code'] == package:

                rd_ID = data['details'][key]['id']
                package_id = data['details'][key]['package']['id']
                package_state = data['details'][key]['package']['current_state']['id']

                return rd_ID,package_id,package_state

        print("El paquete {} no se encuentra en la ruta".format(package))     
        raise SystemExit(1)  

#Desactiva route detail
def deactivateRD(headers, rd_id):

    urlRD = 'https://release--api.clicoh.com/api/v1/driver/route_details/{}/'.format(str(rd_id))
    body = {'is_active':'false'}

    deactivate = requests.patch(urlRD, headers = headers, data = body)

    if deactivate.status_code == 200:
        return print("Route detail desactivado")
    else:
        print('Error:', deactivate.status_code)
        raise SystemExit(1)

#Elimina los estados hasta que se encuentre en 
#Pedido listo o listo para despacho
def changeStatus(package_id,package_state,headers):

    #URL Massive changes
    urlMC = "https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/"

    body = {
        "packages":["{}".format(package_id)],
        "reference":"delete_last_package_state_history",
        "action":"delete_last_package_state_history"
    }

    #URL Package states
    urlPS = 'https://release--api.clicoh.com/api/v1/pickup_points/packages/{}/'.format(str(package_id))

    while package_state != 11 and package_state != 21:
        requests.post(urlMC, headers = headers, json = body)
        responsePS = requests.get(urlPS, headers=headers).json()
        package_state = responsePS['current_state']['state']['id']

    return

#Inicia request
def makeRequest(route_id,package,headers):
    
    urlRoute = "https://release--api.clicoh.com/api/v1/driver/routes/{}/".format(str(route_id))

    routes = requests.get(urlRoute, headers = headers)

    if routes.status_code == 200:
        data = routes.json()
        rd_id, package_id, package_state = RdID(data,package)
        deactivateRD(headers,rd_id)
        changeStatus(package_id,package_state,headers)
    else:
        print('Error: ', routes.status_code)


#Auth
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMzgzMjM2LCJqdGkiOiIwNTE4ZjRjMTM2ODg0ZmE2OTk5MzA2NDA5NWM4Mjg3MyIsInVzZXJfaWQiOjF9.teBtp0kiVPx_tpOxzuS3TxgGfWyMU3ppeMX2YLGIAo4"
headers = {'Authorization': 'Bearer ' + token}

#Completar codigo y ruta del paquete a desactivar
routedetails_array = [
    ['GSNRV84102',28245],
    ['HWAST38249',28245],
    ['DTXLE95724',28245],
    ['MPZJK92863',28245]

    ]

for i in range(len(routedetails_array)):
    makeRequest(
        routedetails_array[i][1],
        routedetails_array[i][0],
        headers
    )




