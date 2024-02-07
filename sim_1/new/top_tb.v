`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/24/2024 07:30:04 PM
// Design Name: 
// Module Name: top_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module top_tb(
);

reg sysclk   = 0,
    comm_clk = 0, 
    txe      = 0; //inputs

wire [7:0] data; //output data (to FT2232)
wire wr; //write ready signal (to FT2232)

top tb
(
.sysclk(sysclk),
.comm_clk(comm_clk),
.txe(txe),
.data(data),
.wr(wr)

);

integer i;
initial begin
    for (i=0; i<100000; i = i+1) begin
        if(i % 1 == 0) begin
            comm_clk <= ~comm_clk;
        end

        if(i % 5 == 0) begin
            sysclk <= ~sysclk;
        end

        if(i % ($random%25) == 0) begin
            txe <= ~txe;
        end
        #10;
    end
end

endmodule
