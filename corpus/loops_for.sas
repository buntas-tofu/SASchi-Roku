/* Source: https://rosettacode.org/wiki/Loops/For
   Rosetta Code task 'Loops/For', page revision 408391.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:12Z. */

data _null_;
length a $5;
do n=1 to 5;
  a="*";
  do i=2 to n;
    a=trim(a) !! "*";
  end;
  put a;
end;
run;

/* Possible without the inner loop. Notice TRIM is replaced with STRIP,
otherwise there is a blank space on the left */

data _null_;
length a $5;
do n=1 to 5;
  a=strip(a) !! "*";
  put a;
end;
run;
