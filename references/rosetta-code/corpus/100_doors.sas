/* Source: https://rosettacode.org/wiki/100_doors
   Rosetta Code task '100 doors', page revision 410483.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:04:55Z. */

data _null_;
   open=1;
   close=0;
   array Door{100};
   do Pass = 1 to 100;
      do Current = Pass to 100 by Pass;
         if Door{Current} ne open 
            then Door{Current} = open;
            else Door{Current} = close;
      end;
   end;
   NumberOfOpenDoors = sum(of Door{*});
   put "Number of Open Doors:  " NumberOfOpenDoors; 
run;
