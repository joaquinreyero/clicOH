import gspread
from bot import add_route_details, sync_route
from logic import route_ok_for_add, package_ok_for_add, change_state, get_route_details_id, deactivate_route_detail
from oauth2client.service_account import ServiceAccountCredentials
import time


def add_package(cell_add_package_route, cell_add_package_package, cells_add_package):
    # Convert cells to simple list and create a set, ROUTE
    add_route_list, add_package_list, = [], []
    for i in cell_add_package_route:
        add_route_list.extend(i)
    add_route_unique = set(add_route_list)
    route_list = list(add_route_unique)

    # Convert cells to simple list and create a set, PACKAGE
    for i in cell_add_package_package:
        add_package_list.extend(i)

    # Create a list of correct routes
    add_route_ok, add_package_ok = [], []

    for i in range(len(route_list)):
        response = route_ok_for_add(route_list[i])
        if response[0]:
            add_route_ok.append(response)

    # Create a list of correct route ids
    route_id = []
    for i in range(len(add_route_ok)):
        route_id.append(add_route_ok[i][1])

    # Create a list of correct package
    for i in range(len(add_package_list)):
        for j in range(len(add_route_ok)):
            if cells_add_package[i][0] in route_id:
                a = package_ok_for_add(cells_add_package[i][1], cells_add_package[i][0])
                if a[0]:
                    add_package_ok.append(a)

    # Create a list of package for Selenium
    package_bot_add, package_code = [], []
    for i in range(len(add_package_ok)):
        code = add_package_ok[i][1]
        route = add_package_ok[i][3]
        package_bot_add.append([route, code])
        package_code.append(code)

    # Create groups by package states
    group_stage_1 = [
        'traveling_mid_mile',
        'on_lookup_batch',
        '1st_mile'
    ]
    group_stage_2 = [
        'ready'
    ]
    group_stage_3 = [
        'at_destination',
        'dispatched'
    ]

    # Sort package by group
    package_by_group_stage_1, package_by_group_stage_2, package_by_group_stage_3, package_by_group_stage_4 = [], [], [], []

    for i in range(len(add_package_ok)):

        if add_package_ok[i][2] in group_stage_1:
            package_by_group_stage_1.append(add_package_ok[i][4])

        if add_package_ok[i][2] in group_stage_2:
            package_by_group_stage_2.append(add_package_ok[i][4])

        if add_package_ok[i][2] in group_stage_3:
            package_by_group_stage_3.append(add_package_ok[i][4])

    # checks if the list is empty, changes the state of the package and therefore adds the packages to the next group
    if package_by_group_stage_1:
        change_state(package_by_group_stage_1, 'ready', package_code)
        package_by_group_stage_2.extend(package_by_group_stage_1)

    if package_by_group_stage_2:
        change_state(package_by_group_stage_2, 'at_destination', package_code)
        package_by_group_stage_3.extend(package_by_group_stage_2)

    if package_by_group_stage_3:
        change_state(package_by_group_stage_3, 'last_mile', package_code)
    # Call Selenium
    if package_bot_add:
        add_route_details(package_bot_add, route_id)
        print(f"These package have been added {package_bot_add}")


def deactivate_route_details(cell_deactivate_route_route, cell_deactivate_route_package):
    # Convert cells to simple list and create a set, ROUTE
    deactivate_route_list, deactivate_package_list, = [], []

    for i in cell_deactivate_route_route:
        deactivate_route_list.extend(i)
    deactivate_route_unique = set(deactivate_route_list)
    route_list = list(deactivate_route_unique)

    # Convert cells to simple list and create a set, PACKAGE
    for i in cell_deactivate_route_package:
        deactivate_package_list.extend(i)
    package_list = list(deactivate_package_list)

    # Get route details ids
    routes_details_response = []
    for i in range(len(route_list)):
        routes_details_response = (get_route_details_id(route_list[i], package_list))

    # Create a list of routes
    routes_id = []
    for i in range(len(routes_details_response)):
        routes_id.append(routes_details_response[i][4])

    # Create a list of package
    routes_details_id, package_id_list, package_code = [], [], []
    for i in range(len(routes_details_response)):
        package_code.append(routes_details_response[i][0])
        routes_details_id.append(routes_details_response[i][1])
        package_id_list.append([routes_details_response[i][2], routes_details_response[i][3]])

    bad_package_status = [
        'delivered',
        'canceled',
        'arrived'
    ]

    package_id_for_change = []
    for i in range(len(routes_details_id)):
        deactivate_route_detail(routes_details_id[i], package_code[i])
        if package_id_list[i][1] not in bad_package_status:
            package_id_for_change.append(package_id_list[i][0])

    if package_id_for_change:
        change_state(package_id_for_change, 'ready', package_id_for_change)
        sync_route(routes_id)
        print(f"Routes {routes_id} have been sync")
    else:
        print("Any route details have been deactivated")


def main():
    start_time = time.time()

    # Sheet configs
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('./add-route-details-860641dac2c6.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("TMS").get_worksheet(0)

    # Get add package
    cells_add_package = sheet.get_values('B6:C52')
    cell_add_package_route = sheet.get_values('B6:B52')
    cell_add_package_package = sheet.get_values('C6:C52')

    # Get deactivate route details
    cells_deactivate_route_details = sheet.get_values('E6:F52')
    cell_deactivate_route_route = sheet.get_values('E6:E52')
    cell_deactivate_route_package = sheet.get_values('F6:F52')

    if cells_add_package:
        add_package(cell_add_package_route, cell_add_package_package, cells_add_package)

    if cells_deactivate_route_details:
        deactivate_route_details(cell_deactivate_route_route, cell_deactivate_route_package)

    # Update sheet
    cell_delete_a = sheet.range("B6:C52")
    if cell_delete_a:
        for cell in cell_delete_a:
            cell.value = ""
        sheet.update_cells(cell_delete_a)

    cell_delete_b = sheet.range("E6:F52")
    if cell_delete_b:
        for cell in cell_delete_b:
            cell.value = ""
        sheet.update_cells(cell_delete_b)

    elapsed_time = time.time() - start_time
    print("Execution time: {} ".format(elapsed_time))


if __name__ == "__main__":
    main()
