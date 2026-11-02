/* Source: https://rosettacode.org/wiki/Trigonometric_functions
   Rosetta Code task 'Trigonometric functions', page revision 408550.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:33Z. */

data _null_;
pi = 4*atan(1);
deg = 30;
rad = pi/6;
k = pi/180;
x = 0.2;

a = sin(rad);
b = sin(deg*k);
put a b;

a = cos(rad);
b = cos(deg*k);
put a b;

a = tan(rad);
b = tan(deg*k);
put a b;

a=arsin(x);
b=arsin(x)/k;
put a b;

a=arcos(x);
b=arcos(x)/k;
put a b;

a=atan(x);
b=atan(x)/k;
put a b;
run;
