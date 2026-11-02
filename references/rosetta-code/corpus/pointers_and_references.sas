/* Source: https://rosettacode.org/wiki/Pointers_and_references
   Rosetta Code task 'Pointers and references', page revision 398361.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:19Z. */

/* Using ADDR to get memory address, and PEEKC / POKE. There is also PEEK for numeric values. */
data _null_;
length a b c $4;
adr_a=addr(a);
adr_b=addr(b);
adr_c=addr(c);
a="ABCD";
b="EFGH";
c="IJKL";
b=peekc(adr_a,1);
call poke(b,adr_c,1);
put a b c;
run;
