/* Source: https://rosettacode.org/wiki/Loops/While
   Rosetta Code task 'Loops/While', page revision 409850.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:14Z. */

data _null_;
n=1024;
do while(n>0);
  put n;
  n=int(n/2);
end;
run;
