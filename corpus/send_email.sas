/* Source: https://rosettacode.org/wiki/Send_email
   Rosetta Code task 'Send email', page revision 408858.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:24Z. */

filename msg email
   to="afriend@someserver.com"
   cc="anotherfriend@somecompany.com"
   subject="Important message"
;

data _null_;
   file msg;
   put "Hello, Connected World!";
run;
