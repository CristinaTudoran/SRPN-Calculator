import operator

#The two variables below represent the maximum and minimum values which can be stored in a variable
min_value=-2147483648
max_value=2147483647

#Set an empty stack where user inputs will be stored
stack=[]

"""
The below dictionary includes all mathematical operators used in the SRPN calculator and 
their respective Python operations 
"""
math_operators={'+':operator.add, '-':operator.sub, '*':operator.mul,
                '/':operator.floordiv, '%':operator.mod, '^':operator.pow}

#The below list includes all special operators used in the SRPN calculator
special_operators=['=', 'd', 'r', " "]

"""
This function checks if the user input is an integer. 
It addresses the scenario when inputs like '-52' need to be accepted as they are negative integers. However, a 'Stack overflow' error is returned by SRPN for inputs like '+52'
"""
def check_ifNumber(item):
  if item[0]=='+':
    return False
  else:
    try:
      item=int(item)
      return True
    except ValueError:
      return False

"""
The function below processes user inputs which are neither an integer nor a valid operator.
Used continue as suggested on the page below: https://stackoverflow.com/questions/43593219/next-item-in-a-list-if-condition-met
"""
def process_lineInput(item):
  count_num=0
  st="" #placeholder for operands 
  op=[]
  math_op=[]
  comment_count=0
  for i in range(0, len(item)):
    if item[i]=="#":
      comment_count=comment_count+1
      continue
    elif comment_count%2==1:
      continue
    else:
      if check_ifNumber(item[i])==True:
        st=st+item[i]
        if i==len(item)-1:
          process_input(st)
          count_num=count_num+1
      elif item[i] in math_operators or item[i] in special_operators:
        if st!="":
          process_input(st)
          count_num=count_num+1
          st=""
        op.append(item[i])
      else:
          if st!="":
            process_input(st)
            count_num=count_num+1
            st="" 
          character='"'+item[i]+'".'
          print("Unrecognised operator or operand", character.strip())

  for i in range(0, len(op)):
    if op[i] in math_operators:
      math_op.append(op[i])
  if ((stack) or comment_count%2!=0) and len(stack)<=len(math_op):
    print("Stack underflow.")
    op.remove(math_op.pop())
  for i in range(0, len(op)):
    if op[i]==" ":
      continue
    else:
      process_input(op[i])

"""
The function below checks if the element to be added to the stack is within the saturation levels. 
"""
def check_saturation(item):  

  if item<min_value:
    stack.append(min_value)
  elif item>max_value:
    stack.append(max_value)
  else:
    stack.append(item)
"""
The function below returns the last 2 items in the stack as a tuple
"""
def get_operands():
  x=stack.pop()
  y=stack.pop()
  return x, y

"""
The function processes the user input:
1. If the input is a number, it is added to the stack
2. If the input is a mathematical operator, its coresponding mathematical operation is performed between the last two items of the stack
3. If the input is a special operator, its coresponding command is performed
"""
def process_input(item):
  if item in math_operators:
    operands=get_operands()
    if operands[0]==0 and item=="/":
      print("Divided by 0.")
      stack.append(operands[1])
      stack.append(operands[0])
    else:    
      result=math_operators[item](operands[1], operands[0])
      check_saturation(result)
  elif item=="=":
    if not stack:
      print ("Stack empty.")
    else:
      print(stack[-1])
  elif item=="d":
    if not stack:
      print(min_value)
    else:
      print(*stack, sep = "\n")
  else:
    check_saturation(int(item))

#the calculator starts running 
print("You can now start interacting with the SRPN calculator")
operator_count=0
operand_count=0
comment_count=0

while True:
  user_input=input()
  if user_input=="#":
    comment_count=comment_count+1
    while comment_count%2==1:
      user_input=input()
      if user_input=="#":
        comment_count=comment_count+1
  else:
    if check_ifNumber(user_input)==True:
      operand_count=operand_count+1 
      process_input(user_input)
    elif user_input in math_operators:
      operator_count=operator_count+1
      if operand_count<=operator_count:
        print("Stack underflow.")
      else:
        process_input(user_input)   
    elif user_input in special_operators: 
      process_input(user_input)  
    else:
      process_lineInput(user_input)  
  