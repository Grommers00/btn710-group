#3.1 COMPLETED
#1. pick a few random words r1, . . . , rb and take i = 0
#2. pick r = r1 . . . rb−1(rb ⊕ i)
#3. if O(r|y) = 0 then increment i and go back to the previous step
#4. replace rb by rb ⊕ i
#5. for n = b down to 2 do
#(a) take r = r1 . . . rb−n(rb−n+1 ⊕ 1)rb−n+2 . . . rb
#(b) if O(r|y) = 0 then stop and output (rb−n+1 ⊕ n). . .(rb ⊕ n)
#6. output rb ⊕ 1 (We do not need to do this, we xor with value 0)

#3.2  - TO DO
#1. take rk = ak ⊕ (b − j + 2) for k = j, . . . , b
#2. pick r1, . . . , rj−1 at random and take i = 0
#3. take r = r1 . . . rj−2(rj−1 ⊕ i)rj . . . rb
#4. if O(r|y) = 0 then increment i and go back to the previous step
#5. output rj−1 ⊕ i ⊕ (b − j + 2)

from btn710.oracle import btnPad, btnUnpad, encrypt, decrypt
from btn710.attack import generateForgedMsg, lastByteForgery, elementForgery, findXorByte, secLastByteForgery
from Crypto.Cipher import AES
from Crypto.Util.py3compat import bchr, bord

if __name__ =='__main__':
    plainText = b'HelloWorld!aaaa'
    #Normal server-client messages
    cipherText = encrypt(plainText)
    print(b'Cipher Text: ' + cipherText)
    print(b'Plain Text: ' + decrypt(cipherText))
    
    # Finding last byte correct padding
    crackedIV = []
    forgedMsg, forgery, forgedLastByte, lastBlock = generateForgedMsg(cipherText)
    correctPadding = False
    count = 0
    while(not correctPadding):
        try: 
            decryptedMsg = decrypt(forgedMsg)
            correctPadding = True
        except ValueError:
            forgedMsg, forgery = lastByteForgery(forgery, forgedLastByte, lastBlock, count)
            count += 1
    tempLastIV = forgery.decode('utf-8')[-1]

    # Modify each element until we know the padding length
    count = 0
    while(correctPadding):
        try: 
            decryptedMsg = decrypt(forgedMsg)
            forgedMsg = elementForgery(forgery, lastBlock, count)
            count += 1
        except ValueError:
            correctPadding = False

    correctPaddingLength = 17 - count
    if(correctPaddingLength == 1):
        crackedIV.insert(count - 1, tempLastIV)
    
    # find byte that xor with last byte to 1
    # set last byte to that new byte
    # loop through second last byte with xor 0-255 to find write padding
    # modify each element up til but not including the second last byte and test each to see what is the padding length

    newLastByte = findXorByte(tempLastIV, 1)
    forgery = forgery[:-1] + bchr(newLastByte)
    forgedLastByte = bytes(forgery.decode('utf-8')[-2], 'utf-8')
    correctPadding = False
    count = 0
    while(not correctPadding):
        try: 
            decryptedMsg = decrypt(forgedMsg)
            correctPadding = True
        except ValueError:
            forgedMsg, forgery = secLastByteForgery(forgery, forgedLastByte, lastBlock, count)
            count += 1
    tempLastIV = forgery.decode('utf-8')[-1]