import random
import string
from Toolbox import Keyboard
import numpy as np
from Enigma import Enigma_I
import pandas as pd


alphabet = string.ascii_uppercase

def ciphertextGen(filename,Enigma_machine):
    condition = True
    permutation_table = np.empty((26,3),dtype=str)
    count = 0

    while count<26*3:

        #this section generates the key first
        key = [random.randint(0,25) for _ in range(3)]
        key = ''.join([alphabet[i] for i in key])
        key = key*2
        key = Enigma_machine.enc_dec(key)

        for i in range(3):
            location = Keyboard.forward(Keyboard,key[i])
            if len(permutation_table[location,i])==0:
                permutation_table[location,i]=key[i+3]
                count+=1
        Enigma_machine.reset()

    pd.DataFrame(permutation_table).to_csv(filename,header=['1','2','3'])