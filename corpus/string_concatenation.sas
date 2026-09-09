/* Source: https://rosettacode.org/wiki/String_concatenation
   Rosetta Code task 'String concatenation', page revision 406325.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:26Z. */

data _null_;
   a="Hello,";
   b="World!";
   c=a !! " " !! b;
   put c;
   *Alternative using the catx function;
   c=catx (" ", a, b);
   put c;
run;
