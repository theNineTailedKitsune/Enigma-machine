import Toolbox as tb
import pandas as pd
import numpy as np
import random as rand


'''
check for entry wheel details
and the models that can use one
type of entry wheel and replacability
'''

rotors = pd.read_csv('rotors.txt', sep=',',index_col=None, header=None, 
names=['rotor_number','rotor_setting','model', 'notch','rotor_count'])
reflectors = pd.read_csv('reflectors.txt', sep=',', index_col=None, header=None,
names=['reflector', 'reflector_setting'])
match= pd.read_csv('match.txt', sep=',', index_col=None, header=None,
names=['model', 'reflector'])
date_keybook = pd.read_csv('date_keybook.txt', sep=',', index_col=None, header=None,
names=['month','key'])
operator_keybook=  pd.read_csv('operator_keybook.txt', sep=',', index_col=None, header=None).to_numpy()

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Enigma:

    
    def __init__(self, steckerbrett, rotor_I, rotor_II, rotor_III, reflector, possible_rotors_from, model, key='AAA'):

        rotor_I_setting=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor_I)]['rotor_setting'].iloc[0]
        notch_I=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor_I)]['notch'].iloc[0]
        rotor_II_setting=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor_II)]['rotor_setting'].iloc[0]
        notch_II=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor_II)]['notch'].iloc[0]
        rotor_III_setting=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor_III)]['rotor_setting'].iloc[0]
        notch_III=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor_III)]['notch'].iloc[0]
        if not pd.isna(match.loc[(match['model']== model) & (match['reflector'] == reflector)])['reflector'].iloc[0]:
            reflector=reflectors.loc[reflectors['reflector']==reflector]['reflector_setting'].iloc[0]

        self.model = model
        self.key = key
        self.entry_wheel = tb.Rotor('QWERTZUIOASDFGHJKPYXCVBNML')
        self.fast = tb.Rotor(rotor_I_setting , notch = notch_I)
        self.medium = tb.Rotor(rotor_II_setting , notch = notch_II)
        self.slow = tb.Rotor(rotor_III_setting , notch = notch_III)
        self.reflector= tb.Reflector(reflector)
        self.steckerbrett = tb.Steckerbrett(steckerbrett)
        left = self.steckerbrett.left
        right = self.steckerbrett.right
        self.reset()

        if self.verify_key(3):
            self.slow.rotate_to_letter(self.key[0])
            self.medium.rotate_to_letter(self.key[1])
            self.fast.rotate_to_letter(self.key[2])


    def enc_dec(self,plaintext):
        ciphertext = []
        for i in plaintext:
            signal = tb.Keyboard.forward(tb.Keyboard, i)
            signal = self.steckerbrett.forward(signal)
            signal,_ = self.entry_wheel.forward(signal)
            signal, notch_I = self.fast.forward(signal)
            signal, notch_II=self.medium.forward(signal)
            signal, _=self.slow.forward(signal)
            signal = self.reflector.forward(signal)
            signal = self.slow.backward(signal)
            signal = self.medium.backward(signal)
            signal = self.fast.backward(signal)
            signal = self.entry_wheel.backward(signal)
            signal = self.steckerbrett.backward(signal)
            letter = tb.Keyboard.backward( tb.Keyboard,signal)
            ciphertext.append(letter)


            self.fast.rotate()
            if notch_I:
                self.medium.rotate()
            if notch_II:
                self.slow.rotate()

        return ''.join(ciphertext)
            
    def reset(self):  
            self.slow.rotate_to_letter(self.key[2])
            self.medium.rotate_to_letter(self.key[1])
            self.fast.rotate_to_letter(self.key[0])
    
    def verify_key(self, key_length):
        if (type(self.key)== str) & len(self.key) == key_length:
            return True
        return False
    
    def set_rotors(self,rotor,possible_rotors_from):
        rotor_I_setting=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor[0])]['rotor_setting'].iloc[0]
        notch_I=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor[0])]['notch'].iloc[0]
        rotor_II_setting=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor[1])]['rotor_setting'].iloc[0]
        notch_II=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor[1])]['notch'].iloc[0]
        rotor_III_setting=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor[2])]['rotor_setting'].iloc[0]
        notch_III=rotors.loc[(rotors['model'].isin(possible_rotors_from)) &(rotors['rotor_number']==rotor[2])]['notch'].iloc[0]

        self.fast = tb.Rotor(rotor_I_setting , notch = notch_I)
        self.medium = tb.Rotor(rotor_II_setting , notch = notch_II)
        self.slow = tb.Rotor(rotor_III_setting , notch = notch_III)


    def set_reflector(self,reflector):
        if not pd.isna(match.loc[(match['model']== self.model) & (match['reflector'] == reflector)])['reflector'].iloc[0]:
            reflector=reflectors.loc[reflectors['reflector']==reflector]['reflector_setting'].iloc[0]
            self.reflector= tb.Reflector(reflector)
            
    def set_key(self,key):
        self.key = key
        self.reset()

    def go_to_position(self, number):
        self.enc_dec('A'*number)


#complete
class Enigma_I(Enigma):


    def __init__(self, steckerbrett, rotor_I, rotor_II, rotor_III, reflector, key='AAA'):
        super().__init__(steckerbrett, rotor_I, rotor_II, rotor_III, reflector, possible_rotors_from=['Enigma_I'], model='Enigma_I', key = key)

    def enc_dec(self, plaintext):
        return super().enc_dec(plaintext)
    
    def reset(self):
        return super().reset()
    
    def set_rotors(self, rotor):
        super().set_rotors(rotor, ['Enigma_I'])

    def set_reflector(self, reflector):
        return super().set_reflector(reflector)
    
    def set_key(self, key):
        return super().set_key(key)
    

#complete
class M3_Army(Enigma):


    def __init__(self, steckerbrett, rotor_I, rotor_II, rotor_III, reflector, month, day):
        super().__init__(steckerbrett, rotor_I, rotor_II, rotor_III, reflector, possible_rotors_from=['M3_Army','Enigma_I'], model='M3_Army')
        self.initial_key = self.set_key(month, day)


    def set_key(self, month, day):
        key = date_keybook.loc[date_keybook['month'] == month]['key'].iloc[day-1]
        return key


    def enc_dec(self, plaintext, mode=['enc','dec']):
        if mode == 'dec':
            key = plaintext[0:6]
            self.key = self.initial_key
            super().reset()
            key = super().enc_dec(key)
            if key[0:3]==key[3:6]:
                self.key = key[0:3]
                super().reset()
                text_A = super().enc_dec(plaintext[6:])
                return self.key + self.key + text_A
            else:
                self.key = key[0:3]
                super().reset()
                text_A = super().enc_dec(plaintext[6:])
                self.key = key[3:6]
                super().reset()
                text_B = super().enc_dec(plaintext[6:])
                return text_A,text_B
        elif mode == 'enc':
            key = plaintext[0:6]
            self.key = self.initial_key
            super().reset()
            key = super().enc_dec(key)
            self.key = plaintext[0:3]
            super().reset()
            return key + super().enc_dec(plaintext[6:])



class commercial_A_B(Enigma):


    def __init__(self, rotor_I, rotor_II, rotor_III, reflector):
        super().__init__([], rotor_I, rotor_II, rotor_III, reflector, key='A', possible_rotors_from=['Commercial_Enigma_A_B'], model='Commercial_Enigma_A_B')
        
    def enc_dec(self, plaintext):
        return super().enc_dec(plaintext)

    

#complete
class M3_Navy(Enigma):
    def __init__(self, steckerbrett, rotor_I, rotor_II, rotor_III, reflector, month, day):
        self.initial_key = date_keybook.loc[date_keybook['month'] == month]['key'].iloc[day-1]
        super().__init__(steckerbrett, rotor_I, rotor_II, rotor_III, reflector, possible_rotors_from=['Enigma_I','M3_Army','M3_Naval','M4_R2'], model='M3_Naval')

    def enc_dec(self, plaintext,mode=['enc','dec']):
        if mode == 'dec':
            key = plaintext[0:6]
            self.key = self.initial_key
            super().reset()
            key = super().enc_dec(key)
            if key[0:3]==key[3:6]:
                self.key = key[0:3]
                super().reset()
                text_A = super().enc_dec(plaintext[6:])
                return self.key + self.key + text_A
            else:
                self.key = key[0:3]
                super().reset()
                text_A = super().enc_dec(plaintext[6:])
                self.key = key[3:6]
                super().reset()
                text_B = super().enc_dec(plaintext[6:])
                return text_A,text_B
        elif mode == 'enc':
            key = plaintext[0:6]
            self.key = self.initial_key
            super().reset()
            key = super().enc_dec(key)
            self.key = plaintext[0:3]
            super().reset()
            return key + super().enc_dec(plaintext[6:])



#in Swiss-k, ETW is the steckerbrett's replacement and there is only one possible reflector
class Swiss_K(Enigma):
    def __init__(self, rotor_I, rotor_II, rotor_III, key='AAA'):
        super().__init__([], rotor_I, rotor_II, rotor_III,'UKW-K', possible_rotors_from=['Swiss_K'],model='Swiss_K',key=key)
        self.entry_wheel= tb.Entry_wheel()
        

        def enc_dec(self, plaintext):
            key = self.key + self.key
            key = self.entry_wheel.forward(key)
            key = super().enc_dec(key.upper)
            if key[:2]==key[3:]:
                self.key = key
                super().reset()
            return super().enc_dec(plaintext.upper())
        


class German_Railway(Swiss_K):
    def __init__(self, rotor_I, rotor_II, rotor_III):
        super().__init__([], rotor_I, rotor_II, rotor_III, 'UKW', possible_rotors_from=['German_Railway_(Rocket)'], model='German_Railway_(Rocket)',entry_wheel='ETW', key='AAA')

    def enc_dec(self, plaintext):
        return super().enc_dec(plaintext)


class M4_Navy(Enigma):
    def __init__(self, steckerbrett, rotor_I, rotor_II, rotor_III, rotor_IV, reflector, month, day, randoms='AA'):

        first = date_keybook.loc[date_keybook['month']==month]['key'].iloc[day-1]
        keybook = operator_keybook.shape
        self.key = operator_keybook[rand.randint(0,keybook[0]-1),rand.randint(0,keybook[1]-1)]
        enc_key = randoms[0]+ self.key[0] + first[0] + self.key[1] + first[1] + self.key[2] + first[2] + randoms[1]

        super().__init__(steckerbrett, rotor_I, rotor_II, rotor_III, reflector, possible_rotors_from=['Enigma_I','M3_Army','M4_Naval'], model='M4_Naval', key=self.key)

        rotor_IV = rotors.loc[(rotors['model'].isin('M4_R2')) &(rotors['rotor_number']==rotor_IV)]['rotor_setting'].iloc[0]
        self.thin, _ = tb.Rotor(rotor_IV)

        #the actual M4_Naval uses a bigram table to encode the key. it is heavy and pointless for me to write,
        #so I will use something resembling a playfair to implement this bigram
        self.bigram = np.array([["H","E","I","L","T"],
                            ["R","U","A","N","B"],
                            ["C","D","F","G","K"],
                            ["M","O","P","Q","S"],
                            ["V","W","X","Y","Z"]])
        
        enc_key = playfair.enc_dec(enc_key, self.bigram)
        self.key = enc_key[1] + enc_key[3] + enc_key[5]

        self.slow.rotate_to_letter(self.key[0])
        self.medium.rotate_to_letter(self.key[1])
        self.fast.rotate_to_letter(self.key[2])

    def key_setup(self, month, day, randoms):
        first = date_keybook.loc[date_keybook['month']==month]['key'].iloc[day-1]
        keybook = operator_keybook.shape
        second = operator_keybook[rand.randint(0,keybook[0]-1),rand.randint(0,keybook[1]-1)]
        enc_key = randoms[0]+ second[0] + first[0] + second[1] + first[1] + second[2] + first[2] + randoms[1]
        enc_key = playfair.enc_dec(enc_key, self.bigram)
        self.key = enc_key[1] + enc_key[3] + enc_key[5]

    def bigram_setup(bigram):
        if bigram.shape != (5,5):
            raise ValueError
        bgram = set()
        for i in bigram:
            for j in i:
                bgram.add(j)
        if len(bgram) != 25:
            raise IndexError

    def forward(self, letter):
        signal = tb.Keyboard.forward( tb.Keyboard,letter)
        signal = self.steckerbrett.forward(signal)
        signal, notch_signal = self.fast.forward(signal)
        self.fast.rotate()

        signal, notch_signal=self.medium.forward(signal, notch_signal=notch_signal)
        signal, _=self.slow.forward(signal)
        signal, _=self.thin.forward(signal)
        signal = self.reflector.forward(signal)

        return signal
    
    def backward(self, signal):
        signal = self.thin.backward(signal)
        return super().backward(signal)
    

plaintext = 'AAAAAA'
Enigma_machine = Enigma_I([],'II','III','I','Reflector_C', 'AAA')

Enigma_machine.reset()
ciphertext = Enigma_machine.enc_dec(plaintext)
Enigma_machine.reset()
print(ciphertext)
plaintext = Enigma_machine.enc_dec(ciphertext)
Enigma_machine.reset()
print(plaintext)
