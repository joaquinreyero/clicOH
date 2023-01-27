#from logic import ok,route,ok_packages


if __name__ == "__main__":  

    data = [
        ['code',1],
        ['code',234],
        ['code',324],
        ['code',1],
        ['code',1],
    
    ]   

    routes = []
    for i in range(len(data)):
        routes.append(data[i][1])
    for i in range(len(set(routes))):
        print(i)


    # Resultado: [1, 2, 3, 4, 5]

    #ok_packages(data)