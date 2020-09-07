class Alphabet:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    @classmethod
    def get(cls, item):
        return cls.alphabet[item]

    @classmethod
    def index(cls, lettre):
        return cls.alphabet.index(lettre)