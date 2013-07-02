array = [int("0x25",16),int("0x50",16),int("0x44",16),int("0x46",16)]
pdf = []
for i in range(0,len(array)-1):
	pdf.append(array[i]^array[i+1])

print(pdf)

hexdump = open("cuthexdump.txt",'r').read()
temp = hexdump.replace(" ","")
line = temp.replace("\n","")
n=2
cuthex = [line[i:i+n] for i in range(0, len(line), n)]

for i in range(0,len(cuthex)-3):
	if (int('0x' + cuthex[i],16))^(int('0x' + cuthex[i+1],16))==pdf[0]:
		if (int('0x' + cuthex[i+1],16))^(int('0x' + cuthex[i+2],16))==pdf[1]:
			if (int('0x' + cuthex[i+2],16))^(int('0x' + cuthex[i+3],16))==pdf[2]:
				print("FOUND XOR HEADER " + str(array[0]^(int('0x' + cuthex[i],16))) + str(array[1]^(int('0x' + cuthex[i+1],16))) + str(array[2]^(int('0x' + cuthex[i+2],16))) + str(array[3]^(int('0x' + cuthex[i+3],16))))
				key = str(array[0]^(int('0x' + cuthex[i],16))) + str(array[1]^(int('0x' + cuthex[i+1],16))) + str(array[2]^(int('0x' + cuthex[i+2],16))) + str(array[3]^(int('0x' + cuthex[i+3],16)))

decrypt=[]
for i in range(0,len(cuthex)):
	cuthex[i] = int('0x' + cuthex[i],16)

	decrypt.append(hex(cuthex[i]^int('0x' + key,16)))
unencryptedhex = "".join(str(x) for x in decrypt).replace("0x","")
print (pdf)
m=4
open("decrypted.txt","w").write(" ".join(unencryptedhex[i:i+m] for i in range(0, len(unencryptedhex), m)))
