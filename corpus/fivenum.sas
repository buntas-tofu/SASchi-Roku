/* Source: https://rosettacode.org/wiki/Fivenum
   Rosetta Code task 'Fivenum', page revision 407440.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:02Z. */

/* build a dataset */
data test;
do i=1 to 10000;
	x=rannor(12345);
	output;
end;
keep x;
run;

/* compute the five numbers */
proc means data=test min p25 median p75 max;
var x;
run;
