/* Source: https://rosettacode.org/wiki/Archimedean_spiral
   Rosetta Code task 'Archimedean spiral', page revision 403755.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:04:56Z. */

data xy;
h=constant('pi')/40;
do i=0 to 400;
    t=i*h;
    x=(1+t)*cos(t);
    y=(1+t)*sin(t);
    output;
end;
keep x y;
run;

proc sgplot;
series x=x y=y;
run;
