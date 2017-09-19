module rippleAdder(in, out);
	input [13:0]in;
	output [6:0]out;
	wire connection_1, connection_2, connection_3,connection_4,connection_5,connection_6;
	
	full_adder f0(in[0],in[7],1'b0,connection_1,out[0]);
	full_adder f1(in[1],in[8],connection_1,connection_2,out[1]);
	full_adder f2(in[2],in[9],connection_2,connection_3,out[2]);
	full_adder f3(in[3],in[10],connection_3,connection_4,out[3]);
	full_adder f4(in[4],in[11],connection_4,connection_5,out[4]);
	full_adder f5(in[5],in[12],connection_5,connection_6,out[5]);
	full_adder f6(in[6],in[13],connection_6,connection_7,out[6]);
	

endmodule 

module full_adder(A, B, cin, cout, S);
	output S;
	output cout;
	input A;
	input B;
	input cin;
	wire w1;
	
	assign w1 = A & ~B | ~A & B;
	mux2to1 m0(B,cin,w1,cout);
	assign S = cin & ~w1 | ~cin & w1;
	
endmodule
	
module mux2to1(x, y, s, m);
    input x; //selected when s is 0
    input y; //selected when s is 1
    input s; //select signal
    output m; //output
  
    assign m = s & y | ~s & x;
    // OR
    // assign m = s ? y : x;

endmodule
