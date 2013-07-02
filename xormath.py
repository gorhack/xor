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

#as of now you have to hand input all file signatures into a hex format
array = [int("0x25",16),int("0x50",16),int("0x44",16),int("0x46",16)]
pdf = []
for i in range(0,len(array)-1):
	pdf.append(array[i]^array[i+1])
#debug print statement for us to be able to make sure its been XORd
print(pdf)

#opens the hexdump file that is only the hex without the offsets or the text representation
hexdump = open("cuthexdump.txt",'r').read()
temp = hexdump.replace(" ","")
line = temp.replace("\n","")

#creates 1 byte pairs of all the hex
n=2
cuthex = [line[i:i+n] for i in range(0, len(line), n)]
#This is where the real code happens, it only finds a header once it has gone through the a match for all
#		of the header differences
for i in range(0,len(cuthex)-3):
	if (int('0x' + cuthex[i],16))^(int('0x' + cuthex[i+1],16))==pdf[0]:
		if (int('0x' + cuthex[i+1],16))^(int('0x' + cuthex[i+2],16))==pdf[1]:
			if (int('0x' + cuthex[i+2],16))^(int('0x' + cuthex[i+3],16))==pdf[2]:
				print("FOUND XOR HEADER " + str(array[0]^(int('0x' + cuthex[i],16))) + str(array[1]^(int('0x' + cuthex[i+1],16))) + str(array[2]^(int('0x' + cuthex[i+2],16))) + str(array[3]^(int('0x' + cuthex[i+3],16))))
				key = str(array[0]^(int('0x' + cuthex[i],16))) + str(array[1]^(int('0x' + cuthex[i+1],16))) + str(array[2]^(int('0x' + cuthex[i+2],16))) + str(array[3]^(int('0x' + cuthex[i+3],16)))
#takes the known i location of the file header, and turns it into the key for decrpytion 
decrypt=[]
for i in range(0,len(cuthex)):
	cuthex[i] = int('0x' + cuthex[i],16)
#decrypts the rest of the text
	decrypt.append(hex(cuthex[i]^int('0x' + key,16)))
unencryptedhex = "".join(str(x) for x in decrypt).replace("0x","")
print (pdf)
m=4
open("decrypted.txt","w").write(" ".join(unencryptedhex[i:i+m] for i in range(0, len(unencryptedhex), m)))
