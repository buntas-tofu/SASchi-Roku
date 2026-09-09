/* Source: https://rosettacode.org/wiki/Palindrome_detection
   Rosetta Code task 'Palindrome detection', page revision 410537.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:17Z. */


/* --- Palindrome detection: example 1 of 3 --- */

The macro "palindro" has two parameters: string and ignorewhitespace.
  string is the expression to be checked.
  ignorewhitespace, (Y/N), determines whether or not to ignore blanks and punctuation.
This macro was written in SAS 9.2.  If you use a version before SAS 9.1.3, 
the compress function options will not work.

/* --- Palindrome detection: example 2 of 3 --- */

 
%MACRO palindro(string, ignorewhitespace);
  DATA _NULL_;
    %IF %UPCASE(&ignorewhitespace)=Y %THEN %DO;
/* The arguments of COMPRESS (sp) ignore blanks and puncutation */
/* We take the string and record it in reverse order using the REVERSE function. */
      %LET rev=%SYSFUNC(REVERSE(%SYSFUNC(COMPRESS(&string,,sp)))); 
      %LET string=%SYSFUNC(COMPRESS(&string.,,sp));
    %END;

    %ELSE %DO;
      %LET rev=%SYSFUNC(REVERSE(&string));
    %END;
    /*%PUT rev=&rev.;*/
    /*%PUT string=&string.;*/

/* Here we determine if the string and its reverse are the same. */
    %IF %UPCASE(&string)=%UPCASE(&rev.) %THEN %DO;
      %PUT TRUE;
    %END;
    %ELSE %DO;
      %PUT FALSE; 
    %END;
  RUN;
%MEND;

/* --- Palindrome detection: example 3 of 3 --- */

%palindro("a man, a plan, a canal: panama",y);

TRUE

NOTE: DATA statement used (Total process time):
      real time           0.00 seconds
      cpu time            0.00 seconds

%palindro("a man, a plan, a canal: panama",n);

FALSE

NOTE: DATA statement used (Total process time):
      real time           0.00 seconds
      cpu time            0.00 seconds
