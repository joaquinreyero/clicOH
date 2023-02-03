import gspread
from bot import add_route_details, sync_route
from logic import route_ok_for_add, package_ok_for_add, change_state, get_route_details_id, deactivate_route_detail
from oauth2client.service_account import ServiceAccountCredentials
import time


def convert_to_simple_list(cells):
    # Convert cells to simple list and create a set
    cells_list = []
    for i in cells:
        cells_list.extend(i)
    cells_unique = set(cells_list)
    cells_list = list(cells_unique)

    return cells_list


def add_package(route_list, cells_add_package):
    # Create lists
    add_route_ok, add_package_ok, route_id, package_bot_add, package_code = [], [], [], [], []

    # Create a list of correct routes
    for i, route in enumerate(route_list):
        response = route_ok_for_add(route)
        if response[0]:
            add_route_ok.append(response)

    # Create a list of correct route ids
    for i, route in enumerate(add_route_ok):
        route_id.append(route[1])

    # Create a list of correct package from the correct routes ids
    for i, sheet in enumerate(cells_add_package):
        if sheet[0] in route_id:
            a = package_ok_for_add(sheet[1], sheet[0])
            if a[0]:
                add_package_ok.append(a)

    # Create a list of package for Selenium format
    for i, package in enumerate(add_package_ok):
        code, route = package[1], package[3]
        package_bot_add.append([route, code])
        package_code.append(code)

    # Create groups by package states
    group_stage_1 = ['traveling_mid_mile', 'on_lookup_batch', '1st_mile']
    group_stage_2 = ['ready']
    group_stage_3 = ['at_destination', 'dispatched']

    # Sort package by group
    package_by_group_stage_1, package_by_group_stage_2, package_by_group_stage_3 = [], [], []

    for i, package in enumerate(add_package_ok):

        if package[2] in group_stage_1:
            package_by_group_stage_1.append(package[4])

        if package[2] in group_stage_2:
            package_by_group_stage_2.append(package[4])

        if package[2] in group_stage_3:
            package_by_group_stage_3.append(package[4])

    # checks if the list is empty, changes the state of the package and therefore adds the packages to the next group
    if package_by_group_stage_1:
        change_state(package_by_group_stage_1, 'ready', package_code)
        package_by_group_stage_2.extend(package_by_group_stage_1)

    if package_by_group_stage_2:
        change_state(package_by_group_stage_2, 'at_destination', package_code)
        package_by_group_stage_3.extend(package_by_group_stage_2)

    if package_by_group_stage_3:
        change_state(package_by_group_stage_3, 'last_mile', package_code)
        print("Testing")

    # Call Selenium
    if package_bot_add:
        add_route_details(package_bot_add, route_id)
        print(f"Packages added {package_bot_add}")


def deactivate_route_details(route_list, package_list):
    # Create a list of route details
    routes_details_response = [[]]
    for i, route in enumerate(route_list):
        routes_details_response.append(get_route_details_id(route, package_list))
    # Convert response into flat list
    flat_list = [item for sublist in routes_details_response for item in sublist]
    routes_details_response = flat_list
    # Create a lists
    routes_details_id, package_id_list, package_code, routes_id = [], [], [], []
    for i, details in enumerate(routes_details_response):
        routes_details_id.append(details[1])
        package_id_list.append([details[2], details[3]])
        routes_id.append(details[4])
        package_code.append(details[0])

    bad_package_status = ['delivered', 'canceled', 'arrived']
    # Deactivate route details and add packages to package change list
    package_id_for_change = []
    for i, details in enumerate(routes_details_id):
        deactivate_route_detail(details, package_code[i])
        if package_id_list[i][1] not in bad_package_status:
            package_id_for_change.append(package_id_list[i][0])
    # Change package states and sync routes
    if package_id_for_change:
        change_state(package_id_for_change, 'at_destination', package_id_for_change)
        route_set = set(routes_id)
        routes_id = list(route_set)
        sync_route(routes_id)
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
        route_list = convert_to_simple_list(cell_add_package_route)
        add_package(route_list, cells_add_package)

    if cells_deactivate_route_details:
        route_list = convert_to_simple_list(cell_deactivate_route_route)
        package_list = convert_to_simple_list(cell_deactivate_route_package)
        deactivate_route_details(route_list, package_list)

    # Update sheet
    cell_delete_a = sheet.range("B6:C52")
    if cell_delete_a:
        for cell in cell_delete_a:
            cell.value = ""
        # sheet.update_cells(cell_delete_a)

    cell_delete_b = sheet.range("E6:F52")
    if cell_delete_b:
        for cell in cell_delete_b:
            cell.value = ""
        # sheet.update_cells(cell_delete_b)

    elapsed_time = time.time() - start_time
    print("Execution time: {} ".format(elapsed_time))


if __name__ == "__main__":
    main()
