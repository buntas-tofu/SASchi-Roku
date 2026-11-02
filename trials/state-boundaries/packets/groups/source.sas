data work.want;
  set work.have;
  by region account;
  raw_prev=lag(value);
  prev=raw_prev;
  if first.account then prev=.;
  if first.region then total=100;
  total + value;
  first_region=first.region;
  last_region=last.region;
  first_account=first.account;
  last_account=last.account;
  keep row_id region account value raw_prev prev total
       first_region last_region first_account last_account;
run;
