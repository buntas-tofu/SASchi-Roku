/* Source: https://rosettacode.org/wiki/Merge_and_aggregate_datasets
   Rosetta Code task 'Merge and aggregate datasets', page revision 387554.
   License: GFDL 1.2 (Rosetta_Code:Copyrights). Retrieved 2026-09-08T14:05:15Z. */

  %let datefmt=E8601DA10.;
  data patient;
      infile "patient.csv" dsd dlm=',';
      attrib
          id length=4
          lastname length=$10; 
      input id lastname;
  data visit;
      infile "visit.csv" dsd dlm=',';
      attrib
          id length=4
          date informat=&datefmt format=&datefmt
          score length=8; 
      input id date score;
  proc sql;
      select * from 
          (select id, max(date) format=&datefmt as max_date, sum(score) as sum_score,
          	avg(score) as avg_score from visit group by id)
          natural right join patient
          order by id;
