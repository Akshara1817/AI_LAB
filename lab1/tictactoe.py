import random
user=int(input("enter 0 for O and 1 for x:"))
sys=1-user
arr=['o','x']
a = [[' ' for _ in range(3)] for _ in range(3)]
win=False
for i in range (0,3):
    for j in range (0,3):
        a[i][j]=' '
def printboard():
    for row in a:
        print(row)
def check():
    for i in range (0,3):
        for j in range (0,3):
            if(a[i][j]==' '):
                return 1
    else:
        return 0
def checkwinner():
     #check if there is 3 in a row
    global win
    for i in range(3):
        if a[i][0] == a[i][1] == a[i][2] != ' ':
            win = True
            return
        if a[0][i] == a[1][i] == a[2][i] != ' ':
            win = True
            return
    if a[0][0] == a[1][1] == a[2][2] != ' ':
        win = True
        return
    if a[0][2] == a[1][1] == a[2][0] != ' ':
        win = True
        return
turn=0    
while win==False and check():
    
    if(turn==0):
        i=int(input("enter x coord: "))
        j=int(input("enter y coord: "))
        if a[i][j]==' ':
            a[i][j]=arr[user]
            printboard()
            checkwinner()
            turn=1
        else:
            print("invalid")
    elif(turn==1):
        i=int(random.randint(0,2))
        j=int(random.randint(0,2))
        if a[i][j]==' ':
            a[i][j]=arr[sys]  
            #print("\n")
            print("-------------------------")     
            print("computer's turn")
            printboard()
            print("-------------------------")
            checkwinner()
            turn=0