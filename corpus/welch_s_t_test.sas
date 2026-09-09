/* Source: https://rosettacode.org/wiki/Welch%27s_t-test
   Rosetta Code task 'Welch's t-test', page revision 401158.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:35Z. */


/* --- Welch's t-test: example 1 of 2 --- */

data tbl;
input value group @@;
cards;
3 1 4 1 1 1 2.1 1 490.2 2 340 2 433.9 2
;
run;

proc ttest data=tbl;
class group;
var value;
run;

/* --- Welch's t-test: example 2 of 2 --- */

proc iml;
use tbl;
read all var {value} into x where(group=1);
read all var {value} into y where(group=2);
close tbl;
n1 = nrow(x);
n2 = nrow(y);
v1 = var(x);
v2 = var(y);
t = (mean(x)-mean(y))/(sqrt(v1/n1+v2/n2));
df = (v1/n1+v2/n2)**2/(v1**2/(n1**2*(n1-1))+v2**2/(n2**2*(n2-1)));
p = 2*probt(-abs(t), df);
print t df p;
quit;
