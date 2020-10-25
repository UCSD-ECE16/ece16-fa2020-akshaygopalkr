import serial
import time
import enchant as e

vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'] # Vowels of the alphabet

"""
Sets up the Serial port
@:param serial_name: the name of the Serial port
@:param baud_rate: the baud rate the Serial port will be set to
@:return: the serial object with the name and baud rate
"""
def setup(serial_name, baud_rate):
    ser = serial.Serial(serial_name, baudrate=baud_rate)
    return ser

"""
Closes the serial port
@:param ser: the Serial object
"""
def close(ser):
    ser.close()

"""
Sends a String message to the Serial prot
@:param ser: The Serial object
@:param message: The message to be sent
"""
def send_message(ser, message):
    if message[-1] != "\n":  # we add a newline character so we know we've received a completed message
        message = message + "\n"
    ser.write(message.encode('utf-8')) # for sending messages to Serial we must encode from String to utf-8

"""
Checks if there is a message in Serial and saves it as a String
@:param ser: the Serial object
@:param num_bytes: the maximum number of bytes that will be read
@:return: The Message waiting in Serial
"""
def receive_message(ser, num_bytes=50):
    if ser.in_waiting > 0:
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None

"""
Translates a message from english to pig latin
@:param message: The English message to be translated
@:return: the message translated in pig latin
"""
def english_to_pig_latin(message):
    msg_arr = message.split('-') # Splits the message based on location of hyphens
    for i in range(len(msg_arr)):
        # If the first word starts with a vowel then add a "yay" to the end of the word
        if msg_arr[i][0] in vowels:
            msg_arr[i] += "yay"
        # Otherwise the word must start with a consonant
        else:
            # find the index of the first vowel in the message
            first_vwl_idx = find_first_vwl_idx(msg_arr[i])
            # For words with upper case, when we translate to pig latin
            # we should capitalize the correct letter after rearranging the letters
            if msg_arr[i][0].isupper():
                msg_arr[i] = msg_arr[i].lower()
                # edge case if the message starts with "qu"
                if msg_arr[i][0:2] == 'qu':
                    msg_arr[i] = msg_arr[i][first_vwl_idx + 1].upper() + msg_arr[i][first_vwl_idx + 2:] + "quay"
                # if the message starts with "y" then you should add an "ew" to the end
                elif msg_arr[i][0] == 'y':
                    msg_arr[i] = msg_arr[i][first_vwl_idx].upper() + msg_arr[i][first_vwl_idx + 1:] + msg_arr[i][0:first_vwl_idx] + 'ey'
                # For consonants, the word should start with the first vowel, followed by
                # the words after that vowel, the consonants before the first vowel, and "ay"
                else:
                    msg_arr[i] = msg_arr[i][first_vwl_idx].upper() + msg_arr[i][first_vwl_idx + 1:] + msg_arr[i][0:first_vwl_idx] + "ay"
            # Case for a word with all lower case letters
            else:
                # edge case if the message starts with "qu"
                if msg_arr[i][0:2] == 'qu':
                    msg_arr[i] = msg_arr[i][first_vwl_idx + 1] + msg_arr[i][first_vwl_idx + 2] + "quay"
                # edge case if the message starts with "y"
                elif msg_arr[i][0] == 'y':
                    msg_arr[i] = msg_arr[i][first_vwl_idx] + msg_arr[0:first_vwl_idx] + "ey"
                # follows the same restructuring as described in the upper case if block
                else:
                    msg_arr[i] = msg_arr[i][first_vwl_idx:] + msg_arr[i][0:first_vwl_idx] + "ay"
    return '-'.join(msg_arr) # join all the hyphenated words together so there is now one pig latin message


"""
Method to translate a pig latin message back to english
"""
def pig_latin_to_english(message):
    msg_arr = message.split('-')  # split the message into an array separated by '-'
    for i in range(len(msg_arr)):  # iterate through the message array
        if msg_arr[i][-3:] == 'yay':  # if the word starts with a vowel, just return the word without "yay"
            msg_arr[i] = msg_arr[i][:-3]
        else:  # if "ay" or "ey is at the end of the word
            letters_before = -3 # this keeps track of the words after the letters after "ay" or "ey"
            temp = msg_arr[i]
            capitalized = msg_arr[i][0].isupper()
            # if the pig latin message is capitalized, lower the first letter
            if capitalized:
                msg_arr[i] = msg_arr[i][0].lower() + msg_arr[i][1:]
            # while our translated message is not an English word
            while not dictionary.check(temp.lower()):
                # This creates a word with the letters before "ay" or "ey" and the letters before that
                temp = msg_arr[i][letters_before:-2] + msg_arr[i][0:letters_before]
                letters_before -= 1 #subtract letters_before so we can try to put a different combination of letters before
            # if the pig latin was capitalized, capitalize the first letter
            if capitalized:
                msg_arr[i] = temp[0].upper() + temp[1:]
            # otherwise set the message to the temporary variable we modified
            else:
                msg_arr[i] = temp
    # join the words in msg_array into one string
    return '-'.join(msg_arr)


"""
Finds the first vowel in the messagee
@:param message: the string to be checked
@:return: the index of the first vowel
"""
def find_first_vwl_idx(message):
    for i in range(len(message)):
        # if the character is a vowel then return that index
        if message[i] in vowels:
            return i
    return -1

"""
Concatenates the pig latin and english version of the message into one string
@:param: the original English message
@:return: The pig latin and english version of the message
"""
def trans_and_decode(message):
    translation = english_to_pig_latin(message)
    decoding = pig_latin_to_english(translation)
    return translation + " " + decoding


dictionary = e.Dict('en_US')
ser = setup("/dev/cu.usbserial-1410", 115200)
time.sleep(3)  # I have a cheap dongle that delays board reset so I need to wait some time before sending the message
send_message(ser, trans_and_decode("Quotient")) #sends translated and retranslated english version to the serial.
time.sleep(1)
close(ser)
