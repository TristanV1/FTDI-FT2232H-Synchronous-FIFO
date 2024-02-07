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

//reg [1:0] count = 0;
reg [7:0] to_send = 'd0;
reg [7:0] next_data = 0;
//reg [7:0] to_send [3:0];
//initial begin
//    to_send[0] = 8'b00000001;
//    to_send[1] = 8'b00000010;
//    to_send[2] = 8'b00000100;
//    to_send[3] = 8'b00001000;
//end
//always @ (negedge clk) begin
//    if (~clk & ~txe & ~r_wr) begin
//        //count <= count + 1'b1;
//        to_send <= to_send + 1'b1;
//    end
//end

always @ ( posedge clk) begin //txe can go high while clk is low
    
    //if (clk & ~txe & ~r_wr) begin
    //        //count <= count + 1'b1;
    //        to_send <= to_send + 1'b1;
    //end

    if(txe) begin
        state <= IDLE;
        r_wr <= 1'b1;
    end

    case(state) 

        IDLE:begin
            if(~txe) begin
                state <= SEND;
            end
            else begin
                r_wr <= 1'b1;
                data_out <= next_data;
            end
        end

        SEND:begin
            if(~txe) begin
                to_send <= to_send + 1'b1;
                data_out <= to_send;
                r_wr <= 1'b0;
            end
            else begin
                to_send <= to_send - 1'b1;
                r_wr <= 1'b1;
                next_data <= to_send+1;
                state <= IDLE;
            end
        end
    endcase
end


endmodule
