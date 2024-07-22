while True:
    try:
        n = int(input("enter a number: "))
        print(n)
        break
    except EOFError:
        break
    except ValueError:
        pass
    