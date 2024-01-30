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

input txe,

output [7:0] data,
output wr,
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


assign data = w_data;
assign wr = w_wr;
assign siwu = r_siwu;
assign oe_n = r_oe_n;

FT2232H_TX TX 
(
    .clk(comm_clk),
    .txe(txe),
    .data(8'b01010101),
    //.enable(r_enable),
    //.reset(r_reset),
    .wr(w_wr),
    .data_out(w_data)
);

//reg clk_div = 1'b0;
//always @ ( posedge(sysclk) ) begin
//    clk_div <= ~clk_div;
//end
//
//always @ (clk_div) begin
//    if (clk_div == 1'b1) begin
//        r_enable <= 1'b1;
//        r_reset <= 1'b0;
//    end
//    else if (clk_div == 1'b0) begin
//        r_enable <= 1'b0;
//        r_reset <= 1'b1;
//    end
//
//end

endmodule
