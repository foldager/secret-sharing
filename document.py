from tabulate import tabulate


def create_table(records):
    table = tabulate(
        records,
        headers=['Other sheet', 'Share ID', 'Share value'],
        tablefmt='rst',
    )
    # Add indent
    table = '\n'.join(f'    {li}' for li in table.split('\n'))
    return table


def create_page(secret_name, sheet_id, n_sheet, records):
    title = f'SECRET: {secret_name}'
    subtitle = f'Sheet {sheet_id}'
    n = max(len(title), len(subtitle))
    return f"""\
{'=' * n}
{title}
{'=' * n}
{subtitle}
{'-' * n}

The secret *{secret_name}* has been split into shares distributed accross
{n_sheet} sheets.
The secret can be recovered with access to 2 of the {n_sheet} sheets.

To recover the secret, combine two shares that have the same *share ID*
from different sheets.

Use the script found at
https://github.com/foldager/secret-sharing
to combine a pair of shares to recover the secret.


.. table:: Secret shares for sheet {sheet_id}
    :widths: auto

{create_table(records)}

Example: combine two shares to recover secret

.. code-block:: console

    % ./secret.py combine NxUXzyq66ZTotfg8n6Z0JoUrhDX6 Wmw6uU/IkLmb0JtO+tJZUORH8VCm
    my-very-secret-value

.. raw:: pdf

    PageBreak

Algotrithm
----------

The secrets are conceptually constructed using a `one-time pad`_.
Conceptually one share is the pad and the other the imprint/ciphertext.
Which share is the pad, and which is the ciphertext is a technical detail
when creating the shares. It does not matter when reconstructing the
plaintext, as they can be switched and the result is the same.

.. _one-time pad: https://en.wikipedia.org/wiki/One-time_pad


.. table:: Combine share A and A`. Secret value: Hi!
    :widths: auto

    ========================  ==========  ===========   ==============
    Description                Byte 1          Byte 2        Byte 3
    ========================  ==========  ===========   ==============
       Share A                1100 0011    0001 0111     ``0001 0100``
       Share A'               1000 1011    0111 1110     ``0010 0101``
    Plaintext (A ``xor`` A')  0100 1000    0110 1001     ``0010 0001``
    Ascii lookup                   H             i             !
    ========================  ==========  ===========   ==============

The secret value is obtained by combining the bits of the two
shares using the `xor function`_. See above table for an example
of how to ``xor`` two shares to get the plaintext bytes.
Use an `ASCII lookup table`_ to convert the bytes to characters.


.. _xor function: https://en.wikipedia.org/wiki/Exclusive_or

.. _ASCII lookup table: https://en.wikipedia.org/wiki/ASCII#Printable_characters


Getting the share bytes
-----------------------

You might have noticed that the secret shares on the first page are not written
in binary. Binary is inefficint/cumbersome to handle, as it takes a lot of error
prone typing.
The shares are instead base64_ encoded with the last byte used for checksum.
The shares must be decoded before their bytes can be ``xor``'ed.
For the
the purpose of getting the share bytes, the last byte can be discarded. The program uses
the checksum byte to validate each share is entered correctly.
See the base64 wiki page for how to decode by hand, or use standard terminal
commands.

Command to decode the share ``wxcUwA==``
to the bytes ``11000011 00010111 00010100``.
Byte 4 is the checksum byte, and is discarded.
The the last line is added to annotate the output of the command.

.. code-block:: console

    % echo wxcUwA== | base64 -d | xxd -b -d
    00000000: 11000011 00010111 00010100 11000000
    index     byte 1   byte 2   byte 3   byte 4

.. _base64: https://en.wikipedia.org/wiki/Base64

.. target-notes::

"""
