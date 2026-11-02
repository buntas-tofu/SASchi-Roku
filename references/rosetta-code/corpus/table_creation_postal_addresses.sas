/* Source: https://rosettacode.org/wiki/Table_creation/Postal_addresses
   Rosetta Code task 'Table creation/Postal addresses', page revision 408583.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:32Z. */

PROC SQL;
CREATE TABLE ADDRESS 
(
ADDRID CHAR(8)
,STREET CHAR(50) 
,CITY CHAR(25)
,STATE CHAR(2)
,ZIP  CHAR(20)
) 
;QUIT;
