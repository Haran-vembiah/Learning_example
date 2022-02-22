def samp(setup):
    for i in range(0, setup):
        print("Value of setup:", setup)
        print("value of setup:", setup)
        print("value of i:", i)

        if i == 1:
            print(i)
            setup = setup - 1
            # samp(setup)
        else:
            print("no action")


setup = 5
samp(setup)

results = [(i, j)
           for i in range(10)
           for j in range(i)]

print(results)
