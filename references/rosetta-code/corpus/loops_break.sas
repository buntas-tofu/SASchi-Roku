/* Source: https://rosettacode.org/wiki/Loops/Break
   Rosetta Code task 'Loops/Break', page revision 409014.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:11Z. */

data _null_;
do while(1);
   n=floor(uniform(0)*20);
   put n;
   if n=10 then leave;    /* 'leave' to break a loop */
end;
run;
