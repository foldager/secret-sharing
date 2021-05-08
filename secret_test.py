
from secret import split_secret, join_secret, encode, decode

def test_join():
    s1 = b'y$\x98\x14s$R:\x975\xb9'
    s2 = b'1A\xf4x\x1c\x04%U\xe5Y\xdd'
    assert join_secret(s1, s2) == b'Hello world'


def test_split_and_join():
    secret = b'Hello!'
    s1, s2 = split_secret(secret)
    assert secret == join_secret(s2, s1)


def test_encode_decode():
    s = '👍 Hello 🐣 world 👍'
    b = s.encode('utf8')
    assert b == decode(encode(b))
