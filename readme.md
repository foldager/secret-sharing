
# Secret sharing

Split recovery keys and other secrets. Prin

Create pdfs for printing. Any two sheets of paper are and prindocuments 

- [x] Secret splitting script
- [x] Secret joining script
- [ ] Script that takes secret and creates multipage PDF. Any two pages can be used to re-create the secret.
- [ ] Add metadata to document
  - [ ] Secret name
  - [ ] Description
  - [ ] Owner
  - [ ] Full list of confidants (Optional)
  - [ ] Selfdocumenting.
    - [ ] High level description of algorithm
    - [ ] Hand derived example(s)
- [ ] Repo documentation
  - [ ] ...
- [x] Unit tests
- [ ] Continous testing (github actions)
- [ ] Checksum in storage string
- [ ] Error handling
  - [ ] Store string invalid -- cannot decode
  - [ ] combining: Secret is not valid utf8



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

