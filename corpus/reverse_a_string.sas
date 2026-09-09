/* Source: https://rosettacode.org/wiki/Reverse_a_string
   Rosetta Code task 'Reverse a string', page revision 410541.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:23Z. */

data _null_;
length a b $11;
a="I am Legend";
b=reverse(a);
put a;
put b;
run;
