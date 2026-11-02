---
status: "generated"
entry: "FILECLOSE= Data Set Option"
docset: "dso"
page: 32
physical_page: 44
category: "Miscellaneous"
type: ""
valid_in: "DATA step and PROC steps"
---

FILECLOSE= Data Set Option
Specifies how a tape is positioned when a SAS data set is closed.

Valid in:         DATA step and PROC steps
Category:         Miscellaneous
Restriction:      Use in the Compute Server, but not in CAS.
See:              FILECLOSE= Data Set Option in the documentation for the UNIX operating
                  environment.
CAUTION:          The option values are not recognized by all operating environments. Additional
                  values are available on some operating environments. For more information about using
                  SAS libraries that are stored on tape, see the SAS documentation for your operating
                  environment.




                  Syntax
                  FILECLOSE=DISP | LEAVE | REREAD | REWIND


                  Syntax Description
                  DISP
                     positions the tape volume according to the disposition that is specified in the
                     operating environment's control language.
                  LEAVE
                    positions the tape at the end of the file that was recently processed. Use
                    FILECLOSE=LEAVE if you are not repeatedly accessing the same files in a SAS
                    program, but you are accessing one or more subsequent SAS files on the same
                    tape.

                  REREAD
                    positions the tape volume at the beginning of the file that was recently
                    processed. Use FILECLOSE=REREAD if you are accessing the same SAS data
                    set on tape several times in a SAS program.
