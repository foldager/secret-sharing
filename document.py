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

The secret *{secret_name}* has been split into shares. The secret can be
recovered with access to two of the {n_sheet} sheets.

The secret has been split into paired shares, where both shares
are needed to recover the secret. A single share by itself does
reveal any information about the secret. This sheet only contains
single shares (*share value*) and the other share can be found on
the *other sheet*. To validate that two shares make a pair,
check that they have the same *share ID*.

Use the script found at
https://github.com/foldager/secret-sharing
to combine a pair of shares to recover the secret.


.. table:: Secret shares for sheet {sheet_id}
    :widths: auto

{create_table(records)}

Example: combine two shares to recover secret

.. code-block:: console

    % ./secret.py combine DcBYCyYI820F4en0Pfw1E540Pwg= YLl1fUN6ikB2hIqGWIgYZf9YSm0=
    my-very-secret-value
"""
