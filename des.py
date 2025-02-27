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
        temp: int = value & (1 << size - index)
    temp >>= (size - index)
    temp <<= i
    i -= 1
    result |= temp
    return result


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
    round_keys: list[int] = []

    def __init__(self, _key: int):
        self.key = _key

    def generate_round_keys():
        '''
        Uses the master key to generate the 16 round keys
        '''

    def encrypt(self):
        pass
