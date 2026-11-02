/* Source: https://rosettacode.org/wiki/Random_numbers
   Rosetta Code task 'Random numbers', page revision 407260.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:22Z. */

/* Generate 1000 random numbers with mean 1 and standard deviation 0.5. 
  SAS version 9.2 was used to create this code.*/

data norm1000;
  call streaminit(123456); 
/* Set the starting point, so we can replicate results. 
   If you want different results each time, comment the above line. */
  do i=1 to 1000;
    r=rand('normal',1,0.5);
    output;
  end;
run;
