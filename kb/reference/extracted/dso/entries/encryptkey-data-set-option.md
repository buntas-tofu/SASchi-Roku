---
status: "generated"
entry: "ENCRYPTKEY= Data Set Option"
docset: "dso"
page: 27
physical_page: 39
category: "Data Set Control Use only with SAS 9.4 or later. Use only with AES-encrypted data files."
type: ""
valid_in: "DATA step and PROC steps"
---

ENCRYPTKEY= Data Set Option
Specifies a key value for AES (Advanced Encryption Standard) encryption.

Valid in:       DATA step and PROC steps
Category:       Data Set Control
Range:          1 to 64 bytes
Restrictions:   Use in the Compute Server, but not in CAS.
                Use only with SAS 9.4 or later.
                Use only with AES-encrypted data files.
Note:           Check your log after this operation to ensure encryption key security. For more
                information, see “Blotting Passwords and Encryption Key Values” in SAS
                Programmer’s Guide: Essentials.




                Syntax
                ENCRYPTKEY=key-value


                Syntax Description
                key-value
                   assigns an encrypt key value. You must specify the ENCRYPTKEY= data set
                   option when you are using ENCRYPT=AES or ENCRYPT=AES2 unless you are
                   creating a data set in a metadata-bound library with a recorded key. The key
                   value can be up to 64 bytes long. To create an ENCRYPTKEY= key value with or
                   without quotation marks, follow these rules:

                   No quotation marks:
                      n use alphanumeric characters and underscores only

                       n can be up to 64 bytes long

                       n use uppercase and lowercase letters
