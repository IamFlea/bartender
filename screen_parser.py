import numpy as np
import cv2
from collections import defaultdict

OFFSET_DIGIT = defaultdict(int)
OFFSET_DIGIT[0] = 1
OFFSET_DIGIT[1] = -2

def threshold(img, thold=145, inverted=False):
    # Threshold the image.
    WHITE_COLOUR = 255
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flag = cv2.THRESH_BINARY_INV if inverted else cv2.THRESH_BINARY
    ret, img_result = cv2.threshold(img_gray, thold, WHITE_COLOUR, flag)
    return img_result

# Get digit from the resources  [From right to left]
def get_digit(image):
    # TODO make a dictionary
    if np.array_equal(image[3][2:], (0,0,0,255,0,0)):
        return 1
    elif np.array_equal(image[3], (0, 0, 255, 255, 255, 255, 0, 0)):
        # 2, 3, 9
        if image[6][4]:
            return 2
        elif image[6][2]:
            return 9
        else:
            return 3
        #return (2,3,9)
    elif np.array_equal(image[3], (0, 0, 0, 0, 255, 255, 0, 0)):
        return 4
    elif np.array_equal(image[3], (0, 0, 255, 255, 255, 255, 255, 0)):
        return 5
    elif np.array_equal(image[3], (0, 255, 255, 255, 255, 255, 0, 0)):
        return 0
    elif np.array_equal(image[3], (0, 255, 255, 0, 0, 0, 0, 0)):
        return 6
    elif np.array_equal(image[4], (0, 255, 255, 255, 255, 255, 255, 255)):
        return 7
    elif np.array_equal(image[3], (0, 255, 255, 0, 0, 255, 255, 0)):
        return 8
    else:
        return None

# Get digit from the time or the research [From left to right]
def get_digit_reversed(image):
    if np.array_equal(image[3][:6], (0,0,0,255,0,0)):
        return 1
    elif np.array_equal(image[3], (0, 0, 255, 255, 255, 255, 0, 0)):
        # 2, 3, 9
        if image[6][4]:
            return 2
        elif image[6][2]:
            return 9
        else:
            return 3
        #return (2,3,9)
    elif np.array_equal(image[3][2:], (0, 0, 255, 255, 0,0)):
        return 4
    elif np.array_equal(image[3], (0, 0, 255, 255, 255, 255, 255, 0)):
        #5,0
        #return 5,0
        if image[4][4]:
            return 5
        else:
            return 0
    elif np.array_equal(image[3], (0, 255, 255, 0, 0, 0, 0, 0)):
        return 6
    elif np.array_equal(image[3], (0, 255, 255, 255, 255, 255, 255, 255)):
        return 7
    elif np.array_equal(image[3], (0, 255, 255, 0, 0, 255, 255, 0)):
        return 8
    else:
        return None

def get_resource_number(img):
    number_str = ""
    start = len(img[1]) - 8
    global OFFSET_DIGIT
    for i in range(6): # while true, watchdog
        number = get_digit(img[0:len(img), start: start + 8])
        if number is None:
            break
        start -= 8 + OFFSET_DIGIT[number]
        number_str += str(number)
    try:
        return int(number_str[::-1])
    except ValueError:
        return None

def get_time_number(img):
    # Result string.
    time_str = ["", "", ""]
    # Offset calculation
    global OFFSET_DIGIT

    start = 0
    for i in range(3):
        # First number
        number = get_digit_reversed(img[:, start: start + 8])
        start += 8 + OFFSET_DIGIT[number]
        time_str[i] += str(number)
        # Second number
        number = get_digit_reversed(img[:, start: start + 8])
        start += 8 + OFFSET_DIGIT[number]
        time_str[i] += str(number)
        # Skip the colon symbol
        start += 4

    try:
        return int(time_str[0])*360 + int(time_str[1])*60 + int(time_str[2])
    except ValueError:
        return None

def get_time(img):
    # Position of the time bar.
    _TIME_INFOBAR_A = 38
    _TIME_INFOBAR_B = 50
    _TIME_INFOBAR_C = 5
    _TIME_INFOBAR_D = 67
    # Greyscale,trashold it
    im_time = img[_TIME_INFOBAR_A:_TIME_INFOBAR_B, _TIME_INFOBAR_C:_TIME_INFOBAR_D]
    im_time = threshold(im_time)
    # Do the end image processing.
    return get_time_number(im_time)

#Get resources info
def get_resources(img):
    # Resources infobar position in pixels.
    _RESOURCES_INFOBAR_A = 6
    _RESOURCES_INFOBAR_B = 18
    # Horizontal
    _RESOURCES_INFOBAR_WOOD_A = 29
    _RESOURCES_INFOBAR_WOOD_B = 75
    _RESOURCES_INFOBAR_FOOD_A = 108
    _RESOURCES_INFOBAR_FOOD_B = 152
    _RESOURCES_INFOBAR_GOLD_A = 180
    _RESOURCES_INFOBAR_GOLD_B = 229
    _RESOURCES_INFOBAR_STONE_A = 258
    _RESOURCES_INFOBAR_STONE_B = 306

    im_sliced = img[_RESOURCES_INFOBAR_A : _RESOURCES_INFOBAR_B, :_RESOURCES_INFOBAR_STONE_B]
    im_sliced = threshold(im_sliced)
    im_wood = im_sliced[:, _RESOURCES_INFOBAR_WOOD_A : _RESOURCES_INFOBAR_WOOD_B]
    im_food = im_sliced[:, _RESOURCES_INFOBAR_FOOD_A : _RESOURCES_INFOBAR_FOOD_B]
    im_gold = im_sliced[:, _RESOURCES_INFOBAR_GOLD_A : _RESOURCES_INFOBAR_GOLD_B]
    im_stone = im_sliced[:, _RESOURCES_INFOBAR_STONE_A : _RESOURCES_INFOBAR_STONE_B]

    stone = get_resource_number(im_stone)
    food = get_resource_number(im_food)
    gold = get_resource_number(im_gold)
    wood = get_resource_number(im_wood)
    return wood, food, gold, stone

# Returns currently researched technologies or `None`
def get_research(img, civ):
    # Expansions has icon and research percentage location bit on right
    expansions = ["Berbers", "Burmese", "Ethiopians", "Incas", "Indians", "Italians", "Khmer", "Magyars", "Malay", "Malians", "Portuguese", "Slavs", "Vietnamese"]
    offset = 3 if civ in expansions else 0
    # Check buggy civs.
    offset = -1 if civ == "Teutons" else offset
    offset = -3 if civ == "Goths" else offset

    # Get research percentage
    research = img[-92:-70, 583+offset:620+offset]
    research = threshold(research, thold=115,  inverted=True)

    # Get First Digit
    start = 0
    digit = get_digit_reversed(research[:,start:start+8])
    start += OFFSET_DIGIT[digit] + 8
    percentage_completed = digit
    if percentage_completed is None:
        return None, None, None # Not researching anything.

    # Get Second Digit	
    digit = get_digit_reversed(research[:,start:start+8])
    start += OFFSET_DIGIT[digit] + 8
    try:
        percentage_completed = digit + percentage_completed*10
    except TypeError: # It is only a percentage_completed with one digit.
        pass

    # Get the icon position and  convert it to grayscale
    icon_rgb = img[-90:-55, 449+offset:485+offset]
    icon = cv2.cvtColor(icon_rgb, cv2.COLOR_BGR2GRAY)

    metadata = (icon[10,10], icon[17,17], icon[20,20], icon[30,30], icon[30,5], icon[5,30], icon[25, 3])
    return metadata, percentage_completed, icon_rgb

BYTES_TO_CIV = {
    # Hue? Just some bytestring of UI which determinates the civiliyation
    # THe bytestring is grabbed from the greyscaled image with the location [-25:-20, :10]
    b"%DFH/$_fK\x1f%D&E4$_fT37)DE/\x1f_q`;.525+'Uuh:\x18DE$*\x0bG_^/" : "Aztecs",
    b"\x02L0fbhx/,\x8aK\x1e\x13\x9fCKep@\x18k\x00\x14\xa7-CpbP\x00*7\x1c\x9f4RpYWe\x05I'\x9c4E\x9agjk" : "Berbers",
    b'\x0e\x0e\x1b\x91mVkj}j\x13\x0c\x1b\x9bs`sq\x82g\x18\x0c.\x92natr~h\x12\x0c)\x99jdpoyb\x0e\x11;\x90mhlkxb' : "Britons",
    b'\x8d\x93\x92\x96\xb9\xc9\xc8\xc8\xc9\xc8\x8d\x93\x93\x94\x94\x93\x93\x93\x93\x93\x8d\x93\x94\x91\x8a\x8a\x8b\x8b\x8b\x8b\x8d\x93\x96\x86\\WXXXX\x8d\x93\x96\x87U99:::' : "Burmese",
    b'XU\\k\x83\x8e\x91\x90\x8e\x7fZX\\m\x83\x8f\x99\x98\x97\x86XR]s\x83\x93\x9a\x9d\x94\x85WTar\x83\x91\x9e\x9d\x95\x84WUan\x7f\x90\x9c\xa2\x95\x88' : "Byzantines",
    b"\x17aS\x1a1\x83'\x0b5\x0b\x18\x18dU\x177dQ(\x19\x17\x16\x18S\x14\x18LQ)5\x180\x19/P\x17\x19KO'\x170\x88S\x16\x12\x0c.7O" : "Celts",
    b"\x15\x1b'(\x85\x87\x85\x87NnY@x\x8f\x85\x85\x9flOlw[e[\xc7\xc5\xc6\x88\x86\x86\xb4^`X\xc5\xc6\xc6\xc5\xa0\xa0f\\eW\xc3\xc3\x88\xc6\xc5\x85" : "Chinese",
    b'@x\x8aBLz\x8bkWHWP5a6MJCNaO_ZNGh2kYSj\x8d\x8fv3g\x94G_~apvcQ\x83B\x82ii' : "Ethiopians",
    b'C~\x8e[h\x96}\xb1\x99\xac49979{WE|\x8e?O\x81\x99\x8ePj?/9\xaf\xba\xb8\x91D\xd9\x9873?\xb7Q06\xab}e\xfa\xba9' : "Franks",
    b'\x1e"?WQ/G&\x0e&0\'q\xaeQH/\'50461QESl!22<2BRR/R!=1>4>OR/8(>4' : "Goths",
    b'2\x1c2AJE<DoQ\x08-/0-;,N[P/,+/,<MXGX>1+,1.FYOPE;6771EQYQ' : "Huns",
    b'0, \x16\x0e\x157]hR#"\x1e\x1d\x15\x186ZfR!$(#\x17\x176\\iQ"\'2/\x1b\x177anY#)61\x17\x0e,ZmS' : "Incas",
    b'\x8a\xa4\xa8xN\x7f\x8a\x90\x9bv\xa3\x92\x9e\x8dp\x90wp\x87m\x91\x8f\x9c}Pny\x81\x88}\x97\x84\x9ew7q\x93\x8ctV\xa2{m]W\x86vk{m' : "Indians",
    b'GGyA0\x1e\x170:6<<fC6\x1e\x15/8/CCn@1!\x16+95CCm@0#\x13693CCvI6\x1e\x142<3' : "Italians",
    b"B)('+;  \x1a%C/A>-M\x1d:?%G,@C8U\x1d'??H>4@BZ = =JHCB@R\x17@5/" : "Japanese",
    b'\x1c\x1e #"!$&\'\'\x1e"$$%\'&\'((!%%&&\'(\'((#%\'((((((($$\')()\'(\'\'' : "Khmer",
    b'\x18\x1e\x1a\x1f1LNFNN>=w\x861KNFMMwf^bLKOOPOx`??HLOFZFaa_`7KOGRO' : "Koreans",
    b'/06C@TF,OL),,@UJJKQC.,.;TW>6pX/633HTB6Ll70.&@?#RJP' : "Magyars",
    b'\x13\x10\x10\x0f2K>3bW\x10\x10\x0e$358AO[\x1f\x0c\x16,3?LJ\x1b+-\x1a-*5>I \x0c\x0c::53:G.\r\x10\x0e' : "Malay",
    b'4;?ISTO\\de5:>IS\\][b_4<AJPVWU]b6<BGVb^d``5:CJPUVVW^' : "Malians",
    b"\x1c\x1e\x1d\x1d)\x1d\x1d\x02\x1b\x1e\x1e \x1e'\x1a\x1c!\x04\x16,\x1d \x1f(\x18\x1e\x1d\x01\x08.\x1c\x1d\x1e\x1d\x1c,\x1b\x02\x06/\x1b\x19\x1b\x1c,,\x17\x02\x07." : "Mayans",
    b'\x1b5*!! \x1b! \x1a\x1c7&\x1a!\x19\x19!!\x1b\x1cA)\x19 \x1c \x1b\x1a )ON=B8<7;D,G;760:;=6' : "Mongols",
    b'\n\x19\t\n]\xa9EQ}\x1c\t\t\t\t\x1b*\x15\n]r\n\t\x11\t\t\t\n\n[\xcc6\t\n\t\t\n\n5\xaa6q\n\x1b\n6\xa8\x1brDD' : "Persians",
    b's0&&\x1e\x1b@ahcJ*+MH6! >Wo,\x1eRxfY@!\x1fI,#"Njbh^9n.%$"Jhb`g' : "Portuguese",
    b'kl\x9f\xc0dW\xa0\x89\x85\x88k\x83\x9d\xccYP\xa5\x97\x86\x86g\x81\x9a\xa8Ze\xab\x89\x84\xa3Si\x82\xf2\x945\x8a\x9e\x85\x9aPg\x82q;,9\x88l\x87' : "Saracens",
    b'3ACC31B!@B\x19,..+,8)-L?@AE520\'\x1f-:-8KF04\'!"$&,\'-35 <8' : "Slavs",
    b'\x9e\xb2\x86\x0c\xa2\xdaYd\xa7\xb9\xa0\xab\xb5\r\xc4\x91C\xad\xa2\x9c\xa1\xb2\x89a\xcfG\x1b\xb1\xa1\x8b\xa1\xa4v\x96\xafJ\x1c\xbc\xa8\xc4\xac\xbc\x8f\xb8t\xac\x1a\xa0\xac\xbf' : "Spanish",
    b'\xb8\xba\xaaj\xa4\x8156\x80\xa4\xb5\xbb\xaf\xd6\xa5\x08\xce\xcf\x08\xa2\xb0\xbb\xad\xa9T\x08\x16\x17\x0bV\xb5\xbb\xa2\x8c\x185HK%\x18\xb6\xbc\xad\xcf\xa1\x08\x8er\x07\xa3' : "Teutons",
    b'wyI3LL3\x1502yxK3KzI%\x18(xxK2JfxJ2&xyL2KyZ{J\x1ax\x9523JZY^eK' : "Turks",
    b'v]8y3l\x81n3/u_<v9y\x7f[4/xbAtE|{M4/xc?rRwyD5/x`8tVtr;6/' : "Vietnamese",
    b'RPmQQNN8)(RG\x80#- +.((RT\x8e^qfNR*(RTiRHE..(3RYdRPOOXA*' : "Vikings",
}

# Civilizations were obtained by `print(get_civ_bytes(img))`
get_civ_bytes = lambda img: cv2.cvtColor(img[-25:-20, :10], cv2.COLOR_BGR2GRAY).tobytes()
# Use this functinoin for getting the civ info from the screenshot.
get_civ = lambda img: BYTES_TO_CIV[get_civ_bytes(img)]