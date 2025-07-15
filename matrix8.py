#!/usr/bin/env python3
#   Matrix8 Encryption    #

import os
import time
import sys



textEncoder = [
    ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X'],
    ['Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f'],
    ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'],
    ['o', 'p', 'q', 'r', 's', 't', 'u', 'v'],
    ['w', 'x', 'y', 'z', '0', '1', '2', '3'],
    ['4', '5', '6', '7', '8', '9', '',  '']
]



def find_position(char):
    for rowIndex, row in enumerate(textEncoder):
        for colIndex, item in enumerate(row):
            if item == char:
                return (rowIndex, colIndex)
    return None  # If not found


def spars_data(inputText):
    newData = ""
    
    for x in str(inputText):
        location = find_position(x)
        if location == None:
            newData += x
        else:
            row, col = location
            newData += f"{row}{col}"  # Combine row and col as string
    return newData


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def encrypt_code(code, shiftCode, isFlipping):
    codeLength = len(str(code))
    finalShiftCode = ''
    x = 0
    while x < codeLength:
        finalShiftCode += str(shiftCode)
        x += 1
    
    shiftedCode = int(code) + int(finalShiftCode)
    if isFlipping == True:
        shiftedCode = str(shiftedCode)[::-1]
    
    firstDigit = int(str(code)[0])
    shiftedCode = int(shiftedCode) // firstDigit

    codeLength = len(str(shiftedCode))
    shiftedCode = int(shiftedCode) // int(codeLength)
    shiftedCode = str(shiftedCode)[-4:]
    
    return shiftedCode
    

def encrypt_data(inputText, encryptionCode):
    integerFlip = True
    combinedCodeValue = sum(int(x) for x in str(encryptionCode))
    shiftCode = int(str(combinedCodeValue)[0])
    if combinedCodeValue % 2 != 0:
        integerFlip = False
    
    sparsedData = spars_data(inputText)
    encryptedCode = encrypt_code(encryptionCode, shiftCode, integerFlip)
    stageTwoData = ""
    digitCount = 0
    activeDigits = ""

    x = 0
    while x < len(sparsedData):
        if sparsedData[x].isdigit():
            digitCount += 1
            activeDigits += sparsedData[x]

            if digitCount == 2:
                activeDigits = str(int(activeDigits) + int(str(shiftCode) + str(shiftCode)))
                if integerFlip == True:
                    activeDigits = str(activeDigits)[::-1]
                activeDigits = int(activeDigits) * int(encryptedCode)
                activeDigits = str(activeDigits).zfill(7)
                
                stageTwoData += str(activeDigits)
                activeDigits = ""
                digitCount = 0
        
        else:
            stageTwoData += sparsedData[x]
        x += 1

    return stageTwoData


def decrypt_data(inputText, encryptionCode):
    integerFlip = True
    combinedCodeValue = sum(int(x) for x in str(encryptionCode))
    shiftCode = int(str(combinedCodeValue)[0])
    if combinedCodeValue % 2 != 0:
        integerFlip = False

    encryptedCode = encrypt_code(encryptionCode, shiftCode, integerFlip)
    digitCount = 0
    activeDigits = ""
    finalShiftCode = ""
    stageTwoData = ""


    x = 0
    while x < len(inputText):
        if inputText[x].isdigit():
            digitCount += 1
            activeDigits += inputText[x]

            if digitCount == 7:
                activeDigits = int(activeDigits) // int(encryptedCode)
                if integerFlip == True:
                    activeDigits = str(activeDigits)[::-1]

                i = 0
                while i < len(str(activeDigits)):
                    finalShiftCode += str(shiftCode)
                    i += 1
                
                activeDigits = str(int(activeDigits) - int(finalShiftCode))
                
                try:
                    if len(activeDigits) != 2:
                        activeDigits = "0" + activeDigits
                    stageTwoData += textEncoder[int(activeDigits[0])][int(activeDigits[1])]
                except:
                    stageTwoData = ">ERROR TRY AGAIN<   Please check that both the data and encryption code are correct!\n\n"
                    break

                finalShiftCode = ""
                digitCount = 0
                activeDigits = ""
        else:
            stageTwoData += inputText[x]
        
        x += 1
    return stageTwoData


def save_to_file(data, address):
    try:
        with open(address, "w") as f:
            f.write(data)
        return True
    except:
        return False


def load_from_file(address):
    data = ""
    try:
        with open(address) as f:
            data = f.read()
        return data
    except:
        data = ">ERROR PLEASE TRY AGAIN<"
        return data
    
    

while True:
    clear_screen()
    print("Please Make A Selection:     [1] Encrypt Text    [2] Decrypt Text    [3] Encrypt File    [4] Decrypt File    [/quit] Exit App        Tip: You can always type [/quit] to exit the program or [/exit] to return to this screen!")
    inputSelection = input()

    if inputSelection == "1":
        clear_screen()
        print ("Please Enter Text To Be Encrypted:")
        text = input()
        if text == "/quit":
            sys.exit()
        elif text == "/exit":
            continue

        isExit = False
        while True:
            print ("\nPlease Enter Your Encryption Code:        Tip: You can use only numbers up to 11 digits, It is suggested to use at least 5 digits!")
            code = input()
            if code == "/quit":
                sys.exit()
            elif code == "/exit":
                isExit = True
                break
            elif not code.isdigit():
                print ("Invalid Input Please Try Again... \n")
            elif len(code) > 11:
                print ("Invalid Input Please Try Again... \n")
            else:
                break

        if isExit == True:
            continue
        
        clear_screen()
        finalData = encrypt_data(text, code)

        while True:        
            print ("Encrypted Data:\n\n", finalData)
            print ("\n\nUse [/exit] to leave this screen, [/quit] to exit the program, [/save] to save data to a file!")

            Input = input()
            if Input == "/quit":
                sys.exit()
            elif Input == "/exit":
                break
            elif Input == "/save":
                print ("\nPlease Input Save File Path...    Tip: You can use pre-existing files and have them overwriten with your new data!")
                address = input()
                if save_to_file(finalData, address) == True:
                    print ("Data Saved!")
                    time.sleep(0.3)
                    clear_screen()
                else:
                    print ("Failed To Save Data Please Try Again...     Tip: Make sure your file path points to the correct file, if the file does not exist one will be made!\n\n")
            else:
                clear_screen()
        
    elif inputSelection == "2":
        clear_screen()
        print ("Please Enter Text:")
        text = input()
        if text == "/quit":
            sys.exit()
        elif text == "/exit":
            continue

        isExit = False
        while True:
            print ("\nPlease Enter Your Encryption Code:        Tip: You can use only numbers up to 11 digits, It is suggested to use at least 5 digits!")
            code = input()
            if code == "/quit":
                sys.exit()
            elif code == "/exit":
                isExit = True
                break
            elif not code.isdigit():
                print ("Invalid Input Please Try Again... \n")
            elif len(code) > 11:
                print ("Invalid Input Please Try Again... \n")
            else:
                break

        if isExit == True:
            continue
        
        clear_screen()
        finalData = decrypt_data(text, code)

        while True:
            print ("Decrypted Data:\n\n", finalData)
            print ("\n\nUse [/exit] to leave this screen, [/quit] to exit the program, [/save] to save data to a file!")

            Input = input()
            if Input == "/quit":
                exit()
            elif Input == "/exit":
                break
            elif Input == "/save":
                print ("\nPlease Input Save File Path...    Tip: You can use pre-existing files and have them overwriten with your new data!")
                address = input()
                if save_to_file(finalData, address) == True:
                    print ("Data Saved!")
                    time.sleep(0.3)
                    clear_screen()
                else:
                    print ("Failed To Save Data Please Try Again...     Tip: Make sure your file path points to the correct file, if the file does not exist one will be made!\n\n")
            else:
                clear_screen()

    elif inputSelection == "3":
        clear_screen()
        
        data = ""
        isExit = False
        while True:
            print ("Please Enter File Directory:")
            address = input()
            if address == "/quit":
                sys.exit()
            elif address == "/exit":
                isExit = True
                break

            data = load_from_file(address)
            if data != ">ERROR PLEASE TRY AGAIN<":
                break
            print (data, "\n\n")

        if isExit == True:
            continue
        
        while True:
            print ("\nPlease Enter Your Encryption Code:        Tip: You can use only numbers up to 11 digits, It is suggested to use at least 5 digits!")
            code = input()
            if code == "/quit":
                sys.exit()
            elif code == "/exit":
                isExit = True
                break
            elif not code.isdigit():
                print ("Invalid Input Please Try Again... \n")
            elif len(code) > 11:
                print ("Invalid Input Please Try Again... \n")
            else:
                break

        if isExit == True:
            continue

        clear_screen()
        finalData = encrypt_data(data, code)

        while True:        
            print ("Encrypted Data:\n\n", finalData)
            print ("\n\nUse [/exit] to leave this screen, [/quit] to exit the program, [/save] to save data to a file!")

            Input = input()
            if Input == "/quit":
                sys.exit()
            elif Input == "/exit":
                break
            elif Input == "/save":
                print ("\nPlease Input Save File Path...    Tip: You can use pre-existing files and have them overwriten with your new data!")
                address = input()
                if save_to_file(finalData, address) == True:
                    print ("Data Saved!")
                    time.sleep(0.3)
                    clear_screen()
                else:
                    print ("Failed To Save Data Please Try Again...     Tip: Make sure your file path points to the correct file, if the file does not exist one will be made!\n\n")
            else:
                clear_screen()

    elif inputSelection == "4":
        clear_screen()
        
        data = ""
        isExit = False
        while True:
            print ("Please Enter File Directory:")
            address = input()
            if address == "/quit":
                sys.exit()
            elif address == "/exit":
                isExit = True
                break

            data = load_from_file(address)
            if data != ">ERROR PLEASE TRY AGAIN<":
                break
            print (data, "\n\n")

        if isExit == True:
            continue
        
        while True:
            print ("\nPlease Enter Your Encryption Code:        Tip: You can use only numbers up to 11 digits, It is suggested to use at least 5 digits!")
            code = input()
            if code == "/quit":
                sys.exit()
            elif code == "/exit":
                isExit = True
                break
            elif not code.isdigit():
                print ("Invalid Input Please Try Again... \n")
            elif len(code) > 11:
                print ("Invalid Input Please Try Again... \n")
            else:
                break

        if isExit == True:
            continue

        clear_screen()
        finalData = decrypt_data(data, code)

        while True:        
            print ("Decrypted Data:\n\n", finalData)
            print ("\n\nUse [/exit] to leave this screen, [/quit] to exit the program, [/save] to save data to a file!")

            Input = input()
            if Input == "/quit":
                sys.exit()
            elif Input == "/exit":
                break
            elif Input == "/save":
                print ("\nPlease Input Save File Path...    Tip: You can use pre-existing files and have them overwriten with your new data!")
                address = input()
                if save_to_file(finalData, address) == True:
                    print ("Data Saved!")
                    time.sleep(0.3)
                    clear_screen()
                else:
                    print ("Failed To Save Data Please Try Again...     Tip: Make sure your file path points to the correct file, if the file does not exist one will be made!\n\n")
            else:
                clear_screen()

    elif inputSelection == "/quit":
        sys.exit()

    else:
        print ("Invalid Input Please Try Again... \n")
