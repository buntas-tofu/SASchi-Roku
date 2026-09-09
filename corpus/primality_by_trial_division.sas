/* Source: https://rosettacode.org/wiki/Primality_by_trial_division
   Rosetta Code task 'Primality by trial division', page revision 409888.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:20Z. */

data primes;
do n=1 to 1000;
  link primep;
  if primep then output;
end;
stop;

primep:
if n < 4 then do;
  primep=n=2 or n=3;
  return;
end;
primep=0;
if mod(n,2)=0 then return;
do k=3 to sqrt(n) by 2;
  if mod(n,k)=0 then return;
end;
primep=1;
return;
keep n;
run;
