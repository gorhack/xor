'''
Code Author: Main:gorhack
		sub:aubinh

Concept of xormath Author: aubinh

Concept: Xor encryption is a simple encryption that takes the "difference" between bits.
using xor encryption requres a message and a key. If you are decrypting, you need to find the key in order to
decrypt the message. This method looks for known file signature headers and xor's them with the encrypted
text. This then creates a key. Using this key you are able to decrypt the  rest of the file.

The reason this works so well is due to the fact of XORd data not changing the "difference" between bytes
meaning: If you have x45 and x47, then xor them with a random key, they will always be x02 apart. This code
looks for those differences of file signatures. Then determines the key.

'''

'''
as of now this only does a one byte key, in order to increase the byte comparison/key you need to offset the pdf and pdftrailer by
+1. that way you can compare the starting bytes of each message part with eachother




'''

from decimal import *

#as of now you have to hand input all file signatures into a hex format
array = [int("0x25",16),int("0x50",16),int("0x44",16),int("0x46",16)]
arraytrailer = [int("0x25",16),int("0x25",16),int("0x45",16),int("0x4f",16),int("0x46",16)]
endvar = 0
beginvar = 0
keyvar = ''
actualKey = False
pdf = []
for i in range(0,len(array)-1):
	pdf.append(array[i]^array[i+1])
#debug print statement for us to be able to make sure its been XORd
print(pdf)
pdftrailer = []
for i in range(0,len(arraytrailer)-1):
	pdftrailer.append(arraytrailer[i]^arraytrailer[i+1])
#debug print statement for us to be able to make sure its been XORd
print(pdftrailer)

#opens the hexdump file that is only the hex without the offsets or the text representation
hexdump = open("cuthexdump.txt",'r').read()
temp = hexdump.replace(" ","")
line = temp.replace("\n","")

#make shift check for keys
def checkForKey ():
	if key == keyvar: 
		print ("actual key")
		actualKey = True
	else: print("No encryption found for File type")

#creates 1 byte pairs of all the hex
n=2
cuthex = [line[i:i+n] for i in range(0, len(line), n)]
#This is where the real code happens, it only finds a header once it has gone through the a match for all
#		of the header differences
for i in range(0,len(cuthex)-3):
	if (int('0x' + cuthex[i],16))^(int('0x' + cuthex[i+1],16))==pdf[0]:
		if (int('0x' + cuthex[i+1],16))^(int('0x' + cuthex[i+2],16))==pdf[1]:
			if (int('0x' + cuthex[i+2],16))^(int('0x' + cuthex[i+3],16))==pdf[2]:
				key = str(array[0]^(int('0x' + cuthex[i],16))) + str(array[1]^(int('0x' + cuthex[i+1],16))) + str(array[2]^(int('0x' + cuthex[i+2],16))) + str(array[3]^(int('0x' + cuthex[i+3],16)))
				print("FOUND BEGIN Key in Decimal: " + str(key))
				beginvar=i
#stopping point for decryption
for i in range(0,len(cuthex)-3):
	if (int('0x' + cuthex[i],16))^(int('0x' + cuthex[i+1],16))==pdftrailer[0]:
		if (int('0x' + cuthex[i+1],16))^(int('0x' + cuthex[i+2],16))==pdftrailer[1]:
			if (int('0x' + cuthex[i+2],16))^(int('0x' + cuthex[i+3],16))==pdftrailer[2]:
				keyvar = str(arraytrailer[0]^(int('0x' + cuthex[i],16))) + str(arraytrailer[1]^(int('0x' + cuthex[i+1],16))) + str(arraytrailer[2]^(int('0x' + cuthex[i+2],16))) + str(arraytrailer[3]^(int('0x' + cuthex[i+3],16)))
				print("FOUND END: " + str(Decimal(keyvar)))
				endvar = i
				checkForKey()

#takes the known i location of the file header, and turns it into the key for decrpytion 
decrypt=[]
g = 0
if actualKey:
	for i in range(beginvar,endvar + 5):
		cuthex[i] = int('0x' + cuthex[i],16)
		#decrypts the rest of the text
		decrypt.append(hex(cuthex[i]^int('0x' + key,16)))
		if int(decrypt[g],16) < int('0x16',16):
			decrypt[g] = '0' + decrypt[g]
		g += 1
	unencryptedhex = "".join(str(x) for x in decrypt).replace("0x",'')
	print (pdf)
	m=4
	open("decrypted.txt","w").write(" ".join(unencryptedhex[i:i+m] for i in range(0, len(unencryptedhex), m)))























