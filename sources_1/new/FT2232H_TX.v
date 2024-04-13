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
          INIT = 2'b10,
          ERROR = 2'b11;

reg [1:0] state;
reg [7:0] HEADER = 8'b11111111;

initial begin
    state <= IDLE;
end

parameter COUNTER_WIDTH = $rtoi($ceil($clog2(total_bytes)));
//parameter COUNTER_WIDTH = $rtoi($ceil($clog2(ADDRESS_WIDTH))) + 1;

reg [COUNTER_WIDTH:0]data_out_COUNTER;

initial begin
    data_out_COUNTER <= 0; 
end

//reg [15:0] time_out_counter = 0;

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
                    r_wr <= 1'b1;

                //time_out_counter <= time_out_counter + 1'b1;
            end

            SEND:begin
                if(~txe) begin
                    r_wr <= 1'b0;
                    if (~wr) begin
                        if (data_out_COUNTER <= total_bytes-1) begin
                            data_out <= data[8*data_out_COUNTER+:8];
                            data_out_COUNTER <= data_out_COUNTER + 1; 
                        end
                        else begin
                            r_wr <= 1'b1;
                            state <= IDLE;
                            data_out_COUNTER <= 0;   
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