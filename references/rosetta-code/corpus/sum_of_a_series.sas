/* Source: https://rosettacode.org/wiki/Sum_of_a_series
   Rosetta Code task 'Sum of a series', page revision 406317.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:31Z. */

data _null_;
s=0;
do n=1 to 1000;
   s+1/n**2;        /* s+x is synonym of s=s+x */
end;
e=s-constant('pi')**2/6;
put s e;
run;
