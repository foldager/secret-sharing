#! /usr/bin/env python3
import sys
import secrets
from base64 import b64encode, b64decode
import argparse

def split_secret(secret):
    """
    secret: The secret byte string.
    return: tuple of two bytestrings.
    """
    # secret, pad, and the two xor'ed. All as bytes.
    pad = secrets.token_bytes(len(secret))
    imprint = xor(pad, secret)

    return pad, imprint


def join_secret(a, b):
    return xor(a, b)


def xor(a, b):
    """
    xor two byte sequences
    """
    if len(a) != len(b):
        raise ValueError('a and b must be the same length')    
    return bytes(x ^ y for x, y  in zip(a, b))

def encode(b):
    return b64encode(b)

def decode(b):
    return b64decode(b)

def main_dep():

    # Type: bytes
    secret = sys.argv[1].encode('utf8')

    s1, s2 = split_secret(secret)
    secret = join_secret(s1, s2)
    print(f'Combining {s1} and {s2} to get {secret}')


    print(f'Combining {encode(s1)} and {encode(s2)} to get {secret}')


def join_command(args):
    a = decode(args.partA.encode('utf8'))
    b = decode(args.partB.encode('utf8'))
    secret = join_secret(a, b)

    print(f'Combining {args.partA} and {args.partB} to get {secret.decode("utf8")}')


def split_command(args):
    secret = args.secret.encode('utf8')
    partA, partB = split_secret(secret)

    strA = encode(partA).decode('utf8')
    strB = encode(partB).decode('utf8')
    print(f"Secret shares: {strA} {strB}")


def get_args():
    p = argparse.ArgumentParser(
        "secret",
        "Split secrets into parts and join parts into secrets",
    )

    p_sub = p.add_subparsers(title='The Joiner') # what??
    p_join = p_sub.add_parser('join')
    p_join.add_argument('partA')
    p_join.add_argument('partB')
    p_join.set_defaults(sub_cmd=join_command)

    p_split = p_sub.add_parser('split')

    p_split.add_argument('secret')
    p_split.set_defaults(sub_cmd=split_command)

    return p.parse_args()


def main():
    args = get_args()
    args.sub_cmd(args)


if __name__ == '__main__':
    main()