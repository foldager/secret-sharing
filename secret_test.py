from secret import (
    split_secret,
    restore_secret,
    xor,
    storestring2bytes,
    bytes2storestring,
    InvalidChecksum,
    InvalidStoreString,
)
import pytest


def test_join_bytes():
    s1 = b'y$\x98\x14s$R:\x975\xb9'
    s2 = b'1A\xf4x\x1c\x04%U\xe5Y\xdd'
    assert xor(s1, s2) == b'Hello world'


def test_restore():
    assert '🦀👀' == restore_secret('xjPi/Lx125Jr', 'NqxEfEzqShJc')


def test_split_and_restore():
    secret = 'Hello🤪👍'
    s1, s2 = split_secret(secret)
    assert secret == restore_secret(s2, s1)


def test_encode_decode():
    b = b'Hello world'
    s = bytes2storestring(b)
    assert b == storestring2bytes(s)


def test_storestring2bytes_err():
    s = 'x82Km0R/s0DDIpM='
    with pytest.raises(InvalidChecksum):
        storestring2bytes(s)


def test_storestring2bytes():
    b = b'Hello world'
    s = 'SGVsbG8gd29ybGQA'
    assert b == storestring2bytes(s)


def test_bytes2storestring():
    b = b'Hello world'
    s = 'SGVsbG8gd29ybGQA'
    assert s == bytes2storestring(b)


def test_restore_secret_invalid_unicode(capsys):
    restore_secret('4q1P', '+Fig')
    captured = capsys.readouterr()
    assert captured.err == (
        "Warning: The secret is not valid utf-8.\n"
        "python bytes representation: b'\\x1a\\xf5'\n"
    )
    assert captured.out == "Best effort uft-8 decoding:\n"


def test_storestring2bytes_invalid_b64():
    with pytest.raises(InvalidStoreString):
        storestring2bytes('****')
