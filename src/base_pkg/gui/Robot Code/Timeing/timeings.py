import time

global clk
global clk2

clk = 0
clk2 = 0

while True:
    time.sleep(0.5)
    clk = time.time()
    clk2 = round(clk)
    print(clk2)

    print(clk2 % 2)
