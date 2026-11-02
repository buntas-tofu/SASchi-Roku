data work.want;
  merge work.left(in=l) work.right(in=r);
  by key;
  from_left=l;
  from_right=r;
  keep key left_seq right_seq a b shared from_left from_right;
run;
