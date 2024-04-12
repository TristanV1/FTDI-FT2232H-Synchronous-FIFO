`timescale 1ns / 1ps

module FT2232H_TX
#(
    parameter DATA_WIDTH = 14    
)
(
    input clk,
    input txe,
    input [0:(DATA_WIDTH*40)-1] data,
    output wr,
    output reg [7:0] data_out
);

parameter total_bits = DATA_WIDTH*40;
parameter total_bytes = $rtoi($ceil((total_bits/8)));

reg r_wr;

initial begin
    r_wr <= 1'b1;
    data_out <= 8'b0;
end

assign wr = r_wr;

parameter IDLE = 2'b00,
          SEND = 2'b01,
          SEND_2 = 2'b10,
          ERROR = 2'b11;

reg [1:0] state;

initial begin
    state <= IDLE;
end

parameter COUNTER_WIDTH = $rtoi($ceil($clog2(total_bytes)));
//parameter COUNTER_WIDTH = $rtoi($ceil($clog2(ADDRESS_WIDTH))) + 1;

reg [COUNTER_WIDTH:0]data_out_COUNTER;

initial begin
    data_out_COUNTER <= 0; 
end

reg [7:0] to_send = 'd0;
reg [7:0] next_data = 0;

reg [9:0] send_counter = 0;
reg buffer_flag = 0;
reg [3:0] buffer_counter = 0;

reg header_sent_flag = 0;

always @ ( posedge clk or posedge txe) begin //txe can go high while clk is low

    if(txe) begin
        state <= IDLE;
        r_wr <= 1'b1;
    end
    
    else begin
        case(state) 

            IDLE:begin
                if(~txe) begin
                    state <= SEND;
                end
                else begin
                    r_wr <= 1'b1;
                    //data_out <= next_data;
                end
            end

            SEND:begin
                if(~txe) begin
                    r_wr <= 1'b0;
                    if (~wr) begin
                        //to_send <= to_send + 1'b1;
                        //data_out <= to_send;
                        if (data_out_COUNTER <= total_bytes-1) begin
                            data_out <= data[8*data_out_COUNTER+:8];
                            data_out_COUNTER <= data_out_COUNTER + 1;
                        end
                        else begin
                            r_wr <= 1'b1;
                            state <= IDLE;
                            data_out_COUNTER <= 0;
                            header_sent_flag <= 1'b0;   
                        end

                    end  
                end

                else begin
                    r_wr <= 1'b1;
                    state <= IDLE;
                end
            end
        endcase
    end
end


endmodule