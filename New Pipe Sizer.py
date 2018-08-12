
# coding: utf-8

# In[1]:


# import packages

import pandas as pd
import numpy as np
import math


# In[2]:


# read excel file

xls = pd.ExcelFile('Gas Pipe Sizing.xlsx')
df1 = pd.read_excel(xls, '402.4(1)')
df2 = pd.read_excel(xls, '402.4(2)')
df3 = pd.read_excel(xls, '402.4(3)')
df4 = pd.read_excel(xls, '402.4(4)')
df5 = pd.read_excel(xls, '402.4(5)')
df6 = pd.read_excel(xls, '402.4(6)')
df7 = pd.read_excel(xls, '402.4(7)')


# In[3]:


df7.head()


# In[4]:


# User Response Class
class Userinput(object):
    
    def __init__(self, material = '',gas = '', pressure = 0, loss = 0, length = 0):
        self.material = material    # pipe material attribute
        self.gas = gas              # gas attribute
        self.pressure = pressure    # pressure attribute
        self.loss = loss            # pressure loss attribute
        self.length = length        # length attribute
        
    def setMaterial(self, new_material):
        self.material = new_material
        
    def setGas(self, new_gas):
        self.gas = new_gas
        
    def setPressure(self, new_pressure):
        self.pressure = new_pressure
        
    def setLoss(self, new_loss):
        self.loss = new_loss
        
    def setLength(self, new_length):
        self.length = new_length


# In[5]:


# function that asks for system attributes
def askuser(user):
    
    while True:
        user.setMaterial(str(input("SCHEDULE 40 METALLIC PIPE or CSST? Enter 'Metallic' or 'CSST' ")).upper())
        if user.material == 'METALLIC' or user.material == 'CSST':
            break
        else:
            print('Input unrecognized. Please enter "Metallic" or "CSST" ')
        
    while True:
        user.setGas(str(input("Natural Gas or Propane? Enter 'Gas' or 'Propane'")).upper())
        if user.gas == 'GAS' or user.gas == 'PROPANE':
            break
        else:
            print('Input unrecognized. Please enter "Gas" or "Propane" ')
            
    user.setPressure(int(input("Gas pressure in PSI? Enter as an integer ")))
        
    if user.pressure < 2:
        while True:
            user.setLoss(float(input("Pressure loss in inches water column? Enter 0.3, 0.5, 3.0, or 27.7 ")))
            if user.loss == 0.3 or user.loss == 0.5 or user.loss == 3.0 or user.loss == 27.7:
                break
            else:
                print('Pressure loss not available for selected input pressure. Please enter 0.3, 0.5, 3.0, or 27.7 ')
    elif user.pressure == 2:
        user.setLoss(1.0)
        print('Pressure loss set to 1 PSI ')
    elif user.pressure == 3:
        user.setLoss(2.0)
        print('Pressure loss set to 2 PSI ')
    elif user.pressure == 5:
        user.setLoss(3.5)
        print('Pressure loss set to 3.5 PSI')
        
    user.setLength(int(input("Total max connected length in feet? ")))
    
    
    
    print ('\n')
    print ('User Parameters:')
    print ("Material: %s" %user.material)
    print ("Gas: %s" %user.gas)
    print ("Pressure: %s" %user.pressure)
    print ("Pressure loss: %s" %user.loss)
    print ("Total Length: %s" %user.length)


# In[6]:


# function that rounds up longest length
def lengthrounder(user):
    if user.length <=100:
        user.length = int(math.ceil(user.length / 10.0)) * 10
        return user.length
    elif user.length >100 and user.length <= 200:
        user.length = int(math.ceil(user.length / 25.0)) * 25
        return user.length
    elif user.length >200 and user.length <= 1000:
        user.length = int(math.ceil(user.length / 50.0)) * 50
        return user.length
    elif user.length >1000 and user.length <= 2000:
        user.length = int(math.ceil(user.length / 100.0)) * 100
        return user.length
    else:
        return "error or length too high"


# In[7]:


# function that filters dataframes based on pressure
def dfselect(user):
    df = [df1,df2,df3,df4,df5,df6,df7]
    if user.pressure < 2:
        if user.loss == 0.3:
            df = df[0]
        elif user.loss == 0.5:
            df = df[1]
        elif user.loss == 3.0:
            df = df[2]
        elif user.loss == 27.7:
            df = df[3]
    elif user.pressure == 2:
        df = df[4]
    elif user.pressure == 3:
        df = df[5]
    elif user.pressure == 5:
        df = df[6]
    return df


# In[8]:


# function that chooses the pipe size
def sizeselector(capacity, selectedrow):
    selectedrow = selectedrow <= capacity
    x = 0
    for key,value in selectedrow.iteritems():
        if value == True:
            x += 1
            pass
        else:
            return selectedrow.index[x]


# In[11]:


# the program that calls each function
def theprogram():
    user = Userinput()
    askuser(user)
    df = dfselect(user)    
    reallength = lengthrounder(user)
    selectedrow = df.loc[reallength]
    capacity = 0
    
    print('\n')
    
    while capacity != "exit":
        capacity = input("Capacity in CFH? Enter exit to stop ")
        if capacity != 'exit':
            capacity = int(capacity)
            print("Your pipe size in inches: %s" %(sizeselector(capacity, selectedrow)))
            print('\n')
        else: 
            pass


# In[10]:


theprogram()


# In[ ]:


"""
To do list:
1. add all other tables to the excel file
2. read the new tables
3. add new dataframes to selection functions
"""

