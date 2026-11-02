/* Source: https://rosettacode.org/wiki/Bitwise_operations
   Rosetta Code task 'Bitwise operations', page revision 406458.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:04:57Z. */

/* rotations are not available, but are easy to implement with the other bitwise operators */
data _null_;
   a=105;
   b=91;
   c=bxor(a,b);
   d=band(a,b);
   e=bor(a,b);
   f=bnot(a); /* on 32 bits */
   g=blshift(a,1);
   h=brshift(a,1);
   put _all_;
run;
