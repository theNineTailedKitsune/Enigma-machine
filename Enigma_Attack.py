from Enigma import Enigma_I
import pandas as pd
import string
import operator

alphabet = string.ascii_uppercase

def positional_table_gen(Enigma_machine):
    Enigma_machine.reset()
    positional_table = []
    for letter in alphabet:
        Enigma_machine.reset()
        row = []
        for _ in range(6):
            row.append(Enigma_machine.enc_dec(letter))
        positional_table.append(row)
    
    return pd.DataFrame(positional_table, columns=['1','2','3','4','5','6'])
 

def align_positional_table(positional_table):
    signature = pd.DataFrame()
    for i in range(1,4):
        table  = positional_table[[str(i),str(i+3)]]
        table = table.sort_values(by=[str(i)])
        table.set_index(str(i),inplace=True)
        signature = pd.concat([signature, table], axis=1)
    return signature

def Enigma_sgn(filename, typefile=['csv','dataframe']):
    if typefile == 'csv':
        keys = pd.read_csv(filename,header=0,index_col=0)
        rng = 0
    elif typefile == 'dataframe':
        keys = filename
        rng = 3
    else:
        raise TypeError
    
    loop_list = []
    loop_str = []

    for align in range(1+rng,4+rng):
        remaining = list(alphabet)
        positional_table = keys[str(align)]
        mapping = {}

        for row in range(len(positional_table)):
            index = alphabet[row]
            mapping[index] = positional_table[row]

        loop_lengths = []
        loops = []

        while remaining:
            start = remaining[0]
            current = start
            loop_string = ''
            count = 0

            while current in remaining:
                remaining.remove(current)
                loop_string += current
                count += 1
                current = mapping.get(current)

                if current is None:
                    break

            if count > 0:
                loop_lengths.append(count)
                loops.append(loop_string)

        loop_list.append(sorted(loop_lengths))
        loop_str.append(loops)

    

    return loop_list, loop_str      

def translate(rotor):
    rotors = rotor.split(',')
    rotor = []
    for item in rotors:
        rotor.append(item.strip('\''))
    return rotor

def lcs_length(s, t):
    if not s or not t:
        return 0
    m, n = len(s), len(t)
    dp = [0] * n
    max_len = 0
    for i in range(m):
        prev = 0
        for j in range(n):
            temp = dp[j]
            if s[i] == t[j]:
                if j == 0:
                    dp[j] = 1
                else:
                    dp[j] = prev + 1
                if dp[j] > max_len:
                    max_len = dp[j]
            else:
                dp[j] = 0
            prev = temp
    return max_len

def max_alignment(string1, string2):
    if len(string1) == len(string2):
        max_align = 0
        length = len(string1)
        for position in range(length):
            aligning = 0
            for i in range(length):
                if string1[i]==string2[i]:
                    aligning +=1
            if aligning >= max_align:
                max_align = aligning
                alignment = position
            string2 = string2[length-1:]+string2[0:length-1]
        string2 = string2[alignment:]+string2[0:alignment]
        return alignment , max_align

def loop_match(loop1,loop2):
    mask = [0]*len(loop2)
    match_size = 0
    for i in range(len(loop1)):
        max_align = 0

        for j in range(len(loop2)):
            if len(loop1[i]) == len(loop2[j]):
                _ , alignment_size = max_alignment(loop1[i],loop2[j])

                if alignment_size >= max_align:
                    max_align = alignment_size
                    index = j


        match_size += (max_align**2)*0.1*len(loop1[i])
        mask[index] = 1

    return match_size

def Heuristic(signature , loop):

    scores = 0
    for i in range(3):
        match_size = loop_match(loop[i],signature[i])
        scores += match_size


    return scores

def Steckerbrett_setting(loops1,loops2):
    for loop in range(3):
        loop1

        
if __name__=='__main__':
    sgn_loops, loop_string = Enigma_sgn('keys.csv',typefile='csv')
    enigma_signatures = pd.read_csv('enigma_signatures.csv')
    matching_signatures=enigma_signatures.loc[(enigma_signatures['Signature1']==str(sgn_loops[0])) &
                                              (enigma_signatures['Signature2']==str(sgn_loops[1])) &
                                              (enigma_signatures['Signature3']==str(sgn_loops[2]))][['Rotor Order','Key']]
    print(matching_signatures)

    loop_strings = {}
    Enigma_machine = Enigma_I([],'II','I','III','Reflector_B')
    for row in range(matching_signatures.shape[0]):
        rotors = (matching_signatures.iloc[row]['Rotor Order'])
        rotors = translate(rotors)
        key = matching_signatures.iloc[row]['Key']

        Enigma_machine.set_rotors(rotors)
        Enigma_machine.set_key(key)

        positional_table = positional_table_gen(Enigma_machine)
        positional_table = align_positional_table(positional_table)
        _,matching_signature_str = Enigma_sgn(positional_table,typefile='dataframe')

        loop_strings[key] = matching_signature_str


    order = {}
    for key in loop_strings.keys():
        order[key] = Heuristic(loop_string,loop_strings[key])
        order = dict(sorted(order.items(), key=lambda item: item[1],reverse=True))
    print(order)



#TODO: match the longest shared substrings
#TODO: test the given function