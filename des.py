def permute(permutation: list[int], value: int, size: int) -> int:
    '''
    Helper function which permutes a binary number by some list.
    Assumes the permutation list is 1-indexed.

    permutation : list[int]
        List of integers. The bit at `permutation[i]` is used to set
        the `i`th bit of the output, reading from left to right.
    value : int
        The value to permute
    size : int
        The number of bits in the input value
    '''
    result: int = 0
    i: int = len(permutation) - 1
    for index in permutation:
        temp: int = value & (1 << (size - index))
        temp >>= (size - index)
        temp <<= i
        i -= 1
        result |= temp
    return result


def left_shift(value: int, amount: int, size: int):
    '''
    Applies a **round** left-shift on value.
    Similar to `value << amount`, but bits at the left end of
    `value` are moved to the right end instead of overflowing.

    value : int
        The value to left shift
    amount : int
        The amount to shift by
    size : int
        The number of bits in `value`
    '''
    value <<= amount
    for i in range(amount):
        temp: int = value & (1 << (size + i))
        temp >>= (size)
        value |= temp
    return value & ((1 << size) - 1)


def print_bin(value: int, size: int, group: int):
    '''
    Helper function which prints an integer's binary representation.
    Separates the bits into groups to make it nicer to look at.

    value : int
        The integer whose binary representation should be printed
    size : int
        The number of bits in the integer to print
    group : int
        How to group the bits in the printed output.
        Should be a factor of `size`
    '''
    s: str = bin(value)[2:].rjust(size, '0')
    num_groups: int = int(size / group)
    for i in range(num_groups):
        print(s[i * group:(i + 1) * group], end=' ')
    print()


class DES:
    '''
    Class which implements the DES algorithm for encryption and decryption.
    '''
    key: int = 0
    PC1: list[int] = [
        57, 49, 41, 33, 25, 17, 9,
        1,  58, 50, 42, 34, 26, 18,
        10, 2,  59, 51, 43, 35, 27,
        19, 11, 3,  60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7,  62, 54, 46, 38, 30, 22,
        14, 6,  61, 53, 45, 37, 29,
        21, 13, 5,  28, 20, 12, 4
    ]
    PC2: list[int] = [
        14, 17, 11, 24, 1,  5,
        3,  28, 15, 6,  21, 10,
        23, 19, 12, 4,  26, 8,
        16, 7,  27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]
    iteration_table: list[int] = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]
    IP: list[int] = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    IP_inv: list[int] = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41,  9, 49, 17, 57, 25,
    ]
    E_bit: list[int] = [
        32,  1,  2,  3,  4,  5,
        4,   5,  6,  7,  8,  9,
        8,   9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]
    S_Boxes: list[int] = [
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
        0,  15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
        4,   1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13,
        15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
        10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
        7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
        2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
        12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
        4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
        13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11,
    ]
    P: list[int] = [
        16,  7, 20, 21,
        29, 12, 28, 17,
        1,  15, 23, 26,
        5,  18, 31, 10,
        2,   8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25
    ]
    round_keys: list[int] = None
    silent: bool

    def __init__(self, _key: int, _silent=True):
        '''
        Constructor

        _key : int
            The key used for encryption and decryption
        _silent : bool
            Whether or not to print information about encryption / decryption.
        '''
        self.key = _key
        self.silent = _silent

    def generate_round_keys(self):
        '''
        Uses the master key to generate the 16 round keys
        '''
        self.round_keys = []
        key_prime = permute(self.PC1, self.key, 64)
        C = (key_prime & 0xFFFFFFF0000000) >> 28
        D = key_prime & 0xFFFFFFF
        for i in range(16):
            C = left_shift(C, self.iteration_table[i], 28)
            D = left_shift(D, self.iteration_table[i], 28)
            temp = (C << 28) | D
            temp = permute(self.PC2, temp, 56)
            if not self.silent:
                print(f"Round key {i+1}: ", end='')
                print_bin(temp, 48, 6)
            self.round_keys.append(temp)

    def get_s_box(self, i: int, row: int, col: int) -> int:
        '''
        Helper method which gets SBOX_i[row][col]
        '''
        index = 64 * i
        return self.S_Boxes[index + (row * 16) + col]

    def f(self, R: int, key: int) -> int:
        '''
        Used in the DES encryption algorithm

        R : int
            A 32-bit intermediate value in the encryption
        key : int
            A 48-bit round key.

        returns : int
            A 32-bit value.
        '''
        R = permute(self.E_bit, R, 32)
        R = R ^ key
        out = 0
        # Splits R into groups of 6 bits
        shift = 0
        for i in range(8):
            group = R & 0b111111
            R >>= 6
            row = ((group >> 4) & 2) | (group & 1)
            col = (group & 0b011110) >> 1
            out |= (self.get_s_box(7 - i, row, col) << shift)
            shift += 4
        out = permute(self.P, out, 32)
        if not self.silent:
            print("f  : ", end='')
            print_bin(out, 32, 4)
        return out

    def encrypt_block(self, block: int) -> int:
        '''
        Encrypts a 64-bit block of data using the DES algorithm
        '''
        if not self.round_keys:
            self.generate_round_keys()
            if not self.silent:
                print()
        block = permute(self.IP, block, 64)
        L = (block & 0xFFFFFFFF00000000) >> 32
        R = block & 0xFFFFFFFF
        if not self.silent:
            print("L_0: ", end='')
            print_bin(L, 32, 4)
            print("R_0: ", end='')
            print_bin(R, 32, 4)
            print()
        for i in range(16):
            temp = R
            R = L ^ self.f(R, self.round_keys[i])
            L = temp
            if not self.silent:
                print(f"L_{i+1}: ", end='')
                print_bin(L, 32, 4)
                print(f"R_{i+1}: ", end='')
                print_bin(R, 32, 4)
                print()
        out = (R << 32) | L
        if not self.silent:
            print("RL: ", end='')
            print_bin(out, 64, 4)
        return permute(self.IP_inv, out, 64)

    def decrypt_block(self, block: int) -> int:
        '''
        Decrypts a 64-bit block of data using the DES algorithm
        '''
        if not self.round_keys:
            self.generate_round_keys()
        block = permute(self.IP, block, 64)
        L = (block & 0xFFFFFFFF00000000) >> 32
        R = block & 0xFFFFFFFF
        if not self.silent:
            print("L_0: ", end='')
            print_bin(L, 32, 4)
            print("R_0: ", end='')
            print_bin(R, 32, 4)
            print()
        for i in range(16):
            temp = R
            R = L ^ self.f(R, self.round_keys[15 - i])
            L = temp
            if not self.silent:
                print(f"L_{i+1}: ", end='')
                print_bin(L, 32, 4)
                print(f"R_{i+1}: ", end='')
                print_bin(R, 32, 4)
                print()
        out = (R << 32) | L
        if not self.silent:
            print("RL: ", end='')
            print_bin(out, 64, 4)
        return permute(self.IP_inv, out, 64)
