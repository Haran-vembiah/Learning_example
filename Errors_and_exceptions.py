def add_int_number():
    while True:
        try:
            result = int(input("Enter a number"))
            result/0
        except (FloatingPointError,ZeroDivisionError,ValueError) as msg:
            print(f"This is not a number {msg}")
            continue
        # else:
        #     print("This is a number")
        #     break
        finally:
            print("I am executing at end always")
    if 2>2:
        raise
add_int_number()
