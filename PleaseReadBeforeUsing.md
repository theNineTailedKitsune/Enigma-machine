# Enigma-machine
Enigma Machine used during WWII for encryption and decryption of messages by German forces. included models:  -  Enigma I (separated from M3 Army and M3 Navy models with different sets of rotors(for user convenience)) - Commercial A and B, Swiss K (still not manufactured)- German Railway (Rocket) (still not manufactured) - M4 Navy (Shark).

### a walkthrough the files and how to properly run the code:
  Toolbox.py: includes all the components of Enigma.
  Enigma.py: the Enigma library, includes the model classes and functions related to them
  playfair.py: a replacement for the bigram tables in Navy protocol since building one from scratch is unecessary and time consuming
  Loop_dict_generator.py: this file generates the catalog for the loop lengths used by Bomba. 
                          NOTE: this section is computationally heavy and must not be rerun unless your device can support it.
                          the csv file 'enigma_signatures.csv' is the catalog and this is just for reference
  messageGen.py: python file in charge of simulating the data the codebreakers used. 
                 creates the file 'keys.csv' which consists of a few number of keys, encrypted by enigma
  Enigma_Attack.py: since the details about the elimination process done by Bomba were rather vague, 
                    I used the 6*26*26*26 catalog to look through and find the right settings. the plugboard setting can be found from there

### how to use the code
to encrypt/decrypt messages, the Enigma.py file can be run directly, replace line 325 with your desired plaintext and line 
326 with your desired settings and recieve the ciphertext

to try an attack on a setting, you can try by running messageGen, replacing line 33 with your desired settings.
then, run Enigma attack and watch the process unfold


SideNote: my sincere apologies for my user unfriendly Enigma, a few technical issues and a few failed attempts here and there,
and I lost half my files and had to retry. this repo will be a work in progress, but for the meantime, please enjoy the code

-best regards, Yasini


