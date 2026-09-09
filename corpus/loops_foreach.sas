/* Source: https://rosettacode.org/wiki/Loops/Foreach
   Rosetta Code task 'Loops/Foreach', page revision 409015.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:13Z. */

/* Initialize an array with integers 1 to 10, and print their sum */
data _null_;
array a a1-a10;
n=1;
do over a;
  a=n;
  n=n+1;
end;
s=sum(of a{*});
put s;
run;
