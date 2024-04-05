`timescale 1ns / 1ps

module FT2232H_TX
(
    input clk,
    input txe,
    input [7:0] data,
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

reg [7:0] to_send = 'd0;
reg [7:0] next_data = 0;

reg [9:0] send_counter = 0;
reg buffer_flag = 0;
reg [3:0] buffer_counter = 0;

always @ ( posedge clk or posedge txe) begin //txe can go high while clk is low

    if(txe) begin
        state <= IDLE;
        r_wr <= 1'b1;
    end
    
    else begin
        if (~txe && ~wr) begin
            send_counter <= send_counter + 1'b1;
        end

        if (send_counter == 'd509) begin
            buffer_flag <= 1'b1;
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
                    r_wr <= 1'b0;
                    if (wr == 1'b0) begin
                        to_send <= to_send + 1'b1;
                        data_out <= to_send;
                    end  
                end

                else begin
                    //to_send <= to_send - 1'b1;
                    r_wr <= 1'b1;
                    next_data <= to_send;
                    state <= IDLE;
                end
            end
        endcase
    end
end


endmodule