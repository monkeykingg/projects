vlib work

vlog -timescale 1ns/1ns part2.v

vsim combined

log {/*}
add wave {/*}

force {load} 0 0, 1 40, 0 60
force {resetn} 0 0, 1 20
force {clk} 0 0, 1 10 -r 20
force {go} 0 0, 1 80, 0 100
force {coordinate} 2#0000000 0, 2#1100110 40, 2#1111000 80
force {colour_in} 2#010

run 5000 ns