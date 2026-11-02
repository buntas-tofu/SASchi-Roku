/* Source: https://rosettacode.org/wiki/Sieve_of_Eratosthenes
   Rosetta Code task 'Sieve of Eratosthenes', page revision 410247.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:24Z. */

proc iml;
start sieve(n);
    a = J(n,1);
    a[1] = 0;
    do i = 1 to n;
        if a[i] then do;
            if i*i>n then return(a);
            a[i*(i:int(n/i))] = 0;
        end;
    end;
finish;

a = loc(sieve(1000))`;
create primes from a;
append from a;
close primes;
quit;
