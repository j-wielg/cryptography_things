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
    round_keys: list[int] = None

    def __init__(self, _key: int):
        self.key = _key

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
            self.round_keys.append(temp)

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

    def encrypt_block(self, block: int) -> int:
        '''
        Encrypts a 64-bit block of data using the DES algorithm
        '''
        if not self.round_keys:
            self.generate_round_keys()
        block = permute(self.IP, block, 64)
        L = (block & 0xFFFFFFFF00000000) >> 32
        R = block & 0xFFFFFFFF
        for i in range(16):
            temp = R
            R = L ^ self.f(R, self.round_keys[i])
            L = temp
