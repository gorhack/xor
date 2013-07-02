xor
===

Find headers in XOR'd data. 
  Create the encryption/decryption key
  XOR all data from the drive
  
Current limitations
  numuber of known file signatures
  size of key is limited to no greater than length of the file signature
  partial decryption is not made but plans can be:
      xor starting at the file signature header and end at the tail


Final Goal: Create a new method for decrypting any XOR'd data by using known file signatures.
