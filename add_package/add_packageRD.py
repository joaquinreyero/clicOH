import requests



#Paquetes a rutear y id de la ruta deseada
package_to_route = [
    ['code',1],
    ['code',1],
    ['code',1],
]
for i in range(len(package_to_route)):
    print(package_to_route[i][1])

route_state_dic = {
    '5' : 6,                #travelling
    '6' : 7                 #delivered
}

package_states_list = [ 
    '26',                   #on_lookup_batch
    '34',                   #traveling_mid_mile
    '25',                   #1st_mile
    '11',                   #ready
    '21',                   #at_Destination
    '31',                   #dispatched
    '23',                   #last_mile
    '6'                     #delivered
]

package_state = 23
route_state = 6


inicio = package_states_list.index('{}'.format(package_state))
final = route_state_dic['{}'.format(route_state)]


for i in range(final - inicio):
    pass

##post: https://release--api.clicoh.com/api/v1/pickup_points/packages/massive_changes/
##{"packages":["1058236"],"reference":"dispatched","action":"change_state"}