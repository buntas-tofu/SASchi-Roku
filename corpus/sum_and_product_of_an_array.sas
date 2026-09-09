/* Source: https://rosettacode.org/wiki/Sum_and_product_of_an_array
   Rosetta Code task 'Sum and product of an array', page revision 408601.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:31Z. */

data _null_;
   array a{*} a1-a100;
   do i=1 to 100;
      a{i}=i*i;
   end;
   b=sum(of a{*});
   put b c;
run;
