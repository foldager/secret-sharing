![Build status](https://github.com/foldager/secret-sharing/actions/workflows/qa.yml/badge.svg)

# Secret sharing 

Split recovery keys and other secrets.

Create pdfs for printing. Any two sheets of paper are and prindocuments 


## Task list
- [x] Secret splitting script
- [x] Secret joining script
- [x] Script that takes secret and creates multipage PDF. Any two pages can be used to re-create the secret.
- [ ] Add metadata to document
  - [ ] Secret name
  - [ ] Description
  - [ ] Owner
  - [ ] Full list of confidants (Optional)
  - [x] Selfdocumenting. Must contain enough detail that the secret can be recovered without access to script.
    - [ ] High level description of algorithm
      - [ ] bytes to b64 store string
      - [ ] checksum byte
    - [ ] Hand derived example(s)
  - [ ] Make a single pdf https://stackoverflow.com/questions/3444645/merge-pdf-files
- [ ] Repo documentation
  - [ ] ...
- [x] Unit tests
- [x] Continous testing (github actions)
- [x] Checksum in storage string
- [x] Option to no leak secret in shell history
- [x] Error handling
  - [x] Store string invalid -- cannot decode
  - [x] combining: Secret is not valid utf8
  - [x] Warn/error if the two shares are identical
- [ ] Make pip-installable
- [ ] Install CLI entrypoint
- [ ] Make log(n) share pairs instead of n**2


## Encoding

```

Input/output from app:
    Secret: str()
    splits: str(b64(checksum()))

Work with:
    bytes


    encode 

Operations

split(s)
join(s1, s2)

encode: b -> b
decode: b -> b

# Python Strings
encode: string -> bytes
decode: bytes -> string
```

## Examples

The first example shows how to combine two secret shares to re-construct the secret.
```console
% ./secret.py combine 6vn3jt/YF2T8CFFmyarX0bd7cM7oADKkRvI= ppaY5f+6cgyVZjVGvcKy8cQTFarI8K0A69w=
Look behind the shed 🤭
```

Split a secret in two and join the parts
```console
% ./secret.py split "short secret"
Secret shares: qUCg1KvIkeSKf0YFPQ== 2ijPpt/o4oHpDSNxeQ==

% ./secret.py combine qUCg1KvIkeSKf0YFPQ== 2ijPpt/o4oHpDSNxeQ==
short secret
```
Mistyping a secret share will likely be caught by the checksum
```console
% ./secret.py combine QUCg1KvIkeSKf0YFPQ== 2ijPpt/o4oHpDSNxeQ==
Store string 'QUCg1KvIkeSKf0YFPQ==' is corrupt or not entered correctly.
```
... Or the share will not be a valid b64 string
```console
% ./secret.py combine UCg1KvIkeSKf0YFPQ== 2ijPpt/o4oHpDSNxeQ==
Invalid base64-encoded string: number of data characters (17) cannot be 1 more than a multiple of 4
Invalid/corrupted store string: UCg1KvIkeSKf0YFPQ==

% ./secret.py combine U-Cg1KvIkeSKf0YFPQ== 2ijPpt/o4oHpDSNxeQ==
Non-base64 digit found
Invalid/corrupted store string: U-Cg1KvIkeSKf0YFPQ==
```

In case you have gotten your hands on two secret shares that combine to bytes
that are not valid utf-8, you will get a warning like this:
```console
% ./secret.py combine 4q1P +Fig
Warning: The secret is not valid utf-8.
python bytes representation: b'\x1a\xf5'
Best effort uft-8 decoding:
�
```


