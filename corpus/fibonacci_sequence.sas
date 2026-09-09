/* Source: https://rosettacode.org/wiki/Fibonacci_sequence
   Rosetta Code task 'Fibonacci sequence', page revision 410577.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:02Z. */


/* --- Fibonacci sequence: example 1 of 2 --- */

data fib;
    a=0;
    b=1;
    do n=0 to 20;
       f=a;
       output;
       a=b;
       b=f+a;
    end;
    keep n f;
run;

/* --- Fibonacci sequence: example 2 of 2 --- */

options cmplib=work.f;

proc fcmp outlib=work.f.p;
    function fib(n);
    if n = 0 or n = 1
        then return(1);
        else return(fib(n - 2) + fib(n - 1));
    endsub;
run;

data _null_;
    x = fib(5);
    put 'fib(5) = ' x;
run;
