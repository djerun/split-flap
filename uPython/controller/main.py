from machine import Pin, SPI
from splitflap import SplitFlap, luts
from time import sleep
import usocket
from bottle import run, get, post, request

OUT = Pin.OUT
IN = Pin.IN

NUM_COL = 22
NUM_ROW = 2

char_lut = luts.char_lut
reverse_char_lut = {}
for key in char_lut:
    reverse_char_lut[char_lut[key]] = key

words = [
#                          |23
    "Chaos Computer Club           Hamburg",
    "Chaos Computer Glub           Hamburg",
    "Chaos Computer Klub           Hamburg",
    "Chaos Computer Klub           Haramburg",
    "www.hamburg.ccc.de    hamburg.freifunk.net",
    "I'M THE CREEPER:      CATCH ME IF YOU CAN",
    "Made possible by hammi space and marble",
    "Original Display      from Hamburg HBF",
    "beep boop beep",
    "Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø#Ø",
    "hello world",
    "welcome to the Jungle",
    "i am a display from   the space age",
    "oldschool tech is     awesome!",
    "Vorsprung durch       Technik",
    "Spass am Geraet.",
    "/(ØWØ)/",
    "War is Peace",
    "Freedom is Slavery",
    "Ignorance is Strength",
    "Vectoring is Glasfaser",
    "The only way to win the game is not to Play!"

]

def vals_to_mat(vals, lut, w, h, default):
    vals = vals.upper()
    mat = [[default for a in range(h)] for b in range(w)]
    for y in range(h):
        for x in range(w):
            i = x + y*w
            if (i < len(vals)) and (vals[i] in lut):
                mat[x][y] = lut[vals[i]]
    return mat


def show_word(word):
    sf.set(vals_to_mat(word, char_lut, NUM_COL, NUM_ROW, char_lut[' ']))
    sleep(1)


def show_words():
    for word in words:
        show_word(word)


spi = SPI(-1, baudrate=int(500e3), phase=1, polarity=0, sck=Pin(5), miso=Pin(4), mosi=Pin(16))
col_rclk = Pin(12, OUT)
start_rclk = Pin(13, OUT)
face_load = Pin(15, OUT)

sf = SplitFlap(NUM_COL, NUM_ROW, spi, col_rclk, start_rclk, face_load)
# show_word("DEBUG IP: {}".format(WLAN().ifconfig()[0]))

#s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
#s.settimeout(1)
#s.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
#s.bind(('10.42.23.221', 1337))
#s.listen(1)


#def try_read_from_socket():
#    conn = False
#    try:
#        print("Try accepting a connection...")
#        conn, addr = s.accept()
#        print("Got connection {} {}".format(conn, addr))
#        if 0 >= addr[1]:
#            return
#        conn.settimeout(1)
#        print("Reading from connection {}...".format(addr))
#        word = conn.recv(64).decode('ascii')
#        print("Got word {}".format(word))
#        try:
#            conn.close()
#        except:
#            pass
#        show_word(word)
#    except Exception as e:
#        print(e)
#        if conn:
#            conn.close()
#    except OSError as e:
#        print(e)
#        if conn:
#            conn.close()


#while(1):
#    try_read_from_socket()
#    show_words()

def faces_to_string(faces):
    res = ''
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            try:
                res += reverse_char_lut[face[col][row]]
            except KeyError:
                res += ' '
    return res

@post('/')
def write():
    text = request.forms.get('text')
    show_word(text)

@get('/')
def get():
    return faces_to_string(sf._get_faces())

run(host='0.0.0.0', port=80)
