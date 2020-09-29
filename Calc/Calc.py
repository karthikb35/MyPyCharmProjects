def ask():
    while True:
        try:
            q=int(input("Type a num"))
        except:
            try:
                q=float(input("Type a num"))
            except:
                print("Enter a num")
        else :
            print(q**2)