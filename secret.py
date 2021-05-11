#! /usr/bin/env python3
import secrets
from base64 import b64encode, b64decode
import argparse
from tabulate import tabulate
from rst2pdf.createpdf import RstToPdf
from random import shuffle


RST_PAGE_JOINER = """

.. raw:: pdf

    PageBreak

"""


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


def splitn_command(secret, n, out_file, **kwargs):
    """
    N shares so that any two shares can be combined to obtain the secret.
    Each share will contain n-1 share values, each matching a different share.
    The secret can be obtained by combining two share values with the same
    share ID.

    The share tables and instructions are saved to pdf.
    """

    ids = list(range(100, 999))
    n_share_values = (n * n) / 2 - n
    if len(ids) < n_share_values:
        raise ValueError(
            f"Share ID space too small for n={n}. Choose smaller n."
        )
    shuffle(ids)

    shares = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            share_a, share_b = split_secret(secret)
            share_id = ids.pop()
            shares[i].append([share_id, f'``{share_a}``'])
            shares[j].append([share_id, f'``{share_b}``'])

    # Sort share values by ID and format ID.
    for share in shares:
        share.sort(key=lambda x: x[0])
        for record in share:
            record[0] = f'#{record[0]}'

    pages = [create_page(share) for share in shares]
    rst_doc = join_pages(pages)

    RstToPdf().createPdf(
        text=rst_doc,
        output=out_file
    )


def create_page(records):
    table = tabulate(
        records, headers=['Share ID', 'Share value'], tablefmt='rst',
    )
    return table


def join_pages(pages):
    return RST_PAGE_JOINER.join(pages)


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
    p_splitn = p_sub.add_parser('split-to-pdf')
    p_splitn.add_argument('secret')
    p_splitn.add_argument('n', type=int)
    p_splitn.add_argument(
        '--out-file', '-o', default='secret_shares.pdf'
    )
    p_splitn.set_defaults(sub_cmd=splitn_command)

    return p.parse_args()


def main():
    args = get_args()
    args.sub_cmd(**vars(args))


if __name__ == '__main__':
    main()
