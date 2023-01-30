import gspread
from bot import add_route_details
from logic import route_ok_for_add, package_ok_for_add, change_state
from oauth2client.service_account import ServiceAccountCredentials
import time

start_time = time.time()

# sheet configs
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./add-route-details-860641dac2c6.json', scope)
client = gspread.authorize(creds)
sheet = client.open("TMS").get_worksheet(0)

# get add package and deactivate route details from sheets
cells = sheet.get_values('B6:C52')
cell_add_package_route = sheet.get_values('B6:B52')
cell_add_package_package = sheet.get_values('C6:C52')

route_list, package_list = [], []
# convert cells to simple list and create a set, ROUTE
for sub_list in cell_add_package_route:
    route_list.extend(sub_list)
unique_route = set(route_list)
route_list = list(unique_route)

# convert cells to simple list and create a set, PACKAGE
for sub_list in cell_add_package_package:
    package_list.extend(sub_list)
unique_package = set(package_list)

route_ok = [
]
for i in range(len(route_list)):
    a = route_ok_for_add(route_list[i])
    if a[0]:
        route_ok.append(a)

package_ok = [

]
for i in range(len(package_list)):
    for j in range(len(route_ok)):
        if cells[i][0] in route_ok[j]:
            a = package_ok_for_add(cells[i][1], cells[i][0])
            if a[0]:
                package_ok.append(a)

package_bot_add = []

for i in range(len(package_ok)):
    code = package_ok[i][1]
    route = package_ok[i][3]
    package_bot_add.append([route, code])

unique_route = [

]
for i in range(len(route_ok)):
    unique_route.append(route_ok[i][1])

add_route_details(package_bot_add, unique_route)

group_x = [
    'traveling_mid_mile',
    'on_lookup_batch',
    '1st_mile'
]
group_x_add = [

]
group_r_add = [

]
group_at = [
    'at_destination',
    'dispatched'
]
group_at_add = [

]

for i in range(len(package_ok)):

    if package_ok[i][2] in group_x:
        group_x_add.append(package_ok[i][4])

    if package_ok[i][2] == 'ready':
        group_r_add.append(package_ok[i][4])

    if package_ok[i][2] in group_at:
        group_at_add.append(package_ok[i][4])

if group_x_add:
    change_state(group_x_add, 'ready')
    group_r_add.extend(group_x_add)

if group_at_add:
    change_state(group_r_add, 'at_destination')
    group_at_add.extend(group_r_add)

if group_at_add:
    change_state(group_at_add, 'last_mile')

elapsed_time = time.time() - start_time

cell_delete = sheet.range("B6:C52")
for cell in cell_delete:
    cell.value = ""

# sheet.update_cells(cell_delete)


print("Execution time: {} ".format(elapsed_time))
