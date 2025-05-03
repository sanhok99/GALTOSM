import sys

#this function returns takes a string an a position of an opening bracket as input and returns the location of the closing bracket corresponding to the input location
def closing_bracket_loc(s, pos):
  if s[pos] not in "({[":
    return -99999

  bracket_map = {"(": ")", "[": "]"}
  opening_bracket = s[pos]
  closing_bracket = bracket_map[opening_bracket]

  stack = []

  for i in range(pos, len(s)):
    if s[i] == opening_bracket:
      stack.append(opening_bracket)
    elif s[i] == closing_bracket:
      stack.pop()
      if not stack:
        return i












"""ACTION to STATE Translator"""











"""
APRCTL TO PRCTL
APCTL  TO PCTL

GRAMMAR of APRCTL and APCTL (APCTL is a subcase of APRCTL) (https://dl.acm.org/doi/pdf/10.1145/3696431)

FUNCTION DETAILS
1 upon recieving the input formula in 'sldlr()' function, it first detects the state operation
  RECIEVES the operation and the formula(s) and calls itself recursievely until base case is reached, by performing nescessary operations of embedding

2 detecting the operation in the state formula using 'sldl_detect_state()' which could be
  a) no operation that is TRUE or FALSE (base case)
    RETURNS TRUE or FALSE, it is a base case

  b) NOT operation (unary operator and one operand[state formula])
  c) AND operation (binary operator and two operands[state formulas])
  d) OR  operation (binary operator and two operands[state formulas])
  e) E   opeartion (unary operator and the operand[state formula])
    RETURNS the operation name and the corresponding formula(s) for b,c,d,e

  f) P operation (unary operator and the operand[path formula])
    RETURNS the path operation and state formula recieved by 
    CALLING 'sldl_detect_path()' with the path formula

3 detecting the path operation in the path formula using 'sldl_detect_path()' which could be
  a) X_a   operation (unary operator and one operand[state formula] and a auxiliary formula 'a')
  b) X_tau operation (unary operator and one operand[state formula] and 'tau')
  c) U     operation (binary operator and two operand[state formulas])
  d) U_x   operation (binary operator and two operands[state formulas] and a auxiliary formula 'X') 
  e) r_U   operation (binary operator and two operands[state formulas] and the number of steps 'r')
  f) r_U_x operation (binary operator and two operands[state formulas] and the number of steps 'r' and auxiliary formula 'X')
    RETURNS the operation and the nescessary operands steps and the auxiliary formula

"""

def sldl_detect_path(formula,prob_initial):
  start_loc_path_formula = formula.find('[',3) #Extracring the path formula from the state formula
  psi = formula[start_loc_path_formula+1:-1] #this is the path formula without [] and () brackets,

  #The formula will be in the format X...
  if psi[0] == 'X':
    #The formula will be in the format X_tau(phi)
    if psi[2:5] == 'tau':
      new_phi = psi[5:]
      ret_tuple = ('X_tau',new_phi,prob_initial)
      return ret_tuple

    #The formula will be in the format X_(chi)(phi)
    else:
      a_open_loc = 2
      a_close_loc = closing_bracket_loc(psi,a_open_loc)
      a = psi[a_open_loc:a_close_loc+1]
      new_phi = psi[a_close_loc+1:]
      ret_tuple = ('X_a',a,new_phi,prob_initial)
      return ret_tuple

  #The formula will be in the format ... U ... having one of the folloging operators (U,U_a,r_U,r_U_x)
  else:

    #extracting the common part (phi1)_(chi1)... for the operators U , U_a , r_U , r_U_x
    phi1_open_loc = 0
    phi1_close_loc = closing_bracket_loc(psi,phi1_open_loc)
    bcef_open_loc = phi1_close_loc+2
    bcef_close_loc = closing_bracket_loc(psi,bcef_open_loc)
    is_U_loc = bcef_close_loc+1

    new_phi_1 = psi[phi1_open_loc:phi1_close_loc+1] #phi1
    bcef = psi[bcef_open_loc:bcef_close_loc+1] #chi1

    #the format of the formula will be (phi1)_(chi1)U(phi2) or (phi1)_(chi1)U_(chi2)(phi2)
    if psi[is_U_loc] == 'U':

      #The formula will be in the format (phi1)_(chi1) U (phi2)
      if psi[is_U_loc+1] == '(':
        new_phi_2 = psi[is_U_loc+1:]
        ret_tuple = ('U',new_phi_1,bcef,new_phi_2,prob_initial)
        return ret_tuple

      #The formula will be in the format (phi1)_(chi1) U_(chi2) (phi2)
      elif psi[is_U_loc+1] == '_':
        d_open_loc = is_U_loc+2
        d_close_loc = closing_bracket_loc(psi,d_open_loc)
        phi2_open_loc = d_close_loc+1

        d = psi[d_open_loc:d_close_loc+1] #chi2
        new_phi_2 = psi[phi2_open_loc:] #phi2

        ret_tuple = ('U_x',new_phi_1,bcef,d,new_phi_2,prob_initial) 
        return ret_tuple

    #the format of the formula will be (phi1)_(chi1)r_U(phi2) or (phi1)_(chi1)r_U_(chi2)(phi2)
    else:

      #extracting common the r_ part
      is_rU_loc = psi.find('U',is_U_loc)
      reward = psi[is_U_loc:is_rU_loc]

      if psi[is_rU_loc] == 'U':

        #The formula will be in the format (phi1)_(chi1)r_U(phi2)
        if psi[is_rU_loc+1] == '(':
          new_phi_2 = psi[is_rU_loc+1:] #phi2
          
          ret_tuple = ('r_U',new_phi_1,bcef,reward,new_phi_2,prob_initial)
          return ret_tuple

        #The formula will be in the format (phi1)_(chi1)r_U_(chi2)(phi2)
        elif psi[is_rU_loc+1] == '_':
          g_open_loc = is_rU_loc+2
          g_close_loc = closing_bracket_loc(psi,g_open_loc)
          phi2_open_loc = g_close_loc+1

          g = psi[g_open_loc:g_close_loc+1] #chi2
          new_phi_2 = psi[phi2_open_loc:] #phi2

          ret_tuple = ('r_U_x',new_phi_1,bcef,reward,g,new_phi_2,prob_initial)
          return ret_tuple

#this function detects the operator on the state formula, also detects if not a state formula, and returns the appropiate components of the formula
def sldl_detect_state(formula): #recieves a formula with trimmed ()
  
  #the formula will be of the syntax !(phi)
  if formula[0] == '!':
    new_phi = formula[1:] #the operand against the NOT operator. This phi is enclosed with () brackets
    ret_tuple = ('!',new_phi)
    return ret_tuple

  #The formula will be in the format (phi1)&(phi2) or (phi1)|(phi2)
  elif formula[0] == '(': 
    phi1_close_loc = closing_bracket_loc(formula,0)
    operator_loc = phi1_close_loc+1 #location of &

    new_phi_1 = formula[:operator_loc] #phi1
    new_phi_2 = formula[operator_loc+1:]  #phi2

    if(formula[operator_loc] == '&'):
      ret_tuple = ('&',new_phi_1,new_phi_2)

    elif(formula[operator_loc] == '|'):
      ret_tuple = ('|',new_phi_1,new_phi_2)

    return ret_tuple

  #The formula will be in the format E...[(phi)]
  elif formula[0] == 'E':
    phi_start_loc = formula.find('[')+1
    reward = formula[1:phi_start_loc-1]

    new_phi = formula[phi_start_loc : -1] #phi, state formula

    ret_tuple = ('E',reward,new_phi)
    return ret_tuple

  #The formula will be in the format P...[(psi)]
  elif formula[0] == 'P':
    start_loc_path_formula = formula.find('[',3)
    prob_initial = formula[:start_loc_path_formula] #captures the P=? or P>0.5 or P>=0.5 . . .

    return sldl_detect_path(formula,prob_initial) #calls path formula needs to be detected for the formula
  
  else:
    return formula #base case assuming the user has input a correct formula with 'true' or 'false'

#This function does the embedding depending upon the operation and calls recusively until base case
def sldlr(formula):
  new_formula = formula[1:-1] #eleminates the outermost bracket (phi) to phi
  operation = sldl_detect_state(new_formula) #operation[0] will contain the operation

  if operation[0] == '!':
    ret = str(sldlr(operation[1]))
    return '(!'+ret+')' #logic embedding from https://dl.acm.org/doi/pdf/10.1145/3696431

  elif operation[0] == '&':
    ret1 = str(sldlr(operation[1])) #recursive call with phi1
    ret2 = str(sldlr(operation[2])) #recursive call with phi2
    return '('+ret1+'&'+ret2+')'    #logic embedding from https://dl.acm.org/doi/pdf/10.1145/3696431

  elif operation[0] == '|':
    #print('or found')
    ret1 = str(sldlr(operation[1])) #recursive call with phi1
    ret2 = str(sldlr(operation[2])) #recursive call with phi2
    return '(!((!('+ret1+'))&(!('+ret2+'))))' #derived from and operator

  elif operation[0] == 'E':
    ret = str(sldlr(operation[2])) #recursive call with the state formula phi
    return '(R'+operation[1]+'[F ('+ret+'&\"bot\")])' #logic embedding from https://dl.acm.org/doi/pdf/10.1145/3696431
            #E has been changed to R since PRISM and STORM accepts R for reward formula
            #it also appends 'F'(eventually) which is not mentioned in the embedding paper, this is due to the syntax of STORM and PRISM where the reward formula are written in the format R=?[F phi]

  elif operation[0] == 'X_a':
    a = operation[1]  #auxiliary formula attached with NEXT operator
    ret = str(sldlr(operation[2]))  #recursive call with the phi
    initial = operation[3]  #represents P=? or P>0.5 or P>=0.5 or P<0.5 or P<=0.5  
    return '('+initial + "[X(!(\"bot\")&"+a+"&P>=1[X(\"bot\"&"+ret+")])])"

  elif operation[0] == 'X_tau':
    ret = str(sldlr(operation[1]))  #recursive call with phi
    initial = operation[2]  #represents P=? or P>0.5 or P>=0.5 or P<0.5 or P<=0.5  
    return "(\"bot\"&"+initial+"[X(\"bot\"&"+ret+")])"

  elif operation[0] == 'U':
    ret1 = str(sldlr(operation[1])) #recursive call with the phi1
    b = operation[2]  #auxiliary formula attached with phi1 ref. sec 8.3 https://dl.acm.org/doi/pdf/10.1145/3696431
    ret2 = str(sldlr(operation[3])) #recursive call with the phi2
    initial = operation[4]  #represents P=? or P>0.5 or P>=0.5 or P<0.5 or P<=0.5  
    return '('+initial+"[((\"bot\"&"+ret1+")|(!(\"bot\")&"+b+"))U(\"bot\"&"+ret2+")])"

  elif operation[0] == 'U_x':
    ret1 = str(sldlr(operation[1])) #recursive call with the phi1
    c = operation[2]  #auxiliary formula attached with phi1
    d = operation[3]  #auxiliary formula attached UNTIL operator ref. https://rdcu.be/ejoD5
    ret2 = str(sldlr(operation[4])) #recursive call with the phi2
    initial = operation[5]  #represents P=? or P>0.5 or P>=0.5 or P<0.5 or P<=0.5
    return '('+initial+"[((\"bot\"&"+ret1+")|(!(\"bot\")&"+c+"))U((!(\"bot\")&"+d+")&P>=1[X(\"bot\"&"+ret2+")])])"

  elif operation[0] == 'r_U':
    ret1 = str(sldlr(operation[1])) #recursive call with the phi1
    ret2 = str(sldlr(operation[4])) #recursive call with the phi2
    initial = operation[5]  #represents P=? or P>0.5 or P>=0.5 or P<0.5 or P<=0.5
    #operation[2] is auxiliary formula attached with phi1
    #operation[3] is the number of steps of bounded UNTIL
    return '('+initial+'(((\"bot\"&'+ret1+')|(!(\"bot\")&'+operation[2]+'))'+operation[3]+'U(\"bot\"&'+ret2+')))'

  elif operation[0] == 'r_U_x':
    ret1 = str(sldlr(operation[1])) #recursive call with the phi1
    ret2 = str(sldlr(operation[5])) #recursive call with the phi2
    f = operation[2]  #auxiliary formula attached with phi1
    reward = operation[3] #number of steps of bounded UNTIL
    g = operation[4]  #auxiliary formula attached with UNTIL
    initial = operation[6]  #represents P=? or P>0.5 or P>=0.5 or P<0.5 or P<=0.5  
    return '('+initial+'[((\"bot\"&'+ret1+')|(!(\"bot\")&'+f+')]'+reward+'U((!(\"bot\")&'+g+')&P>=1[X(\"bot\"&'+ret2+')])))'

  else:
    return formula










"""
APCTL* TO PCTL*

GRAMMAR of APRCTL and APCTL (APCTL is a subcase of APRCTL) (https://dl.acm.org/doi/pdf/10.1145/3696431)

FUNCTION DETAILS
1 upon recieving the input formula in 'sldl_state()' function, it first detects the state operation
  RECIEVES the operation and the formula(s) and calls itself recursievely until base case is reached, by performing nescessary operations of embedding

2 during the detection of the state formulas, i might go to the path formula(if there is a path formula) and throught 'sldl_path()' which call itsel recursively until it reaches to a state formula. because path formula do not have a terminal. ref. sec 6.2 https://dl.acm.org/doi/pdf/10.1145/3696431

3 detecting the operation in the state formula using 'sldl_detect_state_operation()' which could be
  a) no operation that is TRUE or FALSE (base case)
    RETURNS TRUE or FALSE, it is a base case

  b) NOT operation (unary operator and one operand[state formula])
  c) AND operation (binary operator and two operands[state formulas])
  d) OR  operation (binary operator and two operands[state formulas])
    RETURNS the operation name and the corresponding formula(s) for b,c,d

  e) P operation (unary operator and the operand[path formula])
    RETURNS the path operation and state formula recieved by 
    CALLING 'sldl_detect_path()' with the path formula

4 detecting the path operation in the path formula using 'sldl_detect_path_operation()' which could be
  a) X_a  operation (unary operator and one operand[path formula] and a auxiliary formula 'a')
  b) X    operation (unary operator and one operand[path formula] and 'tau')
  c) U    operation (binary operator and two operand[path formulas])
  d) NOT  operation (unary operator and one operand[path formula]
  e) AND  operation (binary operator and two operand[path formulas])
  f) OR   operation (binary operator and two operand[path formulas])
  g) state_formula it it not a path operation anymore ans it is a state formula sol 'sldl_path()' calls 'sldl_state()'
    RETURNS the operation and the nescessary operand's location if the operaiton is a binary operation

"""



def sldl_detect_state_operation(formula): 
  #The formula will be in the format !(phi)
  if formula[0] == '!':
    return '!'
  
  #The formula will be in the format (phi)&(phi)
  elif formula[0] == '(':
    close_loc = closing_bracket_loc(formula,0)
    operator_loc = close_loc+1

    if formula[operator_loc] == '&':
      return  '&',operator_loc

    elif formula[operator_loc] == '|':
      return  '|',operator_loc
  
  #the formula will be in the format P...[(psi)]
  elif formula[0] == 'P':
    loc_of_path_formula = formula.find('[',3)+1 
    return 'P'
  
  else:
    return formula #base case assuming the user has input a correct formula with 'true' or 'false'


def sldl_detect_path_operation(formula): #This formula contains no brackets on the sides it's psi
  #the formula will be in the format !(psi)
  if formula[0] == '!':
    return '!'
  
  #the formula will be in the format (psi)&(psi) or (psi)U(psi)
  elif formula[0] == '(':
    close_loc = closing_bracket_loc(formula,0)
    operator_loc = close_loc+1
    
    #the formula will be in the format (psi)&(psi)
    if formula[operator_loc] == '&':
      return  '&',operator_loc

    #the formula will be in the format (psi)|(psi)
    elif formula[operator_loc] == '|':
      return  '|',operator_loc
    
    #the formula will be in the format (psi)U(psi)
    elif formula[operator_loc] == 'U':
      return 'U',operator_loc
    
    else:
      return 'error'
  
  #the formula will be in the format X_a(psi) or X(psi)
  elif formula[0] == 'X':

    #the formula will be in the format X_a(psi)
    if formula[1] == '_':
      return 'X_a'

    #the formula will be in the format X(psi)
    elif formula[1] == '(':
      return 'X'
    
    else:
      return 'error'
  #the formula can be a state formula in two cases, if it is a 'true' or if it is a P=? . . .
  else:
    return 'state_formula'


def sldl_state(phi): #recieving a formula as input in (phi) format
  phi_trim = phi[1:-1]  #converting (phi) to phi
  operation = sldl_detect_state_operation(phi_trim)

  #the formula will be in the format !(phi)
  if operation[0] == '!':
    phi_new = phi_trim[1:] #(phi1)
    return '!'+str(sldl_state(phi_new)) #calling state formula

  #the formula will be in the format ()&()
  elif operation[0] == '&':

    #operation[1] has the location of the operator
    phi_new_1 = phi_trim[0:operation[1]] #(phi1)
    phi_new_2 = phi_trim[operation[1]+1:] #(phi1)
    ret_1 = sldl_state(phi_new_1) #calling state formula
    ret_2 = sldl_state(phi_new_2)

    return '(('+str(ret_1)+')&('+str(ret_2)+'))'

  elif operation[0] == '|':

    #operation[1] has the location of the operator
    phi_new_1 = phi_trim[0:operation[1]] #(phi1)
    phi_new_2 = phi_trim[operation[1]+1:] #(phi1)
    ret_1 = sldl_state(phi_new_1) #calling state formula
    ret_2 = sldl_state(phi_new_2)

    return '(!((!('+str(ret_1)+'))&(!('+str(ret_2)+'))))'

  #the formula will be in the format P...[(psi)]
  elif operation[0] == 'P':

    #extract the P_J part, which might be P=? or P>= or P> or P< or P<=
    initial_start_loc = 0
    initial_close_loc = phi_trim.find('[',3) 
    initial = phi_trim[initial_start_loc:initial_close_loc]

    Y = phi_trim[initial_close_loc+1:-1]   #(psi)
    
    return initial+'['+str(sldl_path(Y))+']' #sCALLING PATH FORMULA FUNCTION

  elif operation == 'error':
    print("This convertion expects a syntactically correct Logic.")


  else:
    return phi


def sldl_path(y): #recieves the formula as (psi)

  psi_trim = y[1:-1] #psi
  operation = sldl_detect_path_operation(psi_trim)

  #the formula will be in the format !(psi)
  if operation[0] == '!':
    psi_new = psi_trim[1:] #(psi)
    return '(!('+ str(sldl_path(psi_new))+'))'  #assumed the internal formula to be a path formula

  #the formula will be in the format (psi1)&(psi2)
  elif operation[0] == '&':
    psi_new_1 = psi_trim[:operation[1]] #(psi1)
    psi_new_2 = psi_trim[operation[1]+1:] #(psi2)
    
    return '(('+str(sldl_path(psi_new_1))+')&('+str(sldl_path(psi_new_2))+'))'

  #the formula will be in the format (psi1)|(psi2)
  elif operation[0] == '|':
    psi_new_1 = psi_trim[:operation[1]] #(psi1)
    psi_new_2 = psi_trim[operation[1]+1:] #(psi2)
    
    return '(!((!('+str(sldl_path(psi_new_1))+'))&(!('+str(sldl_path(psi_new_2))+'))))' #derived from AND operator using demorgans law

  #the formula will be in the format X(psi)
  elif operation == 'X':
    psi_new = psi_trim[1:]  #(psi)
    ret = sldl_path(psi_new)

    return '(X((\"bot\"&'+str(ret)+') | (!(\"bot\")&X('+str(ret)+'))))'

  #the formula will be in the format X_(chi)(psi)
  elif operation == 'X_a':
    a_open_loc = 2
    a_close_loc = closing_bracket_loc(psi_trim,a_open_loc)

    a = psi_trim[a_open_loc:a_close_loc+1] #(chi)

    psi_new = psi_trim[a_close_loc+1:]  #(psi)
    ret = sldl_path(psi_new)

    return '(X('+a+'&X('+str(ret)+')))'

  #the formula will of the format (psi1)U(psi2)
  elif operation[0] == 'U':
    open_loc_1 = 0
    close_loc_1 = closing_bracket_loc(psi_trim,0)
    open_loc_2 = close_loc_1+2

    psi_new_1 = psi_trim[open_loc_1:close_loc_1+1]  #(psi1)
    psi_new_2 = psi_trim[open_loc_2:] #(psi2)

    ret_1 = sldl_path(psi_new_1)
    ret_2 = sldl_path(psi_new_2)

    return '(!(\"bot\")|('+str(ret_1)+'))U(\"bot\"&'+str(ret_2)+')'

  #back to state
  elif operation == 'state_formula':
    return sldl_state(y) #moving from a path formula to the state formula with ()
















"STATE to ACTION Translators"





















"""P(R)CTL to AP(R)CTL Detailed working pattern aligns to the APCTL to PCTL"""

def aldl_detect_path(formula,prob_initial):
  start_loc_path_formula = formula.find('[',3) #location of the opening [ bracket of path formula
  psi = formula[start_loc_path_formula+1:-1] #this is the path formula without brackets, since we don't impose the brackets on a path formula

  #if the operator is X, check which X it is
  if psi[0] == 'X':
    new_phi = psi[1:]
    ret_tuple = ('X',new_phi,prob_initial)
    return ret_tuple

  #Now it's definetely U
  else:
    phi1_open_loc = 0
    phi1_close_loc = closing_bracket_loc(psi,phi1_open_loc)

    is_U_loc = phi1_close_loc+1

    new_phi_1 = psi[phi1_open_loc:phi1_close_loc+1]

    if psi[is_U_loc] == 'U':
      if psi[is_U_loc+1] == '(':
        new_phi_2 = psi[is_U_loc+1:]
        ret_tuple = ('U',new_phi_1,new_phi_2,prob_initial)
        return ret_tuple

    else:
      is_rU_loc = psi.find('U',is_U_loc)
      reward = psi[phi1_close_loc+1:is_rU_loc]
      new_phi_2 = psi[is_rU_loc+1:]
      ret_tuple = ('r_U',new_phi_1,reward,new_phi_2,prob_initial)

      return ret_tuple

def aldl_detect_state(formula): #recieves a formula with trimmed ()
  #detection of the state formula operator
  if formula[0] == '!':
    new_phi = formula[1:]
    ret_tuple = ('!',new_phi)
    return ret_tuple

  elif formula[0] == '(':
    phi1_close_loc = closing_bracket_loc(formula,0)
    operator_loc = phi1_close_loc+1

    new_phi_1 = formula[:operator_loc]
    new_phi_2 = formula[operator_loc+1:]

    if(formula[operator_loc] == '&'):
      ret_tuple = ('&',new_phi_1,new_phi_2)

    elif(formula[operator_loc] == '|'):
      ret_tuple = ('|',new_phi_1,new_phi_2)
    return ret_tuple

  elif formula[0] == 'R':
    phi_start_loc = formula.find('[')+1
    reward = formula[1:phi_start_loc-1]
    new_phi = formula[phi_start_loc : -1]

    ret_tuple = ('R',reward,new_phi)
    return ret_tuple

  #Detection of the path formula operator
  elif formula[0] == 'P':
    start_loc_path_formula = formula.find('[',3)
    prob_initial = formula[:start_loc_path_formula]

    return aldl_detect_path(formula,prob_initial)
  
  else:
    #print('sat state',formula)
    return formula



def aldlr(formula):
  new_formula = formula[1:-1]
  
  operation = aldl_detect_state(new_formula)
  #print(operation)

  if operation[0] == '!':
    ret = str(aldlr(operation[1]))
    return '(!'+ret+')'

  elif operation[0] == '&':
    ret1 = str(aldlr(operation[1]))
    ret2 = str(aldlr(operation[2]))
    return '('+str(ret1)+'&'+str(ret2)+')'

  elif operation[0] == '|':
    ret1 = str(aldlr(operation[1]))
    ret2 = str(aldlr(operation[2]))
    return '(!((!('+str(ret1)+'))&(!('+str(ret2)+'))))'

  elif operation[0] == 'R':
  #if operation[0] == 'E':
    reward = operation[1]
    ret = str(aldlr(operation[2]))
    return '(E'+reward+'[('+ret+'&P_[1,1][X_(!(\"bot\"))(true))])'

  elif operation[0] == 'X':
    ret = str(aldlr(operation[1]))
    initial = operation[2]
    return '(P_[1,1][X_(!(\"bot\"))('+initial+'[(true)_(\"bot\")U('+ret+'&P_[1,1][X_(!(\"bot\"))(true)])))])'


  elif operation[0] == 'U':
    ret1 = str(aldlr(operation[1]))
    ret2 = str(aldlr(operation[2]))
    initial = operation[3]
    return '('+initial+'[(('+ret1+'&P_[1,1][X_(!(\"bot\"))(true)])|((P_(0,1][X_(\"bot\")(true)])|(P_(0,1][X_tau(true)])))_(true)U('+ret2+'&P_[1,1][X_(!(\"bot\"))(true)])])'


  elif operation[0] == 'r_U':
    ret1 = str(aldlr(operation[1]))
    reward = operation[2]
    ret2 = str(aldlr(operation[3]))
    initial = operation[4]
    return '('+initial+'[(('+ret1+'&P_[1,1][X_(!(\"bot\"))(true)])|((P_(0,1][X_(\"bot\")(true)])|(P_(0,1][X_tau(true)])))_(true)'+reward+'U('+ret2+'&P_[1,1][X_(!(\"bot\"))(true)])])'

  else:
    
    if operation =='true' or operation == 'false':
      return '('+new_formula+')'
    else:
      a = operation
      return '(P_[1,1][X_(('+a+')&!(\"bot\"))(true)])'








"""PCTLStar_to_APCTLStar Detailed working pattern aligns with the working of APCTL star to PCTL star"""



def aldl_detect_path_operation(formula): #This formula contains no brackets on the sides
  if formula[0] == '!':
    return '!'

  elif formula[0] == '(':
    close_loc = closing_bracket_loc(formula,0)
    operator_loc = close_loc+1

    if formula[operator_loc] == '&':
      return  '&',operator_loc

    elif formula[operator_loc] == '|':
      return  '|',operator_loc

    elif formula[operator_loc] == 'U':
      return 'U',operator_loc


  elif formula[0] == 'X':
      return 'X'

  else:
    return 'state_formula'



def aldl_detect_state_operation(formula): #This formula contains no brackets on the sides
  if formula[0] == '!':
    return '!'

  elif formula[0] == '(':
    phi_close_loc = closing_bracket_loc(formula,0)
    operator_loc = phi_close_loc+1
    
    if formula[operator_loc] == '&':
      return  '&',operator_loc

    elif formula[operator_loc] == '|':
      return  '|',operator_loc


  elif formula[0] == 'P':
    loc_of_path_formula = formula.find('[',3)+1 #it captures P=?[PSI] as well as P_[i,j][PSI]
    return 'P',loc_of_path_formula

  else:
    return formula

def aldl_path(y):
  psi_trim = y[1:len(y)-1]
  operation = aldl_detect_path_operation(psi_trim)
  #print("path :",operation)

  #CASE 1: if the operation is a not on a path/state formula
  if operation[0] == '!':
    psi_new = psi_trim[1:]
    ret = str(aldl_path(psi_new))
    return '(!'+ ret+')'  #consider the formula after ! to be a path formula

  #CASE 2: if the operation is & of two path/state formula
  elif operation[0] == '&':
    psi_new_1 = psi_trim[:operation[1]]
    psi_new_2 = psi_trim[operation[1]+1:]
    ret1 = str(aldl_path(psi_new_1))
    ret2 = str(aldl_path(psi_new_2))
    return '('+ret1+'&'+ret2+')'

  elif operation[0] == '|':
    psi_new_1 = psi_trim[:operation[1]]
    psi_new_2 = psi_trim[operation[1]+1:]
    ret1 = str(aldl_path(psi_new_1))
    ret2 = str(aldl_path(psi_new_2))
    return '(!((!('+ret1+'))&(!('+ret2+'))))'


  #CASE 3: if the operation is a X
  elif operation == 'X':
    psi_new = psi_trim[1:]
    ret = str(aldl_path(psi_new))
    return '(X_(!(\"bot\"))(X_(\"bot\")('+ret+')|X_tau('+ret+')))'

  #CASE 4: if the path formula has a U operator
  elif operation[0] == 'U':
    open_loc_1 = 0
    close_loc_1 = closing_bracket_loc(psi_trim,0)
    open_loc_2 = close_loc_1+2
    #close_loc_2 = EOS
    psi_new_1 = psi_trim[open_loc_1:close_loc_1+1]
    psi_new_2 = psi_trim[open_loc_2:]
    ret_1 = aldl_path(psi_new_1)
    ret_2 = aldl_path(psi_new_2)
    return '(!(\"bot\")|('+str(ret_1)+'))U(\"bot\"&'+str(ret_2)+')'

  #CASE 0: back to state
  elif operation == 'state_formula':
    return aldl_state(y) #moving from a path formula to the state formula with ()



def aldl_state(phi):
  phi_trim = phi[1:-1]
  operation = aldl_detect_state_operation(phi_trim)
  #print("state :",operation)
  #if the operation is not of a state formula
  if operation[0] == '!':
    phi_new = phi_trim[1:]
    ret = str(aldl_state(phi_new))
    return '(!'+ret+')'

  #if the operation is the and of two state formulas
  elif operation[0] == '&':
    phi_new_1 = phi_trim[0:operation[1]] #enclosed within brackets
    phi_new_2 = phi_trim[operation[1]+1:] #enclosed within brackets
    ret_1 = str(aldl_state(phi_new_1))
    ret_2 = str(aldl_state(phi_new_2))
    return '('+ret_1+'&'+ret_2+')'

  elif operation[0] == '|':
    phi_new_1 = phi_trim[0:operation[1]] #enclosed within brackets
    phi_new_2 = phi_trim[operation[1]+1:] #enclosed within brackets
    ret_1 = str(aldl_state(phi_new_1))
    ret_2 = str(aldl_state(phi_new_2))
    return '(!((!('+ret_1+'))&(!('+ret_2+'))))'

  #if the operator is the P
  elif operation[0] == 'P':
    #extract the P_J part, which might be P=? OR P_[i,j]
    initial_start_loc = 0
    initial_close_loc = phi_trim.find('[',3)-1 #3 for a reason
    initial = phi_trim[initial_start_loc:initial_close_loc+1]

    Y = phi_trim[initial_close_loc+2:-1]   #extract the psi from the state formula, enclosed with ()
    ret = str(aldl_path(Y))
    return '('+initial+'['+ret+'])' #switch from a state formula to a path formula

  else:
    if operation =='true' or operation == 'false':
      return '('+phi_trim+')'
    else:
      a = operation
      return '(P_[1,1][X_(('+a+')&!(\"bot\"))(true)])'








def main():
    if len(sys.argv) != 3:
        print("One of the two arguments is missing: Please select an appropiate logic_type")
        print("<APCTL|APCTLS|APRCTL|PCTL|PCTLS|PRCTL>")
        sys.exit(1)

    first_arg = sys.argv[1]
    second_arg = sys.argv[2]

    mapping = {
        "APCTL": sldlr,
        "APCTLS": sldl_state,
        "APRCTL": sldlr,
        "PCTL": aldlr,
        "PCTLS": aldl_state,
        "PRCTL": aldlr
    }

    if first_arg in mapping:
        print(mapping[first_arg](second_arg))
    else:
        print(f"Unknown option: {first_arg}")
        print("Enter\nAPCTL\t if your input formula is Action PCTL\nAPCTLS\t if your input formula is Action PCTL*\nAPRCTL\t if your input formula is Action PCTL with rewards\nPCTL\t if your input formula is State PCTL\nPCTLS\t if your input formula is State PCTL*\nPRCTL\t if your input formula is State PCTL with rewards\n")
        sys.exit(1)

if __name__ == "__main__":
    main()

