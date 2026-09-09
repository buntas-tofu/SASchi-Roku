/* Source: https://rosettacode.org/wiki/Day_of_the_week
   Rosetta Code task 'Day of the week', page revision 409981.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:00Z. */

data _null_;
do y=2008 to 2121;
    a=mdy(12,25,y);
    if weekday(a)=1 then put y;
end;
run;

/* 2011 2016 2022 2033 2039 2044 2050 2061 2067
   2072 2078 2089 2095 2101 2107 2112 2118 */
