def shift(letter: str, amount: int) -> str:
    ascii_val = ord(letter) + amount
    while ascii_val < ord('A'):
        ascii_val += 26
    while ascii_val > ord('Z'):
        ascii_val -= 26
    return chr(ascii_val)


class Caesar:
    '''
    Class which can encrypt and decrypt messages using the caesar cypher.
    '''
    key: int

    def __init__(self, key: int | str):
        '''
        Constructor

        key : int or str
            The key used for encryption and decryption. Can either be an
            alphabet character, or integer between 0 and 25
        '''
        if type(key) is int:
            self.key = key
        elif type(key) is str:
            if not key.isalpha() or len(key) != 1:
                raise ValueError("'key' must be an alphabet character")
            self.key = ord(key.upper()) - ord('A')
        else:
            raise ValueError("'key' must be an int or character")

    def encrypt(self, message: str) -> str:
        '''
        Encrypts a message using the key
        '''
        return "".join((shift(letter, self.key) for letter in message))

    def decrypt(self, message: str) -> str:
        '''
        Decrypts a message using the key
        '''
        return "".join((shift(letter, -self.key) for letter in message))


class CrackCaesar:
    '''
    Class with tools to crack a caesar cypher.
    '''
    code: str
    freq_en: dict[str, float] = {
        'A': 0.080,
        'B': 0.015,
        'C': 0.030,
        'D': 0.040,
        'E': 0.130,
        'F': 0.020,
        'G': 0.015,
        'H': 0.060,
        'I': 0.065,
        'J': 0.005,
        'K': 0.005,
        'L': 0.035,
        'M': 0.030,
        'N': 0.070,
        'O': 0.080,
        'P': 0.020,
        'Q': 0.002,
        'R': 0.065,
        'S': 0.060,
        'T': 0.090,
        'U': 0.030,
        'V': 0.010,
        'W': 0.015,
        'X': 0.005,
        'Y': 0.020,
        'Z': 0.002
    }
    freq_code: dict[str, float] = {}
    count_code: dict[str, int] = {}
    alg: Caesar

    def __init__(self, code: str):
        '''
        Constructor

        code : str
            The code which you wish to crack.
        '''
        self.code = code.upper()
        self.alg = Caesar(0)

    def compute_frequencies(self):
        '''
        Computes the letter freqencies in the encoded message.
        '''
        for i in 'QWERTYUIOPASDFGHJKLZXCVBNM':
            self.count_code[i] = 0
            self.freq_code[i] = 0
        for letter in self.code:
            self.count_code[letter] += 1
            self.freq_code[letter] += 1
        for letter in self.freq_code:
            self.freq_code[letter] /= len(self.code)

    def print_frequencies(self):
        '''
        Prints the letter frequencies sorted from most common to least
        '''
        for letter in sorted(self.freq_code, key=lambda x: -self.freq_code[x]):
            print(f"{letter}: {self.freq_code[letter]}")

    def compute_phi(self, i: int) -> float:
        '''
        Computes the phi function for the ciphertext.
        '''
        if not self.freq_code:
            self.compute_frequencies()
        total: float = 0
        for letter in self.freq_code:
            total += self.freq_code[letter] * self.freq_en[shift(letter, -i)]
        return total

    def test(self, i: int) -> str:
        self.alg.key = i
        return self.alg.decrypt(self.code)
