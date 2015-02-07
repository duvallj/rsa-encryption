#! /usr/bin/python3
from random import randint, choice

M, P, D = 0, 0, 0
try:
    with open("secret.rsaC", 'r') as initcodes:
        init_numbers = initcodes.read().split(";")
        M = int(init_numbers[0])
        P = int(init_numbers[1])
        D = int(init_numbers[2])
    if M <= D:
        raise(FileNotFoundError)

except FileNotFoundError:
    def prime_factors(num):
        n = num
        l = []
        d = 2
        while d*d <= n:
            while (n % d) == 0:
                l.append(d)
                n /= d
            d += 1
        if n > 1:
            l.append(n)
        if l == [n]:
            return "prime"
        else:
            return l

    prime_nums = []
    for x in range(2, 1000):
        if prime_factors(x) == "prime":
            prime_nums.append(x)
    big_primes = prime_nums[31:]
    small_primes = prime_nums[:10]

    M = -1
    D = 0
    while M < D:
        a = choice(big_primes)
        b = choice(big_primes)
        M = a*b
        n1 = (a-1)*(b-1)
        ln = prime_factors(n1)
        pl = []

        for x in small_primes:
            if ln.count(x) == 0:
                pl.append(x)

        P = choice(pl)*choice(pl)

        while (n1*x+1) % P != 0:
            x += 1

        D = int((n1*x+1)/P)

    with open("secret.rsaC", 'w') as writefile:
        writefile.write("{};{};{};".format(M, P, D))


def encode_list(string, modulator, power):
    list_of_string = list(string)
    code = []
    for character in list_of_string:
        thing = encode(character, modulator, power)
        code.append(thing)
    return code


def encode(character, modulator, power):
    return pow(ord(character), power, modulator)


def decode_list(num_list, mod, power):
    trans_nums = []
    word = []
    for num in num_list:
        thing = decode(num, mod, power)
        trans_nums.append(thing)
    for character in trans_nums:
        word.append(chr(character))
    return word


def decode(number, modulation, power):
    return pow(number, power, modulation)


def to_binary(number, base):
    return '{:0{}b}'.format(number, base)


def from_binary(bi_string):
    return int(bi_string, 2)

ALL_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '!', '@', '#', '$', '%', '^', '&', '[', ']', '{', '}', '|', ';', ':', ',', '.', '?']


def to_everyletter( num ):
    if num == 0: return ALL_CHARS[0]
    digits = []
    while num:
        num = int(num)
        digits.append(ALL_CHARS[num % 80])
        num /= 80
    digits.reverse()
    del digits[0]
    return ''.join(digits)

def from_everyletter( letters ):
    output = 0
    reversed_letters = letters[::-1]
    for letter in reversed_letters:
        index = reversed_letters.index(letter)
        output+=ALL_CHARS.index(letter)*pow(80, index)
        #This is necesary for strings w/ more than one of the same character
        reversed_letters = reversed_letters[:index] + '_' + reversed_letters[index+1:]
    return output


def encode_text( string, modulation, power ):

    code = encode_list( string, modulation, power )

    key_list = []

    for thing in range(0, len(code)):
        key_list.append(randint(0, 31))
        code[thing] += key_list[thing]
        
    output = ""

    for counter in range(0, len(key_list)):
        binary = to_binary(key_list[counter], 5)
        binary += to_binary(code[counter], 19)
        output += to_everyletter(from_binary(binary))+'_'
    return output

def decode_text( all_char_string, mod, power ):

    all_char_things=all_char_string.split('_')
    binary_list=[]

    for thing in all_char_things:
        binary_list.append(to_binary(from_everyletter(thing), 24))
    binary_file=''.join(binary_list)

    if not(len(binary_file) % 24 == 0):
        return "Error: wrong number of bits"

    encoded = []
    key_list = []

    for index_start in range(0, int(len(binary_file)/24)+1):
        key_list.append(binary_file[index_start*24:index_start*24+5])
        encoded.append(binary_file[index_start*24+5:(index_start+1)*24])

    del encoded[len(encoded)-1]
    del key_list[len(key_list)-1]

    decoded_first_stage = []

    for counter in range(0, len(key_list)):
        decoded_first_stage.append(from_binary(encoded[counter]))
        key_list[counter] = from_binary(key_list[counter])
        decoded_first_stage[counter] -= key_list[counter]

    decoded_stage_two = decode_list(decoded_first_stage, mod, power)
    return "".join(decoded_stage_two)

if __name__ == "__main__":
    from os import listdir, getcwd, remove
    files = []

    def refresh():
        global files
        files = []
        for file in listdir(getcwd()):
            if file.endswith(".rsa"):
                files.append(file)

    def encode_click():
        modulator = M
        power = P
        message = str(input("Enter message: "))
        filename = str(input("What will the file be called? "))
        with open(getcwd() + "/" + filename + ".rsa", 'w') as writefile:
            writefile.write(encode_text(message, modulator, power))
        print("Done!")

    def decode_click():
        modulator = M
        decrypting_power = D
        print("List of availible files:")
        global files
        for file in files:
            print(file)
        print()
        filename = str(input("Which would you like to decrypt? "))
        if not filename.endswith(".bef3"):
            filename += ".bef3"
        with open(getcwd() + "/" + filename) as readfile:
            print("Here is your message:" + "\n")
            print(decode_text( readfile.read(), modulator, decrypting_power ))

    while True:
        refresh()
        print()
        what_to_do = str(input("What do you want to do? "))
        user_encode = ['e', 'E', 'encode', 'Encode']
        user_decode = ['d', 'D', 'decode', 'Decode']
        if what_to_do in user_encode:
            encode_click()
        elif what_to_do in user_decode:
            decode_click()
        elif what_to_do == 'q':
            print("goodbye")
            break
        elif what_to_do == 'r':
            remove('secret.rsaC')
            break
        else:
            print("Not a valid command")
