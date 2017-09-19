// Part 2 skeleton

module project
	(
		CLOCK_50,						//	On Board 50 MHz
		// Your inputs and outputs here
        KEY,
        SW,
		  LEDR,
		// The ports below are for the VGA output.  Do not change.
		VGA_CLK,   						//	VGA Clock
		VGA_HS,							//	VGA H_SYNC
		VGA_VS,							//	VGA V_SYNC
		VGA_BLANK_N,						//	VGA BLANK
		VGA_SYNC_N,						//	VGA SYNC
		VGA_R,   						//	VGA Red[9:0]
		VGA_G,	 						//	VGA Green[9:0]
		VGA_B,   						//	VGA Blue[9:0]
		HEX0,
		HEX1,
		HEX2,
		HEX3
	);

	input			CLOCK_50;				//	50 MHz
	input   [9:0]   SW;
	input   [3:0]   KEY;

	// Declare your inputs and outputs here
	// Do not change the following outputs
	output			VGA_CLK;   				//	VGA Clock
	output			VGA_HS;					//	VGA H_SYNC
	output			VGA_VS;					//	VGA V_SYNC
	output			VGA_BLANK_N;				//	VGA BLANK
	output			VGA_SYNC_N;				//	VGA SYNC
	output	[9:0]	VGA_R;   				//	VGA Red[9:0]
	output	[9:0]	VGA_G;	 				//	VGA Green[9:0]
	output	[9:0]	VGA_B;   				//	VGA Blue[9:0]
	output [6:0] HEX0, HEX1, HEX2, HEX3;

	wire resetn;
	wire en;
	wire doneplot;
	assign resetn = 1'b1;
	assign en = 1'b1;

	// Create the colour, x, y and writeEn wires that are inputs to the controller.
	wire [2:0] colour;
	wire [2:0] colour_out;
	wire [6:0] x;
	wire [6:0] y_out;
	wire [6:0] x_out;
	wire [6:0] y;
	wire [6:0] lengthx;
	wire [6:0] lengthy;
	wire [5:0] cases;
	wire writeEn;
	output [9:0]LEDR;


	// Create an Instance of a VGA controller - there can be only one!
	// Define the number of colours as well as the initial background
	// image file (.MIF) for the controller.
	vga_adapter VGA(
			.resetn(resetn),
			.clock(CLOCK_50),
			.colour(colour_out),
			.x(x_out),
			.y(y_out),
			.plot(writeEn),
			/* Signals for the DAC to drive the monitor. */
			.VGA_R(VGA_R),
			.VGA_G(VGA_G),
			.VGA_B(VGA_B),
			.VGA_HS(VGA_HS),
			.VGA_VS(VGA_VS),
			.VGA_BLANK(VGA_BLANK_N),
			.VGA_SYNC(VGA_SYNC_N),
			.VGA_CLK(VGA_CLK));
		defparam VGA.RESOLUTION = "160x120";
		defparam VGA.MONOCHROME = "FALSE";
		defparam VGA.BITS_PER_COLOUR_CHANNEL = 1;
		defparam VGA.BACKGROUND_IMAGE = "black.mif";

	// Put your code here. Your code should produce signals x,y,colour and writeEn/plot
	// for the VGA controller, in addition to any other functionality your design may require.

    // Instansiate datapath
	datapath d0(
				.clk(CLOCK_50),
				.resetn(resetn),
				.colour_in(colour),
				.x(x),
				.y(y),
				.cases(cases),
				.lengthx(lengthx),
				.lengthy(lengthy),
				.x_out(x_out),
				.y_out(y_out),
				.colour_out(colour_out),
				.doneplot(doneplot),
				.x_load(x_load),
				.y_load(y_load),
				.done_plot(done_plot),
				.count_x_enable(count_x_enable),
				.colour_load(colour_load),
				.done_countdown(done),
				.timesup(timesup)
				);




	wire reset_counter;
	wire reset_load;
	wire colour_erase_enable;
	wire count_x_enable;
	wire ld_x;
	wire ld_y;
	wire enable_erase;
	wire done_plot;
	wire [2:0] colour_load;
	wire enable_frame;
	wire enable_counter;

	wire [6:0] x_load;
	wire [6:0] y_load;
	wire success;
	wire restart;

	states s0(.doneplot(doneplot),
				 .clk(CLOCK_50),
				 .resetn(resetn),
				 .x(x),
				 .y(y),
				 .lengthx(lengthx),
				 .lengthy(lengthy),
				 .colour(colour),
				 .cases(cases),
				 .en(en),
				 .writeEn(writeEn),
				 .go(1'b1),
				 .reset_counter(reset_counter),
				 .reset_load(reset_load),
				 .enable_counter(enable_counter),
				 .colour_erase_enable(colour_erase_enable),
				 .count_x_enable(count_x_enable), //input of data path, waiting to be used
				 .ld_x(ld_x),
				 .ld_y(ld_y),
				 .enable_erase(enable_erase),
				 .done_plot(done_plot), // input from datapath
				 .success(success),
				 .restart(restart),
				 .doneflash(1'b1),
				 .reset_countdown(reset_countdown),
				 .start_game(SW[9])
				 );







	wire timesup;

	load l0(
		.right(~KEY[0]),
		.left(~KEY[1]),
		.up(~KEY[3]),
		.down(~KEY[2]),
		.clk(CLOCK_50),
		.reset(reset_load),
		.colour_in(3'b101),
		.colour_erase_enable(colour_erase_enable),
		.ld_x(ld_x),
		.ld_y(ld_y),
		.x(x_load), // output
		.y(y_load), // output
		.success(success),
		.colour(colour_load), // output
		.restart(restart),
		.s1(LEDR[0]),
		.s2(LEDR[1]),
		.s3(LEDR[2]),
		.s4(LEDR[3]),
		.s5(LEDR[4]),
		.s6(LEDR[5]),
		.s7(LEDR[6]),
		.s8(LEDR[7]),
		.s9(LEDR[8]),
		.s10(LEDR[9]),
		.timesup(timesup),
		.score_out_low(HEX2),
		.score_out_high(HEX3)
	);

	delay_counter dc(
			.enable(enable_counter),
			.clk(CLOCK_50),
			.resetn(reset_counter),
			.enable_frame(enable_frame)
	);

	frame_counter f0(
			.enable(enable_frame),
			.clk(CLOCK_50),
			.resetn(reset_counter),
			.enable_out(enable_erase)
	);

wire done, reset_countdown;


counter2 c0(.clk(CLOCK_50), .lower(HEX0), .higher(HEX1), .done(done), .reset_countdown(reset_countdown));



		

endmodule

module states(doneplot, x, y, lengthx, lengthy, colour, clk, resetn, cases, en, writeEn,
go, reset_counter, reset_load, enable_counter,
colour_erase_enable, count_x_enable, ld_x, ld_y, enable_erase, done_plot, success, restart, doneflash, reset_countdown, start_game);




	 input doneplot;
	 input resetn;
	 input clk;
	 input en;
	 input go;
	 input doneflash;
	 input start_game;


	 output reg reset_counter;
	 output reg reset_load;
	 output reg enable_counter;
	 output reg colour_erase_enable;
	 output reg count_x_enable;
	 output reg writeEn;
	 output reg ld_x;
	 output reg ld_y;
	 output reg restart;


	 output reg [6:0] x;
	 output reg [6:0] y;
	 output reg [6:0] lengthx;
	 output reg [6:0] lengthy;
	 output reg [2:0] colour;
	 output reg [5:0] cases;
    reg [7:0] current_state, next_state;

	 input enable_erase;
	 input done_plot;
	 input success;
	 output reg reset_countdown;






    localparam
				upperbound = 6'd0,
				lowerbound = 6'd1,
				leftbound = 6'd2,
				rightbound = 6'd3,
				rect1 = 6'd4,
				rect2 = 6'd5,
				rect3 = 6'd6,
				rect4 = 6'd7,
				rect5 = 6'd8,
				rect6 = 6'd9,
				rect7 = 6'd10,
				rect8 = 6'd11,
				rect9 = 6'd12,
				food1 = 6'd13,
				food2 = 6'd14,
				food3 = 6'd15,
				food4 = 6'd16,
				food5 = 6'd17,
				food6 = 6'd18,
				food7 = 6'd19,
				food8 = 6'd20,
				food9 = 6'd21,
				food10 = 6'd22,
				core = 6'd23,
				black = 6'd24,
				RESET = 6'd25,
				RESET_WAIT = 6'd26,
				PLOT = 6'd27,
				RESET_COUNTER = 6'd28,
				COUNT = 6'd29,
				ERASE = 6'd30,
				UPDATE = 6'd31,
				ENDGAME = 6'd32;


    // Next state logic aka our state table
    always@(*)
    begin: state_table
            case (current_state)
					 black: next_state = en ? upperbound : black;
                upperbound: next_state = doneplot ? lowerbound : upperbound; // Loop in current state until value is input
                lowerbound: next_state = doneplot ? leftbound : lowerbound; // Loop in current state until go signal goes low
                leftbound: next_state = doneplot ? rightbound : leftbound;
					 rightbound : next_state = doneplot ? rect1 : rightbound;
					 rect1: next_state = doneplot ? rect2 : rect1;
					 rect2: next_state = doneplot ? rect3 : rect2;
					 rect3: next_state = doneplot ? rect4 : rect3;
					 rect4: next_state = doneplot ? rect5 : rect4;
					 rect5: next_state = doneplot ? rect6 : rect5;
					 rect6: next_state = doneplot ? rect7 : rect6;
					 rect7: next_state = doneplot ? rect8 : rect7;
					 rect8: next_state = doneplot ? rect9 : rect8;
					 rect9: next_state = doneplot ? food1 : rect9;
					 food1: next_state = doneplot ? food2 : food1;
					 food2: next_state = doneplot ? food3 : food2;
					 food3: next_state = doneplot ? food4 : food3;
					 food4: next_state = doneplot ? food5 : food4;
					 food5: next_state = doneplot ? food6 : food5;
					 food6: next_state = doneplot ? food7 : food6;
					 food7: next_state = doneplot ? food8 : food7;
					 food8: next_state = doneplot ? food9 : food8;
					 food9: next_state = doneplot ? food10 : food9;
					 food10: next_state = doneplot ? core : food10;
					 core: next_state = doneplot ? RESET : core;

                RESET: next_state = go ? RESET_WAIT : RESET; // Loop in current state until value is input
                RESET_WAIT: next_state = start_game ? PLOT : RESET_WAIT; // Loop in current state until go signal goes low
                PLOT: next_state = done_plot ? RESET_COUNTER : PLOT;
					 RESET_COUNTER : next_state = COUNT;
					 COUNT: next_state = enable_erase ? ERASE : COUNT;
                ERASE: next_state = done_plot ? UPDATE : ERASE;
					 UPDATE: next_state = success ? ENDGAME : PLOT;
					 ENDGAME: next_state = doneflash ? food1 : ENDGAME;
            default: next_state = black;
        endcase
    end // state_table


    // Output logic aka all of our datapath control signals
    always @(*)
    begin: output_signals


	   ld_x = 1'b0;
      ld_y = 1'b0;
		writeEn = 1'b0;
		reset_counter = 1'b1;
		reset_load = 1'b1;
		enable_counter = 1'b0;
		colour_erase_enable = 1'b0;
		count_x_enable = 1'b0;
		restart = 1'b0;
		reset_countdown = 1'b1;


      case (current_state)
		black: begin
			x = 0;
			y = 0;
			lengthx = 0;
			lengthy = 0;
			colour = 3'b000;
			cases = 6'b011000;
		end

         upperbound: begin
				writeEn = 1'b1;
				x = 7'b0000000;
				y = 7'b0000000;
				lengthx = 7'b1111111;
				lengthy = 7'b0000011;
				colour = 3'b111;
				cases = 6'b000000;
			end

			lowerbound: begin
				restart = 1'b1;
				writeEn = 1'b1;
				x = 7'b0000000;
				y = 7'b1110100;
				lengthx = 7'b1111111;
				lengthy = 7'b0000011;
				colour = 3'b111;
				cases = 6'b000001;
			end

			leftbound: begin
				x = 7'b0000000;
				writeEn = 1'b1;
				y = 7'b0000000;
				lengthx = 7'b0000011;
				lengthy = 7'b1110100;
				colour = 3'b111;
				cases = 6'b000010;
			end

			rightbound: begin
				x = 7'b1111100;
				writeEn = 1'b1;
				y = 7'b0000000;
				lengthx = 7'b0000011;
				lengthy = 7'b1110100;
				colour = 3'b111;
				cases = 6'b000011;
			end


			rect1: begin
				x = 7'b0001111;
				writeEn = 1'b1;
				y = 7'b0001111;
				lengthx = 7'b0100000;
				lengthy = 3'b011;
				colour = 3'b111;
				cases = 6'b000100;
			end

			rect2: begin
				x = 7'b0001111;
				writeEn = 1'b1;
				y = 7'b0001111;
				lengthx = 3'b011;
				lengthy = 7'b0100000;
				colour = 3'b111;
				cases = 6'b000101;
			end

			rect3: begin
				x = 7'b0001111;
				y = 7'b1000101;
				writeEn = 1'b1;
				lengthx = 3'b011;
				lengthy = 7'b0100000;
				colour = 3'b111;
				cases = 6'b000110;
			end

			rect4: begin
				x = 7'b0001111;
				writeEn = 1'b1;
				y = 7'b1100101;
				lengthx = 7'b0100000;
				lengthy = 3'b011;
				colour = 3'b111;
				cases = 6'b000111;
			end

			rect5: begin
				x = 7'b1010000;
				writeEn = 1'b1;
				y = 7'b0001111;
				lengthx = 7'b0100000;
				lengthy = 3'b011;
				colour = 3'b111;
				cases = 6'b001000;
			end

			rect6: begin
				x = 7'b1101110;
				writeEn = 1'b1;
				y = 7'b0001111;
				lengthx = 3'b011;
				lengthy = 7'b0100000;
				colour = 3'b111;
				cases = 6'b001001;
			end

			rect7: begin
				x = 7'b1010000;
				writeEn = 1'b1;
				y = 7'b1100101;
				lengthx = 7'b0100000;
				lengthy = 3'b011;
				colour = 3'b111;
				cases = 6'b001010;
			end


			rect8: begin
				x = 7'b1101110;
				writeEn = 1'b1;
				y = 7'b1001000;
				lengthx = 3'b011;
				lengthy = 7'b0100000;
				colour = 3'b111;
				cases = 6'b001011;
			end

         rect9: begin
				x = 7'b0101011;
				writeEn = 1'b1;
				y = 7'b0101011;
				lengthx = 7'b0101001;
				lengthy = 7'b0101001;
				colour = 3'b111;
				cases = 6'b001100;
			end


         food1: begin
				x = 7'b0101011;
				writeEn = 1'b1;
				y = 7'b0100010;
				lengthx = 1'b0;
				lengthy = 1'b0;
				colour = 3'b100;
				cases = 6'b001101;
			end

         food2: begin
				x = 7'b0001001;
				writeEn = 1'b1;
				y = 7'b1001101;
				lengthx = 1'b0;
				lengthy = 1'b0;
				colour = 3'b010;
				cases = 6'b001110;
			end

         food3: begin
				x = 7'b1110011;
				writeEn = 1'b1;
				y = 7'b1100101;
				lengthx = 1'b0;
				lengthy = 1'b0;
				colour = 3'b101;
				cases = 6'b001111;
			end

         food4: begin
				x = 7'b1101000;
				writeEn = 1'b1;
				y = 7'b0001010;
				lengthx = 1'b0;
				lengthy = 1'b0;
				colour = 3'b001;
				cases = 6'b010000;
			end

         food5: begin
				x = 7'b1110011;
				writeEn = 1'b1;
				y = 7'b0001111;
				lengthx = 1'b0;
				lengthy = 1'b0;
				colour = 3'b011;
				cases = 6'b010001;
			end

			food6: begin
				   x = 7'b0011001;
					writeEn = 1'b1;
				   y = 7'b1100000;
				   lengthx = 1'b0;
				   lengthy = 1'b0;
				   colour = 3'b100;
				   cases = 6'b010010;
			   end

			food7: begin
				   x = 7'b0001101;
					writeEn = 1'b1;
				   y = 7'b0001101;
				   lengthx = 1'b0;
				   lengthy = 1'b0;
				   colour = 3'b010;
				   cases = 6'b010011;
			   end

			food8: begin
				   x = 7'b1100111;
					writeEn = 1'b1;
				   y = 7'b0011010;
				   lengthx = 1'b0;
				   lengthy = 1'b0;
				   colour = 3'b101;
				   cases = 6'b010100;
			   end

			food9: begin
				   x = 7'b1001000;
					writeEn = 1'b1;
				   y = 7'b0001111;
				   lengthx = 1'b0;
				   lengthy = 1'b0;
				   colour = 3'b001;
				   cases = 6'b010101;
			   end

			food10: begin
				   x = 7'b0111110;
					writeEn = 1'b1;
				   y = 7'b1100101;
				   lengthx = 1'b0;
				   lengthy = 1'b0;
				   colour = 3'b011;
				   cases = 6'b010110;
			   end

         core: begin
				x = 7'b1000011;
				writeEn = 1'b1;
				y = 7'b1100101;
				lengthx = 2'b11;
				lengthy = 2'b11;
				colour = 3'b110;
				cases = 6'b010111;
			end

			RESET: begin
				reset_counter = 1'b0;
				reset_load = 1'b0;
				cases = 6'b011001;
			end

			RESET_WAIT: begin
			cases = 6'b011010;
			end

			PLOT: begin
				count_x_enable = 1'b1;
				writeEn = 1'b1;
				cases = 6'b011011;
				reset_countdown = 1'b0;
			end

			RESET_COUNTER: begin
				reset_counter = 1'b0;
				cases = 6'b011100;
				reset_countdown = 1'b0;
			end

			COUNT: begin
				enable_counter = 1'b1;
				cases = 6'b011101;
				reset_countdown = 1'b0;
			end

			ERASE: begin
				colour_erase_enable = 1'b1;
				count_x_enable = 1'b1;
				writeEn = 1'b1;
				cases = 6'b011110;
				reset_countdown = 1'b0;
			end

			UPDATE: begin
				ld_x = 1'b1;
				ld_y = 1'b1;
				cases = 6'b011111;
				reset_countdown = 1'b0;
			end

			ENDGAME: begin
				restart = success ? 1'b1 : 1'b0;
			end


        endcase
    end



    // current_state registers
    always@(posedge clk)
    begin: fsm
        if(!resetn)
            current_state <= black;
        else
            current_state <= next_state;
    end // state_FFS

endmodule

module datapath(
    input clk,
    input resetn,
    input [2:0] colour_in,
    input [6:0] x,
	 input [6:0] y,
	 input [6:0] lengthx,
	 input [6:0] lengthy,
	 input [5:0] cases,
	 input [2:0] colour_load,
    output reg [6:0] x_out,
	 output reg [6:0] y_out,
    output reg [2:0] colour_out,
	 output reg doneplot,
	 input [6:0] x_load,
	 input [6:0] y_load,
	 output reg done_plot,
	 input count_x_enable,
	 input done_countdown,
	 output reg timesup
    );

    // input registers
    reg [6:0] count_x1;
	 reg [6:0] count_y1;
	 reg [6:0] count_x2;
	 reg [6:0] count_y2;
	 reg [6:0] count_x3;
	 reg [6:0] count_y3;
	 reg [6:0] count_x4;
	 reg [6:0] count_y4;
	 reg [6:0] count_x5;
	 reg [2:0] count_y5;
	 reg [2:0] count_x6;
	 reg [6:0] count_y6;
	 reg [2:0] count_x7;
	 reg [6:0] count_y7;
	 reg [6:0] count_x8;
	 reg [2:0] count_y8;
	 reg [6:0] count_x9;
	 reg [2:0] count_y9;
	 reg [2:0] count_x10;
	 reg [6:0] count_y10;
	 reg [6:0] count_x11;
	 reg [2:0] count_y11;
	 reg [2:0] count_x12;
	 reg [6:0] count_y12;
	 reg [6:0] count_x13;
	 reg [6:0] count_y13;
	 reg [0:0] foodx1;
	 reg [0:0] foody1;
	 reg [0:0] foodx2;
	 reg [0:0] foody2;
	 reg [0:0] foodx3;
	 reg [0:0] foody3;
	 reg [0:0] foodx4;
	 reg [0:0] foody4;
	 reg [0:0] foodx5;
	 reg [0:0] foody5;
	 reg [0:0] foodx6;
	 reg [0:0] foody6;
	 reg [0:0] foodx7;
	 reg [0:0] foody7;
	 reg [0:0] foodx8;
	 reg [0:0] foody8;
	 reg [0:0] foodx9;
	 reg [0:0] foody9;
	 reg [0:0] foodx10;
	 reg [0:0] foody10;
	 reg [1:0] corex;
	 reg [1:0] corey;

	 wire enable_y1, enable_y2, enable_y3, enable_y4, enable_y5, enable_y6, enable_y7, enable_y8, enable_y9, enable_y10, enable_y11, enable_y12, enable_y13, enable_fy1;
	 wire enable_fy2, enable_fy3, enable_fy4, enable_fy5, enable_fy6, enable_fy7, enable_fy8, enable_fy9, enable_fy10, enable_corey;
	 reg doneplot1, doneplot2, doneplot3, doneplot4, doneplot5, doneplot6, doneplot7, doneplot8, doneplot9, doneplot10, doneplot11, doneplot12, doneplot13, doneplotf1;
	 reg doneplotf2, doneplotf3, doneplotf4, doneplotf5, doneplotf6, doneplotf7, doneplotf8, doneplotf9, doneplotf10, doneplotcore;



	always @(*)	begin
	    if (count_x1 == lengthx && count_y1 == lengthy) begin
			 doneplot1 <= 1'b1;
			 end
	    else
		    doneplot1 <= 1'b0;
	    end


	// counter for x1
	always @(posedge clk) begin
		if (!(cases == 6'b000000) | !resetn)
			count_x1 <= 7'b0000000;
			else if(!doneplot1)
				count_x1 <= count_x1 + 1'b1;
	end

	assign enable_y1 = (count_x1 == lengthx) ? 1 : 0;

	// counter for y1
	always @(posedge clk) begin
		if (!resetn)
			count_y1 <= 7'b0000000;
		else if ( enable_y1 && !doneplot1)
			count_y1 <= count_y1 + 1'b1;
	end





	always @(*)	begin
	    if (count_x2 == lengthx && count_y2 == lengthy) begin
			 doneplot2 <= 1'b1;
			 end
	    else
		    doneplot2 <= 1'b0;
	    end


	// counter for x2
	always @(posedge clk) begin
		if (!(cases == 6'b000001) | !resetn)
			count_x2 <= 7'b0000000;
			else
				count_x2 <= count_x2 + 1'b1;

	end

	assign enable_y2 = (count_x2 == lengthx) ? 1 : 0;

	// counter for y2
	always @(posedge clk) begin
		if (!resetn)
			count_y2 <= 7'b0000000;
		else if (enable_y2 && !doneplot2)
			count_y2 <= count_y2 + 1'b1;
	end




	always @(*)	begin
	    if (count_x3 == lengthx && count_y3 == lengthy) begin
			 doneplot3 <= 1'b1;
			 end
	    else
		    doneplot3 <= 1'b0;
	    end


	// counter for x3
	always @(posedge clk) begin
		if (!(cases == 6'b000010) | !resetn)
			count_x3 <= 7'b0000000;
			else begin
				if(count_x3 == 7'b0000011) begin
					count_x3 <= 7'b0000000;
					end
					else
						count_x3 <= count_x3 + 1'b1;
				end
	end

	assign enable_y3 = (count_x3 == lengthx) ? 1 : 0;

	// counter for y3
	always @(posedge clk) begin
		if (!resetn)
			count_y3 <= 7'b0000000;
		else  if (enable_y3 && !doneplot3)
			count_y3 <= count_y3 + 1'b1;
	end




	always @(*)	begin
	    if (count_x4 == lengthx && count_y4 == lengthy) begin
			 doneplot4 <= 1'b1;
			 end
	    else
		    doneplot4 <= 1'b0;
	    end


	// counter for x4
	always @(posedge clk) begin
		if (!(cases == 6'b000011) | !resetn)
			count_x4 <= 7'b0000000;
			else begin
				if(count_x4 == 7'b0000011) begin
					count_x4 <= 7'b0000000;
					end
					else
						count_x4 <= count_x4 + 1'b1;
				end
	end

	assign enable_y4 = (count_x4 == lengthx) ? 1 : 0;

	// counter for y4
	always @(posedge clk) begin
		if (!resetn)
			count_y4 <= 7'b0000000;
		else if (enable_y4 && !doneplot4)
			count_y4 <= count_y4 + 1'b1;
	end




	always @(*)	begin
	    if (count_x5 == lengthx && lengthy == {5'b00000, count_y5}) begin
			 doneplot5 <= 1'b1;
			 end
	    else
		    doneplot5 <= 1'b0;
	    end


	// counter for x5
	always @(posedge clk) begin
		if (!(cases == 6'b000100) | !resetn)
			count_x5 <= 7'b0000000;
			else begin
				if(count_x5 == 7'b0100000) begin
					count_x5 <= 7'b0000000;
					end
					else
						count_x5 <= count_x5 + 1'b1;
				end
		end

	assign enable_y5 = (count_x5 == 7'b0100000) ? 1 : 0;

	// counter for y5
	always @(posedge clk) begin
		if (!resetn)
			count_y5 <= 3'b000;
		else if (enable_y5 && !doneplot5)
			count_y5 <= count_y5 + 1'b1;
	end






	always @(*)	begin
	    if ({5'b00000, count_x6} == lengthx && lengthy == count_y6) begin
			 doneplot6 <= 1'b1;
			 end
	    else
		    doneplot6 <= 1'b0;
	    end


	// counter for x6
	always @(posedge clk) begin
		if (!(cases == 6'b000101) | !resetn)
			count_x6 <= 3'b000;
			else begin
				if(count_x6 == 3'b011) begin
					count_x6 <= 3'b000;
					end
					else
						count_x6 <= count_x6 + 1'b1;
				end
		end

	assign enable_y6 = (count_x6 == 3'b011) ? 1 : 0;

	// counter for y6
	always @(posedge clk) begin
		if (!resetn)
			count_y6 <= 3'b000;
		else if (enable_y6 && !doneplot6)
			count_y6 <= count_y6 + 1'b1;
	end







	always @(*)	begin
	    if ({5'b00000, count_x7} == lengthx && lengthy == count_y7) begin
			 doneplot7 <= 1'b1;
			 end
	    else
		    doneplot7 <= 1'b0;
	    end


	// counter for x7
	always @(posedge clk) begin
		if (!(cases == 6'b000110) | !resetn)
			count_x7 <= 3'b000;
			else begin
				if(count_x7 == 3'b011) begin
					count_x7 <= 3'b000;
					end
					else
						count_x7 <= count_x7 + 1'b1;
				end
		end

	assign enable_y7 = (count_x7 == 3'b011) ? 1 : 0;

	// counter for y7
	always @(posedge clk) begin
		if (!resetn)
			count_y7 <= 3'b000;
		else if (enable_y7 && !doneplot7)
			count_y7 <= count_y7 + 1'b1;
	end








	always @(*)	begin
	    if (count_x8 == lengthx && lengthy == {5'b00000, count_y8}) begin
			 doneplot8 <= 1'b1;
			 end
	    else
		    doneplot8 <= 1'b0;
	    end
	// counter for x8
	always @(posedge clk) begin
		if (!(cases == 6'b000111) | !resetn)
			count_x8 <= 7'b0000000;
			else begin
				if(count_x8 == 7'b0100000) begin
					count_x8 <= 7'b0000000;
					end
					else
						count_x8 <= count_x8 + 1'b1;
				end
		end

	assign enable_y8 = (count_x8 == 7'b0100000) ? 1 : 0;

	// counter for y8
	always @(posedge clk) begin
		if (!resetn)
			count_y8 <= 3'b000;
		else if (enable_y8 && !doneplot8)
			count_y8 <= count_y8 + 1'b1;
	end







	always @(*)	begin
	    if (count_x9 == lengthx && lengthy == {5'b00000, count_y9}) begin
			 doneplot9 <= 1'b1;
			 end
	    else
		    doneplot9 <= 1'b0;
	    end
	// counter for x9
	always @(posedge clk) begin
		if (!(cases == 6'b001000) | !resetn)
			count_x9 <= 7'b0000000;
			else begin
				if(count_x9 == 7'b0100000) begin
					count_x9 <= 7'b0000000;
					end
					else
						count_x9 <= count_x9 + 1'b1;
				end
		end

	assign enable_y9 = (count_x9 == 7'b0100000) ? 1 : 0;

	// counter for y9
	always @(posedge clk) begin
		if (!resetn)
			count_y9 <= 3'b000;
		else if (enable_y9 && !doneplot9)
			count_y9 <= count_y9 + 1'b1;
	end







	always @(*)	begin
	    if ({5'b00000, count_x10} == lengthx && lengthy == count_y10) begin
			 doneplot10 <= 1'b1;
			 end
	    else
		    doneplot10 <= 1'b0;
	    end


	// counter for x10
	always @(posedge clk) begin
		if (!(cases == 6'b001001) | !resetn)
			count_x10 <= 3'b000;
			else begin
				if(count_x10 == 3'b011) begin
					count_x10 <= 3'b000;
					end
					else
						count_x10 <= count_x10 + 1'b1;
				end
		end

	assign enable_y10 = (count_x10 == 3'b011) ? 1 : 0;

	// counter for y10
	always @(posedge clk) begin
		if (!resetn)
			count_y10 <= 7'b0000000;
		else if (enable_y10 && !doneplot10)
			count_y10 <= count_y10 + 1'b1;
	end










	always @(*)	begin
	    if (count_x11 == lengthx && lengthy == {5'b00000, count_y11}) begin
			 doneplot11 <= 1'b1;
			 end
	    else
		    doneplot11 <= 1'b0;
	    end
	// counter for x11
	always @(posedge clk) begin
		if (!(cases == 6'b001010) | !resetn)
			count_x11 <= 7'b0000000;
			else begin
				if(count_x11 == 7'b0100000) begin
					count_x11 <= 7'b0000000;
					end
					else
						count_x11 <= count_x11 + 1'b1;
				end
		end

	assign enable_y11 = (count_x11 == 7'b0100000) ? 1 : 0;

	// counter for y11
	always @(posedge clk) begin
		if (!resetn)
			count_y11 <= 3'b000;
		else if (enable_y11 && !doneplot11)
			count_y11 <= count_y11 + 1'b1;
	end







	always @(*)	begin
	    if ({5'b00000, count_x12} == lengthx && lengthy == count_y12) begin
			 doneplot12 <= 1'b1;
			 end
	    else
		    doneplot12 <= 1'b0;
	    end


	// counter for x12
	always @(posedge clk) begin
		if (!(cases == 6'b001011) | !resetn)
			count_x12 <= 3'b000;
			else begin
				if(count_x12 == 3'b011) begin
					count_x12 <= 3'b000;
					end
					else
						count_x12 <= count_x12 + 1'b1;
				end
		end

	assign enable_y12 = (count_x12 == 3'b011) ? 1 : 0;

	// counter for y12
	always @(posedge clk) begin
		if (!resetn)
			count_y12 <= 7'b0000000;
		else if (enable_y12 && !doneplot12)
			count_y12 <= count_y12 + 1'b1;
	end







	always @(*)	begin
	    if (count_x13 == lengthx && lengthy == count_y13) begin
			 doneplot13 <= 1'b1;
			 end
	    else
		    doneplot13 <= 1'b0;
	    end


	// counter for x13
	always @(posedge clk) begin
		if (!(cases == 6'b001100) | !resetn)
			count_x13 <= 7'b0000000;
			else begin
				if(count_x13 == 7'b0101001) begin
					count_x13 <= 7'b0000000;
					end
					else
						count_x13 <= count_x13 + 1'b1;
				end
		end

	assign enable_y13 = (count_x13 == 7'b0101001) ? 1 : 0;

	// counter for y13
	always @(posedge clk) begin
		if (!resetn)
			count_y13 <= 7'b0000000;
		else if (enable_y13 && !doneplot13)
			count_y13 <= count_y13 + 1'b1;
	end






	always @(*)	begin
	    if (foodx1 == lengthx && foody1 == lengthy) begin
			 doneplotf1 <= 1'b1;
			 end
	    else
		    doneplotf1 <= 1'b0;
	    end


	// counter for xf1
	always @(posedge clk) begin
		if (!(cases == 6'b001101)|!resetn)
			foodx1 <= 1'b0;
			else begin
				if(foodx1 == lengthx) begin
					foodx1 <= 1'b0;
					end
					else
						foodx1 <= foodx1 + 1'b1;
				end
		end

	assign enable_fy1 = (foodx1 == lengthx) ? 1 : 0;

	// counter for yf1
	always @(posedge clk) begin
		if (!resetn)
			foody1 <= 1'b0;
		else if (enable_fy1 && !doneplotf1)
			foody1 <= foody1 + 1'b1;
	end





	always @(*)	begin
	    if (foodx2 == lengthx && foody2 == lengthy) begin
			 doneplotf2 <= 1'b1;
			 end
	    else
		    doneplotf2 <= 1'b0;
	    end


	// counter for xf2
	always @(posedge clk) begin
		if (!(cases == 6'b001110)|!resetn)
			foodx2 <= 1'b0;
			else begin
				if(foodx2 == lengthx) begin
					foodx2 <= 1'b0;
					end
					else
						foodx2 <= foodx2 + 1'b1;
				end
		end

	assign enable_fy2 = (foodx2 == lengthx) ? 1 : 0;

	// counter for yf2
	always @(posedge clk) begin
		if (!resetn)
			foody2 <= 1'b0;
		else if (enable_fy2 && !doneplotf2)
			foody2 <= foody2 + 1'b1;
	end









	always @(*)	begin
	    if (foodx3 == lengthx && foody3 == lengthy) begin
			 doneplotf3 <= 1'b1;
			 end
	    else
		    doneplotf3 <= 1'b0;
	    end


	// counter for xf3
	always @(posedge clk) begin
		if (!(cases == 6'b001111)|!resetn)
			foodx3 <= 1'b0;
			else begin
				if(foodx3 == lengthx) begin
					foodx3 <= 1'b0;
					end
					else
						foodx3 <= foodx3 + 1'b1;
				end
		end

	assign enable_fy3 = (foodx3 == lengthx) ? 1 : 0;

	// counter for yf3
	always @(posedge clk) begin
		if (!resetn)
			foody3 <= 1'b0;
		else if (enable_fy3 && !doneplotf3)
			foody3 <= foody3 + 1'b1;
	end






	always @(*)	begin
	    if (foodx4 == lengthx && foody4 == lengthy) begin
			 doneplotf4 <= 1'b1;
			 end
	    else
		    doneplotf4 <= 1'b0;
	    end


	// counter for xf4
	always @(posedge clk) begin
		if (!(cases == 6'b010000)|!resetn)
			foodx4 <= 1'b0;
			else begin
				if(foodx4 == lengthx) begin
					foodx4 <= 1'b0;
					end
					else
						foodx4 <= foodx4 + 1'b1;
				end
		end

	assign enable_fy4 = (foodx4 == lengthx) ? 1 : 0;

	// counter for yf4
	always @(posedge clk) begin
		if (!resetn)
			foody4 <= 1'b0;
		else if (enable_fy4 && !doneplotf4)
			foody4 <= foody4 + 1'b1;
	end






	always @(*)	begin
	    if (foodx5 == lengthx && foody5 == lengthy) begin
			 doneplotf5 <= 1'b1;
			 end
	    else
		    doneplotf5 <= 1'b0;
	    end


	// counter for xf5
	always @(posedge clk) begin
		if (!(cases == 6'b010001)|!resetn)
			foodx5 <= 1'b0;
			else begin
				if(foodx5 == lengthx) begin
					foodx5 <= 1'b0;
					end
					else
						foodx5 <= foodx5 + 1'b1;
				end
		end

	assign enable_fy5 = (foodx5 == lengthx) ? 1 : 0;

	// counter for yf5
	always @(posedge clk) begin
		if (!resetn)
			foody5 <= 1'b0;
		else if (enable_fy5 && !doneplotf5)
			foody5 <= foody5 + 1'b1;
	end







		always @(*)	begin
		    if (foodx6 == lengthx && foody6 == lengthy) begin
				 doneplotf6 <= 1'b1;
				 end
		    else
			    doneplotf6 <= 1'b0;
		    end


		// counter for xf6
		always @(posedge clk) begin
			if (!(cases == 6'b010010)|!resetn)
				foodx6 <= 1'b0;
				else begin
					if(foodx6 == lengthx) begin
						foodx6 <= 1'b0;
						end
						else
							foodx6 <= foodx6 + 1'b1;
					end
			end

		assign enable_fy6 = (foodx6 == lengthx) ? 1 : 0;

		// counter for yf6
		always @(posedge clk) begin
			if (!resetn)
				foody6 <= 1'b0;
			else if (enable_fy6 && !doneplotf6)
				foody6 <= foody6 + 1'b1;
		end







			always @(*)	begin
			    if (foodx7 == lengthx && foody7 == lengthy) begin
					 doneplotf7 <= 1'b1;
					 end
			    else
				    doneplotf7 <= 1'b0;
			    end


			// counter for xf7
			always @(posedge clk) begin
				if (!(cases == 6'b010011)|!resetn)
					foodx7 <= 1'b0;
					else begin
						if(foodx7 == lengthx) begin
							foodx7 <= 1'b0;
							end
							else
								foodx7 <= foodx7 + 1'b1;
						end
				end

			assign enable_fy7 = (foodx7 == lengthx) ? 1 : 0;

			// counter for yf7
			always @(posedge clk) begin
				if (!resetn)
					foody7 <= 1'b0;
				else if (enable_fy7 && !doneplotf7)
					foody7 <= foody7 + 1'b1;
			end








				always @(*)	begin
				    if (foodx8 == lengthx && foody8 == lengthy) begin
						 doneplotf8<= 1'b1;
						 end
				    else
					    doneplotf8 <= 1'b0;
				    end


				// counter for xf8
				always @(posedge clk) begin
					if (!(cases == 6'b010100)|!resetn)
						foodx8 <= 1'b0;
						else begin
							if(foodx8 == lengthx) begin
								foodx8 <= 1'b0;
								end
								else
									foodx8 <= foodx8 + 1'b1;
							end
					end

				assign enable_fy8 = (foodx8 == lengthx) ? 1 : 0;

				// counter for yf8
				always @(posedge clk) begin
					if (!resetn)
						foody8 <= 1'b0;
					else if (enable_fy8 && !doneplotf8)
						foody8 <= foody8 + 1'b1;
				end







					always @(*)	begin
					    if (foodx9 == lengthx && foody9 == lengthy) begin
							 doneplotf9 <= 1'b1;
							 end
					    else
						    doneplotf9 <= 1'b0;
					    end


					// counter for xf9
					always @(posedge clk) begin
						if (!(cases == 6'b010101)|!resetn)
							foodx9 <= 1'b0;
							else begin
								if(foodx9 == lengthx) begin
									foodx9 <= 1'b0;
									end
									else
										foodx9 <= foodx9 + 1'b1;
								end
						end

					assign enable_fy9 = (foodx9 == lengthx) ? 1 : 0;

					// counter for yf9
					always @(posedge clk) begin
						if (!resetn)
							foody9 <= 1'b0;
						else if (enable_fy9 && !doneplotf9)
							foody9 <= foody9 + 1'b1;
					end







						always @(*)	begin
						    if (foodx10 == lengthx && foody10 == lengthy) begin
								 doneplotf10 <= 1'b1;
								 end
						    else
							    doneplotf10 <= 1'b0;
						    end


						// counter for xf10
						always @(posedge clk) begin
							if (!(cases == 6'b010110)|!resetn)
								foodx10 <= 1'b0;
								else begin
									if(foodx10 == lengthx) begin
										foodx10 <= 1'b0;
										end
										else
											foodx10 <= foodx10 + 1'b1;
									end
							end

						assign enable_fy10 = (foodx10 == lengthx) ? 1 : 0;

						// counter for yf10
						always @(posedge clk) begin
							if (!resetn)
								foody10 <= 1'b0;
							else if (enable_fy10 && !doneplotf10)
								foody10 <= foody10 + 1'b1;
						end




	always @(*)	begin
	    if (corex == lengthx && corey == lengthy) begin
			 doneplotcore <= 1'b1;
			 end
	    else
		    doneplotcore <= 1'b0;
	    end


	// counter for corex
	always @(posedge clk) begin
		if (!(cases == 6'b010111)|!resetn)
			corex <= 2'b00;
			else begin
				if(corex == lengthx) begin
					corex <= 2'b00;
					end
					else
						corex <= corex + 1'b1;
				end
		end

	assign enable_corey = (corex == lengthx) ? 1 : 0;

	// counter for corey
	always @(posedge clk) begin
		if (!resetn)
			corey <= 2'b00;
		else if (enable_corey && !doneplotcore)
			corey <= corey + 1'b1;
	end







	reg [1:0] move_x, move_y;
	wire enable_move_y;



	always @(*)
	begin
	if (move_x == 2'b11 && move_y == 2'b11)
		done_plot = 1'b1;
	else
		done_plot = 1'b0;
	end

	// counter for movex
	always @(posedge clk) begin
		if (!resetn)
			move_x <= 2'b00;
		else if (count_x_enable)
			move_x <= move_x + 1'b1;
	end

	assign enable_move_y = (move_x == 2'b11) ? 1 : 0;

	// counter for movey
	always @(posedge clk) begin
		if (!resetn)
			move_y <= 2'b00;
		else if (enable_move_y)
			move_y <= move_y + 1'b1;
	end

















	always@(*) begin
		timesup = 1'b0;
		case (cases)
			6'b000000: begin
				x_out = x + count_x1;
				y_out = y + count_y1;
				doneplot = doneplot1;
				colour_out = colour_in;
				end
			6'b000001: begin
				x_out = x + count_x2;
				y_out = y + count_y2;
				doneplot = doneplot2;
				colour_out = colour_in;
				end
			6'b000010: begin
				x_out = x + count_x3;
				y_out = y + count_y3;
				doneplot = doneplot3;
				colour_out = colour_in;
				end
			6'b000011: begin
				x_out = x + count_x4;
				y_out = y + count_y4;
				doneplot = doneplot4;
				colour_out = colour_in;
				end
			6'b000100: begin
				x_out = x + count_x5;
				y_out = y + {5'b00000, count_y5};
				doneplot = doneplot5;
				colour_out = colour_in;
				end

			6'b000101: begin
				x_out = x + {5'b00000, count_x6};
				y_out = y + count_y6;
				doneplot = doneplot6;
				colour_out = colour_in;
				end

			6'b000110: begin
				x_out = x + {5'b00000, count_x7};
				y_out = y + count_y7;
				doneplot = doneplot7;
				colour_out = colour_in;
				end

			6'b000111: begin
				x_out = x + count_x8;
				y_out = y + {5'b00000, count_y8};
				doneplot = doneplot8;
				colour_out = colour_in;
				end

			6'b001000: begin
				x_out = x + count_x9;
				y_out = y + {5'b00000, count_y9};
				doneplot = doneplot9;
				colour_out = colour_in;
				end

			6'b001001: begin
				x_out = x + {5'b00000, count_x10};
				y_out = y + count_y10;
				doneplot = doneplot10;
				colour_out = colour_in;
				end

			6'b001010: begin
				x_out = x + count_x11;
				y_out = y + {5'b00000, count_y11};
				doneplot = doneplot11;
				colour_out = colour_in;
				end

			6'b001011: begin
				x_out = x + {5'b00000, count_x12};
				y_out = y + count_y12;
				doneplot = doneplot12;
				colour_out = colour_in;
				end


			6'b001100: begin
				x_out = x + count_x13;
				y_out = y + count_y13;
				doneplot = doneplot13;
				colour_out = colour_in;
				end


			6'b001101: begin
				x_out = x + foodx1;
				y_out = y + foody1;
				doneplot = doneplotf1;
				colour_out = colour_in;
				end

			6'b001110: begin
				x_out = x + foodx2;
				y_out = y + foody2;
				doneplot = doneplotf2;
				colour_out = colour_in;
				end

			6'b001111: begin
				x_out = x + foodx3;
				y_out = y + foody3;
				doneplot = doneplotf3;
				colour_out = colour_in;
				end

			6'b010000: begin
				x_out = x + foodx4;
				y_out = y + foody4;
				doneplot = doneplotf4;
				colour_out = colour_in;
				end

			6'b010001: begin
				x_out = x + foodx5;
				y_out = y + foody5;
				doneplot = doneplotf5;
				colour_out = colour_in;
				end


				6'b010010: begin
					x_out = x + foodx6;
					y_out = y + foody6;
					doneplot = doneplotf6;
					colour_out = colour_in;
					end

				6'b010011: begin
					x_out = x + foodx7;
					y_out = y + foody7;
					doneplot = doneplotf7;
					colour_out = colour_in;
					end

				6'b010100: begin
					x_out = x + foodx8;
					y_out = y + foody8;
					doneplot = doneplotf8;
					colour_out = colour_in;
					end

				6'b010101: begin
					x_out = x + foodx9;
					y_out = y + foody9;
					doneplot = doneplotf9;
					colour_out = colour_in;
					end

				6'b010110: begin
					x_out = x + foodx10;
					y_out = y + foody10;
					doneplot = doneplotf10;
					colour_out = colour_in;
					end

			6'b010111: begin
				x_out = x + corex;
				y_out = y + corey;
				doneplot = doneplotcore;
				colour_out = colour_in;
				end

			6'b011001: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;
			end

			6'b011010: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;
			end

			6'b011011: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;
			end

			6'b011100: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;
			end

			6'b011101: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;
			end

			6'b011110: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;

			end

			6'b011111: begin
			   x_out = x_load + move_x;
				y_out = y_load + move_y;
				colour_out = colour_load;
				timesup = done_countdown ? 1'b1 : 1'b0;
			end
		endcase
	end



endmodule









































module delay_counter(enable, clk, resetn, enable_frame);
	  input enable, clk, resetn;
      output enable_frame;
	  reg [22:0] counter;

	  assign enable_frame = (counter == 0) ? 1 : 0;

	  always @(posedge clk)
	  begin
	       if (!resetn)
			      counter <= 433332;
			  else if (enable == 1'b1)
			  begin
					if (counter == 22'd0)
						counter <= 433332;
					else
						counter <= counter - 1'b1;
				end
	  end
endmodule

module frame_counter(enable, clk, resetn, enable_out);
	input enable, clk, resetn;
	output enable_out;

	reg [3:0] frames;

	assign enable_out= (frames == 4'b1111) ? 1 : 0;

	always @ (posedge clk)
	begin
		if (!resetn)
			frames <= 0;
		else if (enable == 1'b1)
		begin
			if (frames == 4'b1111)
				frames <= 0;
			else
			frames <= frames + 1;
			end
	end
endmodule

module load(clk, reset, colour_in, colour_erase_enable, ld_x, ld_y, 
 x, y, colour, right, left, up, down, success, restart, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, timesup, score_out_low, score_out_high);
	input clk, reset;
	input restart;
	input [2:0] colour_in;
	input colour_erase_enable;
	input ld_x, ld_y;
	input right;
	input left;
	input up;
	input timesup;
	input down;
	output reg [6:0] x;
	output reg [6:0] y;
	output reg [2:0] colour;
	output  success;

	reg [1:0] cases;

	always @(*) begin
		if (right)
			cases <= 2'b00;
			else if (left)
				cases <= 2'b01;
				else if (down)
					cases <= 2'b10;
						else if (up)
							cases <= 2'b11;
							else
								cases <= cases;
	end


	output reg s1;
	output reg s2;
	output reg s3;
	output reg s4;
	output reg s5;
	output reg s6;
	output reg s7;
	output reg s8;
	output reg s9;
	output reg s10;
	output [6:0]score_out_low;
	output [6:0]score_out_high;
	reg [7:0]score_out;
	
	
	wire [7:0] c1,c2,c3,c4,c5,c6,c7,c8,c9,c10;
	
	assign c1 = s1 ? 8'b00000100 : 8'b00000000;
	assign c2 = s2 ? 8'b00000011 : 8'b00000000;
	assign c3 = s3 ? 8'b00000010 : 8'b00000000;
	assign c4 = s4 ? 8'b00000100 : 8'b00000000;
	assign c5 = s5 ? 8'b00000110 : 8'b00000000;
	assign c6 = s6 ? 8'b00000010 : 8'b00000000;
	assign c7 = s7 ? 8'b00000111 : 8'b00000000;
	assign c8 = s8 ? 8'b00000001 : 8'b00000000;
	assign c9 = s9 ? 8'b00000010 : 8'b00000000;
	assign c10 = s10 ? 8'b00000001 : 8'b00000000;
	
	always@(*) begin
		if (restart) begin
			score_out <= 8'b00000000;
		end
		else begin
			score_out <= (c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10);
		end
	end
	
	
	reg [3:0] higher;
	reg [3:0] lower;
	always@(*) begin
		higher = 4'b0000;
		if(score_out < 10) begin
			higher = 4'b0000;
			lower = score_out[3:0];
		end
		else if (score_out < 20) begin
			higher = 4'b0001;
			lower = score_out - 10;
		end
		else if (score_out < 30) begin
			higher = 4'b0010;
			lower = score_out - 20;
		end
		else if (score_out < 40) begin
			higher = 4'b0011;
			lower = score_out - 30;
		end
	end
	
	segments y0(lower[3:0], score_out_low[6:0]);
	segments y1({2'b00,higher[1:0]}, score_out_high[6:0]);
	
	always@(*) begin

		 if (restart) begin
			s1 <= 1'b0;
		 end

		 else if (((x == 7'b0101011|x == 7'b0101000) && y > 7'b0011110 && y < 7'b0100011)
			| ((y == 7'b0100010|y == 7'b0011111) && x > 7'b0100111 && x < 7'b0101100) ) begin
				if (!s1) begin
					s1 <= 1'b1;
				end
			end
		end


	always@(*) begin

		 if (restart) begin
			s2 <= 1'b0;
		 end

		 else if (((x == 7'b0001001|x == 7'b0000110) && (y > 7'b1001001) && (y < 7'b1001110))
			| ((y == 7'b1001101|y == 7'b1001010) && (x > 7'b0000101) && (x < 7'b0001010)) ) begin
				if (!s2) begin
					s2 <= 1'b1;
				end
			end
	   end


	always@(*) begin

		if (restart) begin
			s3 <= 1'b0;
		end

		else if (((x == 7'b1110011|x == 7'b1110000) && (y > 7'b1100001) && (y < 7'b1100110))
 			  | ((y == 7'b1100101|y == 7'b1100010) && (x > 7'b1101111) && (x < 7'b1110100)) ) begin
 				if (!s3) begin
 					s3 <= 1'b1;
 				end
 			end
		end



	always@(*) begin

		if (restart) begin
			s4 <= 1'b0;
		end

		else if (((x == 7'b1101000|x == 7'b1100101) && (y > 7'b0000110) && (y < 7'b0001011))
 			  | ((y == 7'b0001010|y == 7'b0000111) && (x > 7'b1100100) && (x < 7'b1101001)) ) begin
 				if (!s4) begin
 					s4 <= 1'b1;
 				end
 			end
		end



	always@(*) begin

		if (restart) begin
			s5 <= 1'b0;
		end

		else if (((x == 7'b1110011|x == 7'b1110000) && (y > 7'b0001011) && (y < 7'b0010000))
 			  |  ((y == 7'b0001111|y == 7'b0001100) && (x > 7'b1101111) && (x < 7'b1110100)) ) begin
 				if (!s5) begin
 					s5 <= 1'b1;
 				end
 			end
		end

		always@(*) begin

			 if (restart) begin
				s6 <= 1'b0;
			 end

			 else if (((x == 7'b0011001|x == 7'b0010110) && y > 7'b1011100 && y < 7'b1100001)
				|     ((y == 7'b1100000|y == 7'b1011101) && x > 7'b0010101 && x < 7'b0011010) ) begin
					if (!s6) begin
						s6 <= 1'b1;
					end
				end
			end


		always@(*) begin

			 if (restart) begin
				s7 <= 1'b0;
			 end

			 else if (((x == 7'b0001101|x == 7'b0001010) && (y > 7'b0001001) && (y < 7'b0001110))
				|     ((y == 7'b0001101|y == 7'b0001010) && (x > 7'b0001001) && (x < 7'b0001110)) ) begin
					if (!s7) begin
						s7 <= 1'b1;
					end
				end
		   end


		always@(*) begin

			if (restart) begin
				s8 <= 1'b0;
			end

			else if (((x == 7'b1100111|x == 7'b1100100) && (y > 7'b0010110) && (y < 7'b0011011))
				   | ((y == 7'b0011010|y == 7'b0010111) && (x > 7'b1100011) && (x < 7'b1101000)) ) begin
					if (!s8) begin
						s8 <= 1'b1;
					end
				end
			end



		always@(*) begin

			if (restart) begin
				s9 <= 1'b0;
			end

			else if (((x == 7'b1001000|x == 7'b1000101) && (y > 7'b0001011) && (y < 7'b0010000))
				   | ((y == 7'b0001111|y == 7'b0001100) && (x > 7'b1000100) && (x < 7'b1001001)) ) begin
					if (!s9) begin
						s9 <= 1'b1;
					end
				end
			end



		always@(*) begin

			if (restart) begin
				s10 <= 1'b0;
			end

			else if (((x == 7'b0111110|x == 7'b0111011) && (y > 7'b1100001) && (y < 7'b1100110))
				   | ((y == 7'b1100101|y == 7'b1100010) && (x > 7'b0111010) && (x < 7'b0111111)) ) begin
					if (!s10) begin
						s10 <= 1'b1;
					end
				end
			end




	reg endbytime;

	always@(clk) begin
		if (timesup == 1'b1)
			endbytime <= 1'b1;
		else
			endbytime <= 1'b0;
	end

	assign success = ((s1 && s2 && s3 && s4 && s5 && s6 && s7 && s8 && s9 && s10) | endbytime);
	
	


	always @ (posedge clk) begin

		case(cases)
			// move to the right
			2'b00: begin
				if (!reset|success) begin
            x <= 7'b1000011;
            y <= 7'b1100101;
				end
					else begin
						if (ld_x) begin
								if ((x == 7'b0001011 && y > 7'b0001011 && y < 7'b0110000)
									|(x == 7'b0001011 && y > 7'b1000001 && y < 7'b1101001)

									|(x == 7'b1001100 && y > 7'b0001011 && y < 7'b0010011)
									|(x == 7'b1001100 && y > 7'b1100001 && y < 7'b1101001)

									|(x == 7'b1101010 && y > 7'b0001011 && y < 7'b0110000)
									|(x == 7'b1101010 && y > 7'b1000100 && y < 7'b1101001)

									|(x == 7'b0100111 && y > 7'b0100111 && y < 7'b1010101)

									|(x == 7'b1111000 && y > 7'b0000000 && y < 7'b1111111)
									|(right == 1'b0) ) begin
									x <= x;
								end
								else begin
									x <= x + 1;
								end
							end
						else
							x <= x;
						end
					end
			2'b01: begin
				if (!reset|success) begin
            x <= 7'b1000011;
            y <= 7'b1100101;
				end
					else begin

						if (ld_x) begin
								if ((x == 7'b0010011 && y > 7'b0001111 && y < 7'b0110000)
									|(x == 7'b0010011 && y > 7'b1000001 && y < 7'b1101001)

									|(x == 7'b0110000 && y > 7'b0001011 && y < 7'b0010011)
									|(x == 7'b0110000 && y > 7'b1100001 && y < 7'b1101001)

									|(x == 7'b1110010 && y > 7'b0001011 && y < 7'b0110000)
									|(x == 7'b1110010 && y > 7'b1000100 && y < 7'b1101001)

									|(x == 7'b1010101 && y > 7'b0100111 && y < 7'b1010101)

									|(x == 7'b0000100 && y > 7'b0000000 && y < 7'b1111111)
									| left == 1'b0) begin
									x <= x;
								end
								else begin
									x <= x - 1;
								end
							end
						else
							x <= x;
						end
					end
			2'b10: begin
				if (!reset|success) begin
            x <= 7'b1000011;
            y <= 7'b1100101;
				end
					else begin
						if (ld_x) begin
								if ((y == 7'b0001011 && x > 7'b0001011 && x < 7'b0110000)
									|(y == 7'b0001011 && x > 7'b1001100 && x < 7'b1110010)

									|(y == 7'b1000001 && x > 7'b0001011 && x < 7'b0010011)
									|(y == 7'b1000100 && x > 7'b1101010 && x < 7'b1110010)

									|(y == 7'b1100001 && x > 7'b0001011 && x < 7'b0110000)
									|(y == 7'b1100001 && x > 7'b1001100 && x < 7'b1110010)

									|(y == 7'b0100111 && x > 7'b0100111 && x < 7'b1010101)

									|(y == 7'b1110000 && x > 7'b0000000 && x < 7'b1111111)
									| down == 1'b0) begin
									y <= y;
								end
								else begin
									y <= y + 1;
								end
							end
						else
							x <= x;
						end
					end
			2'b11: begin
				if (!reset |success) begin
            x <= 7'b1000011;
            y <= 7'b1100101;
				end
					else begin
						if (ld_x) begin
								if ((y == 7'b0010011 && x > 7'b0001111 && x < 7'b0110000)
									|(y == 7'b0010011 && x > 7'b1001100 && x < 7'b1110001)

									|(y == 7'b0110000 && x > 7'b0001011 && x < 7'b0010011)
									|(y == 7'b0110000 && x > 7'b1101010 && x < 7'b1110010)

									|(y == 7'b1101001 && x > 7'b0001011 && x < 7'b0110000)
									|(y == 7'b1101001 && x > 7'b1001100 && x < 7'b1110010)

									|(y == 7'b1010101 && x > 7'b0100111 && x < 7'b1010101)

									|(y == 7'b0000100 && x > 7'b0000000 && x < 7'b1111111)

									| up == 1'b0) begin
									y <= y;
								end
								else begin
									y <= y - 1;
								end
							end
						else
							x <= x;
						end
					end
			endcase
		end


	always @(*)
	begin
	if (colour_erase_enable | success)
		colour = 3'b000;
	else
		colour = colour_in;
	end
endmodule






