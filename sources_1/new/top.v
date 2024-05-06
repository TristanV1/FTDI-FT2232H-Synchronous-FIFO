`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/23/2024 12:25:57 AM
// Design Name: 
// Module Name: top
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


module top
(
input sysclk,
input comm_clk,
input enable,
input txe,

output [7:0] data,
output wr,
output rd,

output siwu,
output oe_n
);


reg r_enable;
reg r_reset;

wire [7:0] w_data;
wire w_wr;

reg r_siwu;
initial begin
    r_siwu <= 1'b1;
end

reg r_oe_n;
initial begin
    r_oe_n <= 1'b1;
end

reg r_rd;
initial begin
    r_rd <= 1'b1;
end

assign data = w_data;
assign wr = w_wr;
assign siwu = r_siwu;
assign oe_n = r_oe_n;
assign rd = r_rd;

reg [0:559]r_data = 560'b00000000000000010000001000000011000001000000010100000110000001110000100000001001000010100000101100001100000011010000111000001111000100000001000100010010000100110001010000010101000101100001011100011000000110010001101000011011000111000001110100011110000111110010000000100001001000100010001100100100001001010010011000100111001010000010100100101010001010110010110000101101001011100010111100110000001100010011001000110011001101000011010100110110001101110011100000111001001110100011101100111100001111010011111000111111010000000100000101000010010000110100010001000101;

FT2232H_TX TX 
(
    .clk(comm_clk),
    .txe(txe),
    .data(r_data),
    .enable(enable),
    //.reset(r_reset),
    .wr(w_wr),
    .data_out(w_data)
);


endmodule
