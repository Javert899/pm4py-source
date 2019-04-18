from datetime import datetime
from random import randrange

n_traces_per_period = 10

F = open("conceptdrift1.csv", "w")
F.write("case:concept:name,concept:name,time:timestamp,attr1,attr2\n")
curr_timestamp = 0
process = ["A", "B", "C", "D"]
attr1_value = "LOW"
attr2_range = [100, 200]

for i in range(n_traces_per_period):
    attr2_value = randrange(attr2_range[0], attr2_range[1])
    for j in range(len(process)):
        curr_timestamp = curr_timestamp + 1
        date_string = datetime.utcfromtimestamp(curr_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        #print(date_string)
        F.write(str(i)+","+process[j]+","+date_string+","+attr1_value+","+str(attr2_value)+"\n")

curr_timestamp = 100000000
process = ["A", "E", "F", "D"]
attr1_value = "HIGH"
attr2_range = [500, 600]

for i in range(n_traces_per_period+1, 2*n_traces_per_period):
    attr2_value = randrange(attr2_range[0], attr2_range[1])
    for j in range(len(process)):
        curr_timestamp = curr_timestamp + 1
        date_string = datetime.utcfromtimestamp(curr_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        #print(date_string)
        F.write(str(i)+","+process[j]+","+date_string+","+attr1_value+","+str(attr2_value)+"\n")

F.close()