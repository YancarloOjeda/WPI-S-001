"""
Walden Modular Equipment SAS
Python-Spyder
2020
"""

#This is a comment
#Comments are not compiled by the program
#Use the symbol # o (ctrl + 1) to write a comment

#Use print to display a string in the console - print('string')
print('Hello Walden')

#Use the symbol = to assign a value to a variable
Var_1 = 10
Var_2 = 5

#You can do operations with the variables
Result  = Var_1 / Var_2
print(Result)

#Use if and esle to compare variables
#Try to change the value of the variables
if (Var_1 > Var_2):
    print('Var_1 is greater than Var_2')
else:
    print('Var_1 is less than Var_2')
    
#Try use other operators, ==, !=, <, <=, >, >=
if (Var_1 != Var_1):
    print('Result one')
else:
    print('Result two')
    
#try using conditional operators to compare variables
# and(&), or(|)
Var_1 = 10
Var_2 = 20
Var_3 = 30
if (Var_1 < Var_2) & (Var_2 < Var_3):
    print('Result one')
else:
    print('Result two')

#Using While loop the code will iterate as long as the condition is true
#NOTE: It is important to respect the tabulations
i = 0
End = 10
while(i<=End):
    print(i)
    i = i + 1
    
#Using For loop the code will iterate a finite number of times
for i in range(0, 10):
    print(i)
