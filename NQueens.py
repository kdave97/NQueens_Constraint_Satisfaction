import sys
import copy
import time
global domains
global tmp
global cnt
domains = []
cnt=0;

class QueenGraph:
    
    def __init__(self,n):
        
        var=[]
        for i in range(n):
            var.append("Q"+str(i))
        self.size=n;                                                                       #n is the no of queens          
        self.variables=var                                                                 #VARIABLE NAMES 
        self.domain=[[i for i in range(n)] for i in range(n) ]                             # DOMAIN of size N*N     
        self.row=0
        self.sol=[]                                                                        # Maintaining All Solutions
        self.csol=[]                                                                       # Maintaining Solutions in the form of 1D array indicating the column values
        self.board=[0]*n
        for i in range(n):
            self.board[i]=[0]*n                                                            # Intitializing the board for display purpose 

    def backtrack_FC(self,board,row,domain):
        global cnt
        dom=copy.deepcopy(domain)
        d1=list(filter(lambda x: x!= 'X',dom[row]))                                         # d1 holds the list of unassigned variables
        domains.append(copy.deepcopy(dom))
        for i in d1:                                                                        # Selecting an element from the unassigned variable list
            board[row][i]= 1                                                                # Queen is placed on the board
            
            if row==self.size-1:                                                            # The if condition executed when it reaches the last row  
                s_board=copy.deepcopy(board)                                                # and the inner part finds the solution and add the solution
                self.sol.append(s_board)                                                    # to the sol list.
                board[row][i]=0                                                             #    
                return
            
            up_dom=self.forward_check(copy.deepcopy(dom),row,i)                             # Forward checking inference is done to update the domain.
            #print ("Updated domain:",up_dom)
            n_d1=list(filter(lambda x: x!= 'X',up_dom[row+1]))                              # We determine n_d1 to check weather the backtracking is to be preformed or not.    
            if len(n_d1)!=0:                                                                # If there is some place where we can keep place the queen then we perform the nacktrack.   
                self.backtrack_FC(copy.deepcopy(board),row+1,up_dom)
                board[row][i]=0
                cnt+=1
            else:
                cnt+=1
                board[row][i]=0                                                             # If there is no place where queen can be placed, we move the queen to the next position in the row.
                    
    def backtrack_MAC(self,board,row,domain):                                               # The Maintaining arc consistency tuns the AC3 algorithm whenver we assign a new queen. It ensures that no partial assignment is          

        dom=copy.deepcopy(domain)           
        d1=list(filter(lambda x: x!= 'X',dom[row]))                                         # d1 holds the list of unassigned variables
        domains.append(copy.deepcopy(dom))
        for i in d1:
            board[row][i]=1
            
            if row==self.size-1:
                s_board=copy.deepcopy(board)
                self.sol.append(s_board)
                board[row][i]=0
                return
            up_dom=self.forward_check(copy.deepcopy(dom),row,i)                               # We perform initally forward checking to update the domain.   
            new_dom = self.AC3(copy.deepcopy(up_dom),row,i)                                   # We perform the AC3 Consistency to determine all the possible places which are availbale where we can place the queen
            #print ("Updated domain:",up_dom)
            #n_d1=list(filter(lambda x: x!= 'X',up_dom[row+1]))
            #print (n_d1)
            #if len(n_d1)!=0:
            if new_dom:                                                                       # If domain is not empty then we can perform the backtrack       
                self.backtrack_MAC(copy.deepcopy(board),row+1,up_dom)
                board[row][i]=0
            else:
                board[row][i]=0                                                                # If arc consistency return False we move the initial queen to neighbouring place. 

    def revise(self, domain, tup):                                                              
        revised = False
        #new_val = []
        for i in range(len(domain[tup[0]])):
            flag = 0
            val1 = domain[tup[0]][i]
            if val1 == 'X':
                continue
            for j in range(len(domain[tup[1]])):
                val = domain[tup[1]][j]
                if val == "X":
                    continue
                if val1 != val and abs(tup[0]-tup[1]) != abs(val1-val):
                    flag = 1
                    break
            if flag == 0:
               domain[tup[0]][i] = "X"
               revised = True
        return revised
    
    def AC3(self,domain,row,col):                                                                 # The AC-3 known as the arc consistency maintains a queue of arcs. It maintains all the possible                      
        que=[]                                                                                    # row combinations for the queens. It pops out a random tuple and makes it consistent.                        
        for i in range(row+1,len(domain)):                                                        #  If Domain changes, it revises and add new arcs in the queue. 
            for j in range(row+1,len(domain)):                                                    # Else, it moves to the next tuple in the queue.
                if i!=j:
                    que.append([i,j])
        while que:
            tup = que.pop(0)
            if self.revise(domain,tup):
                if len(domain[tup[0]]) == 0:
                    return False
                for k in range(row+1,len(domain)):
                    if k!=tup[0] and k != tup[1]:
                        que.append([k,tup[0]])
    
        #return True
        return domain       
        
            
    def forward_check(self,domain,row,col):                                                       # Forward Checking is done to ensure wheather the queen can be placed at a particluar palce           
        for r1 in range(len(domain)):                                                             # considering the constarints that are imposed on queens as we start placing them.       
            for c1 in range(len(domain[r1])):                                                     # Placing each queen leads to updating the domain.  
                if r1==row:
                    domain[r1][c1]="X"
                if c1==col:
                    domain[r1][c1]="X"
                    
        tr = row                                                                                  # Here we eliminate all the possible domain values which are diagonally to the queen           
        tc = col                                                                                  # and belong to the same column.
            
        for c in range(len(domain)-1):
            if row==len(domain)-1 or col==len(domain)-1:
                break
            else:
                        
                domain[row+1][col+1]="X"
                row+=1;
                col+=1;
        row=tr
        col = tc
        for c in range(len(domain)-1):
            if row==len(domain)-1 or col==0:
                break
            else:
                      
                domain[row+1][col-1]="X"
                row+=1;
                col-=1;
            
        return domain

    def column_sol(self,sol):
        c_sol=[]
        for i in sol:
            a=[]
            for j in i:
                a.append(j.index(1))
            c_sol.append(a)
    
        return c_sol             

    
    def write_file(self,RFile,sol,c_sol,final):
        f = open("RFile.txt", "w")
        f.write("***********************ALL SOLUTIONS**************")
        f.write("\n")
        for i in self.sol:
            f.write("Solution: ")
            f.write("\n")
            for j in i:
                f.write(str(j))
                f.write("\n")
        f.write("\n")
        f.write("********************UNIQUE SOLUTIONS**************")
        f.write("\n")
        for k in final:
            f.write("Solution:")
            f.write(str(k))
            f.write("\n")
            
        f_len=len(final)
        f.write("Unique Soln: ")
        f.write(str(f_len))
        f.close()

    def write1_file(self,CFile):
        f = open("CFile.txt", "w")
        f.write("Variables: ")
        f.write(str(q.variables))
        f.write("\n")
        f.write("Domains: ")
        f.write("\n")
        for i in range(len(q.domain)):
            f.write(q.variables[i])
            f.write(str(q.domain[i]))
            f.write("\n")
        f.write("\n")    
        f.write("Constraints: ")
        f.write("\n")
        for i in range(len(q.variables)):
            for j in range(i+1,len(q.variables)):
                f.write(str(q.variables[i])+" != "+str(q.variables[j]))
                f.write("\n")
                f.write("|"+str(q.variables[i])+"-"+str(q.variables[j])+"| != abs("+str(i)+"-"+str(j)+")")
                f.write("\n")
                
        f.close()
        
    def UniqueSOL(self,c_sol):                                                                      # We can determine the unique solutions from the set of all solutions by eliminating 
        
        def rotate_board(s_sol):                                                                    # those solutions which are similar when the board is rotated or reflected.     
            temp=[0]*len(s_sol)
            for i in range(len(s_sol)):
                a=s_sol[i]
                temp[a]=len(s_sol)-i-1
            return temp    

        def transpose_board(s_sol):
            temp=[0]*len(s_sol)
            for i in range(len(s_sol)):
                a=s_sol[i]
                temp[a]=i
            return temp
                                                                                                    # There exist 7 possible cases:    
        def rotate_board_90(s_sol):                                                                   #1) Rotate board by 90  
            return rotate_board(s_sol)                                                                #2) Rotate board by 180
        def rotate_board_180(s_sol):                                                                  #3) Rotate board by 270
            return rotate_board(rotate_board(s_sol))                                                  #4) Reflect and rotate by 90
        def rotate_board_270(s_sol):                                                                  #5) Reflect and rotate by 180
            return rotate_board(rotate_board(rotate_board(s_sol)))                                    #6) Reflect and rotate by 270 
        def trans_rotate_90(s_sol):                                                                   #7) Reflect  
            return rotate_board(transpose_board(s_sol))
        def trans_rotate_180(s_sol):
            return rotate_board(rotate_board(transpose_board(s_sol)))
        def trans_rotate_270(s_sol):
            return rotate_board(rotate_board(rotate_board(transpose_board(s_sol))))
    
        def unique(c_sol):
            s=c_sol
            uni=[]
    
            while len(s)!=0:
                s_sol=s[0]
                uni.append(s_sol)
                a=[]
        
                a.append(s_sol)
                a.append(rotate_board_90(s_sol))
                a.append(rotate_board_180(s_sol))
                a.append(rotate_board_270(s_sol))
                a.append(transpose_board(s_sol))
                a.append(trans_rotate_90(s_sol))
                a.append(trans_rotate_180(s_sol))
                a.append(trans_rotate_270(s_sol))
        
                for i in a:
                    try: 
                        s.remove(i)
                    except: 
                        continue
            return uni

        Final=unique(c_sol)
        
        return Final    


if __name__=="__main__":

    alg=sys.argv[1];
    N=sys.argv[2];
    CFile=sys.argv[3];
    RFile=sys.argv[4];
    if alg=="FOR":
        init=time.time()
        q=QueenGraph(int(N))
        q.backtrack_FC(q.board,q.row,q.domain)
        print ("Time taken to execute: %s sec" %(time.time()-init))
        print ("Total Solutions :" ,len(q.sol))
        print ("Backtrack Couts:", cnt)
        
        c_sol=q.column_sol(q.sol)
        final=q.UniqueSOL(c_sol)
        print ("Unique Solutions :", len(final))
        q.write_file(RFile,q.sol,c_sol,final)
        q.write1_file(CFile)
    if alg=="MAC":
        init=time.time()
        q=QueenGraph(int(N))
        q.backtrack_MAC(q.board,q.row,q.domain)
        print ("Time taken to execute: %s sec" %(time.time()-init))
        print ("Total Solutions :" ,len(q.sol))
        c_sol=q.column_sol(q.sol)
        final=q.UniqueSOL(c_sol)
        print ("Unique Solutions :", len(final))
        q.write_file(RFile,q.sol,c_sol,final)
        q.write1_file(CFile)
        
