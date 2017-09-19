vlib work

vlog -timescale 1ns/1ns part2.v

vsim control

log {/*}
add wave {/*}

force {load} 0 0, 1 40, 0 60, 1 80, 0 100, 1 140, 0 150 -r 170
force {resetn} 0 0, 1 20
force {clk} 0 0, 1 10 -r 20
force {go} 0 0, 1 80 -r 100
run 500ns