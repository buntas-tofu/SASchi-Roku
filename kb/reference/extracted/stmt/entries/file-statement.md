---
status: "generated"
entry: "FILE Statement"
docset: "stmt"
page: 85
physical_page: 97
category: "CAS File-Handling"
type: "Executable"
valid_in: "DATA step"
---

FILE Statement
Specifies the current output file for PUT statements.

Valid in:        DATA step
Categories:      CAS
                 File-Handling
Type:            Executable
Restriction:     When SAS is in a locked-down state, the FILENAME statement is not available for
                 files that are not in the locked-down path list. For more information, see “SAS
                 Processing Restrictions for Servers in a Locked-Down State” in SAS Language
                 Reference: Concepts.
See:             FILE Statement under Windows, UNIX, and z/OS




                 Syntax
                 FILE file-specification <device-type> <options> <operating-environment-options>;


                 Arguments
                 file-specification
                     identifies an external file that the DATA step uses to write output from a PUT
                     statement. File-specification can have these forms:

                    'external-file'
                        specifies the physical name of an external file, which is enclosed in
                        quotation marks. The physical name is the name by which the operating
                        environment recognizes the file.

                    fileref
                        specifies the fileref of an external file.

                        Range         1 to 8 bytes

                        Restriction   This argument is not supported in a DATA step that runs in
                                      CAS.

                        Requirement   You must have associated fileref with an external file in a
                                      FILENAME statement or function in a previous step or in an
                                      appropriate operating environment command. The only way to
                                      assign fileref at run time is to use the FILEVAR= option in the
                                      FILE statement.

                        Note          If your fileref is associated with the EMAIL access method,
                                      additional options are available for the FILE statement. For a
