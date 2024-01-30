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
    input [7:0] data,
    //input enable,
    //input reset,
    output wr,
    output reg [7:0] data_out
);

reg r_wr;

initial begin
    r_wr <= 1'b1;
end

assign wr = r_wr;

parameter IDLE = 2'b00,
          SEND = 2'b01,
          DONE = 2'b10,
          ERROR = 2'b11;

reg [1:0] state;

initial begin
    state <= IDLE;
end

reg [1:0] count = 0;
reg [7:0] to_send [3:0];
initial begin
    to_send[0] = 8'b00001010;
    to_send[1] = 8'b10010010;
    to_send[2] = 8'b10100010;
    to_send[3] = 8'b00000000;
end


always @ ( posedge(clk) ) begin
    case(state) 
        
        IDLE:begin
            if(txe == 1'b0) begin
                state <= SEND;
            end
            else begin
                r_wr <= 1'b1;
                data_out <= 8'b0;
            end
        end

        SEND:begin
            if(txe == 1'b0) begin
                data_out <= to_send[count];
                count <= count + 1'b1;
                r_wr <= 1'b0;
            end
            else begin
                r_wr <= 1'b1;
                data_out <= 8'b0;
                state <= IDLE;
            end
        end
    endcase
end


endmodule
