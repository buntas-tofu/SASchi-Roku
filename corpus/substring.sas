/* Source: https://rosettacode.org/wiki/Substring
   Rosetta Code task 'Substring', page revision 409497.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:29Z. */

data _null_;
   a="abracadabra";
   b=substr(a,2,3); /* first number is position, starting at 1,
                       second number is length */
   put _all_;
run;
