data work.want;
  set work.have;
  prev = lag(value);
  prev2 = lag2(value);
  change = value - prev;
run;
