/* Source: https://rosettacode.org/wiki/Loops/Do-while
   Rosetta Code task 'Loops/Do-while', page revision 408099.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:12Z. */

/* using DO UNTIL so that the loop executes at least once */
data _null_;
n=0;
do until(mod(n,6)=0);
    n+1;
    put n;
end;
run;
