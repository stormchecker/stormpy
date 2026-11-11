// Symmetric random walk on [0..N] starting in the middle.
dtmc

const int N;

module walk
	x : [0..N] init N/2;

	[] 0 < x & x < N -> 0.5 : (x'=x-1) + 0.5 : (x'=x+1);
	[] x = 0 | x = N -> 1 : true;
endmodule

label "goal" = x = N;
