from secret import (
    split_secret,
    restore_secret,
    xor,
    storestring2bytes,
    bytes2storestring,
)


def test_join_bytes():
    s1 = b'y$\x98\x14s$R:\x975\xb9'
    s2 = b'1A\xf4x\x1c\x04%U\xe5Y\xdd'
    assert xor(s1, s2) == b'Hello world'


def test_split_and_restore():
    secret = 'Hello🤪👍'
    s1, s2 = split_secret(secret)
    assert secret == restore_secret(s2, s1)


def test_encode_decode():
    s = 'x82Km0R/s0DDIpM='
    b = storestring2bytes(s)
    assert s == bytes2storestring(b)
