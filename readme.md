
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
  - [ ] Selfdocumenting. Must contain enough detail that the secret can be recovered without access to script.
    - [ ] High level description of algorithm
      - [ ] bytes to b64 store string
      - [ ] checksum byte
    - [ ] Hand derived example(s)
- [ ] Repo documentation
  - [ ] ...
- [x] Unit tests
- [x] Continous testing (github actions)
- [x] Checksum in storage string
- [x] Option to no leak secret in shell history
- [ ] Error handling
  - [ ] Store string invalid -- cannot decode
  - [ ] combining: Secret is not valid utf8
  - [ ] Warn/error if the two shares are identical



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

```console
% ./secret.py combine txhEAu8Dm9OdZ5iKzPukpDy4vIP1NqMOuA== +3crac9h/rv0CfyquJPBhE/Q2efVxjyqFQ==
Look behind the shed 🤭
```
