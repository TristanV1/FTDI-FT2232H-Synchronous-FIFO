`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 01/24/2024 06:32:52 PM
// Design Name: 
// Module Name: FT2232H_TX
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


module FT2232H_TX
(
    input clk,
    input txe,
    input data,
    input enable,
    input reset,
    output reg wr,
    output reg [7:0] data_out
);

//parameter IDLE = 2'b00;
//          SEND = 2'b01;

reg r_wr;
always @ (enable,reset) begin
    if (txe == 1'b1) begin
        if (enable == 1'b1) begin
            r_wr <= 1'b1;
        end
        if (reset == 1'b1) begin
            r_wr <= 1'b0;
        end
    end
end


always @ (posedge clk) 
begin : Polling

    if(txe == 1'b0) begin
        wr <= 1'b0;
        data_out <= data;
    end

    else begin
        wr <= 1'b1;
        data_out <= 8'b0;
    end

end
endmodule
