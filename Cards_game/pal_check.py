import random
[p1,p2]=[[],[]]

def displ(p1, p2):
   for pos in range(1,10,1):
        print(' ', end='')
        if pos in p1:
            print('X',end='')
        elif pos in p2:
            print('O', end='')
        else:
            print(' ',end='')
        print(' |', end='')
        if pos%3==0:
            print("\n----------\n")

def p_input(player_no):
    choice=int(input("Enter the choice for Player " + str(player_no) + ":       "))
    if choice in p1 or choice in p2 or choice not in range(1,10):
        print(str(choice)+" is used or not valid. Please enter other value")
        return 0
    else:
        if player_no==1:
            p1.append(choice)
        else:
            p2.append(choice)
    return 1

def check_result(p1,p2):
    combinations=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]

    for x in combinations:
        fl=True
        for t in x:
            if t not in p1:
                fl=False
        if fl==True:
            return 1
    for x in combinations:
        fl=True
        for t in x:
            if t not in p2:
                fl = False
            if fl == True:
                return 2
            return 0

def game ( ):
    global p1
    global p2
    p1.clear ( )
    p2.clear ( )
    result = 0
    i = random.randint ( 0, 1 )
    for pos in range ( 1, 10, 1 ):
        print ( ' ' + str ( pos ) + ' |', end='' )
        if pos % 3 == 0:
            print ( "\n--------------------\n" )
    while result == 0:
        input_success = 0
        while input_success == 0:
            input_success = p_input ( (i % 2) + 1 )

        i += 1
        displ ( p1, p2 )
        p3 = p1 + p2
        p3.sort ( )
        result = check_result ( p1, p2 )
    if result:
        print ( "Game Over! Winner is:" + str ( result ) )
    elif p3 == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        print ( "You both lose" )

def game_run ( ):
    cont = 'y'
    while cont == 'y' or cont == 'Y':
        game ( )
        cont = input ( "Do you want to continue? Press [Y/y] to continue    :   " )
    print ( "\n*****GOOD BYE*****\n" )

game_run ( )
