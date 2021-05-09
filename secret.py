#! /usr/bin/env python3
import secrets
from base64 import b64encode, b64decode
import argparse


def split_secret_bytes(secret):
    """
    Split secret into two shares that can be combined to
    recreate the secret.

    secret: The secret byte string.
    return: Tuple of two byte strings.
    """
    share_a = secrets.token_bytes(len(secret))
    share_b = xor(secret, share_a)
    return share_a, share_b


def split_secret(secret):
    """
    Interface to split_secret_bytes() that works with strings.
    """
    secret_bytes = secret.encode('utf8')
    shares = split_secret_bytes(secret_bytes)
    return tuple(map(bytes2storestring, shares))


def restore_secret(share_a, share_b):
    """
    Combine secret shares to obtain the secret value.

    Shares are recieved as store strings. They converted to
    bytes, combined, and decoded to a string. This function
    can only work with secrets that are valid utf8.
    """
    a = storestring2bytes(share_a)
    b = storestring2bytes(share_b)
    return xor(a, b).decode('utf8')


def xor(a, b):
    """
    xor two byte sequences
    """
    if len(a) != len(b):
        raise ValueError('a and b must be the same length')
    return bytes(x ^ y for x, y in zip(a, b))


def join_command(share_a, share_b, **kwargs):
    secret = restore_secret(share_a, share_b)
    print(f'Combining {share_a} and {share_b} to get {secret}')


def split_command(secret, **kwargs):
    share_a, share_b = split_secret(secret)
    print(f"Secret shares: {share_a} {share_b}")


def splitn_command(secret, n, **kwargs):
    pass


def bytes2storestring(b):
    """
    Convert abitrary bytes to a printable string, the storage format
    for handling secret shares.
    """
    # TODO add checksum byte(s)
    return b64encode(b).decode('utf8')


def storestring2bytes(string):
    """
    Convert storage string to bytes. string must be using the storage
    format -- usually created by bytes2storestring(bytes)
    """
    # TODO handle errors
    return b64decode(string.encode('utf8'))


def get_args():
    p = argparse.ArgumentParser(
        prog="secret",
        description="Split secrets into shares and combine shares into secrets"
    )

    # A print_help() that can be called with arguments. Arguments are ignored.
    def print_help(*args, **kwargs):
        p.print_help()
    p.set_defaults(sub_cmd=print_help)

    p_sub = p.add_subparsers(title='Sub commands')

    # Combine
    p_join = p_sub.add_parser('combine')
    p_join.add_argument('share_a')
    p_join.add_argument('share_b')
    p_join.set_defaults(sub_cmd=join_command)

    # Split
    p_split = p_sub.add_parser('split')
    p_split.add_argument('secret')
    p_split.set_defaults(sub_cmd=split_command)

    # Create pdf
    p_splitn = p_sub.add_parser('splitn')
    p_splitn.add_argument('secret')
    p_splitn.add_argument('n')
    p_splitn.set_defaults(sub_cmd=splitn_command)

    return p.parse_args()


def main():
    args = get_args()
    args.sub_cmd(**vars(args))


if __name__ == '__main__':
    main()
