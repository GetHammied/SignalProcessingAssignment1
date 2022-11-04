
import numpy as np
import matplotlib.pyplot as plt


txtfile = open("SignalProcessing\Assignment1\signal.txt", "r")
read = txtfile.readlines()
data = []                           #array for data to be saved in
SLEW_STEP_SIZE = 0.001                    #FACTOR BY WHICH SLEW IS MULTIPLIED
TIME_STEP = 0.01

#read the data from signal.txt file line by line and safe it in array data

for line in read:
    if line[-1] == "\n":
        data.append(float(line[:-1]))
    else:
        data.append(float(line))


current_bit = 0                      #holds currently calculated next bit
slew_factor = 0                      #variable slew rate based on last 4 bits
count_t = 0                          #counts timesteps
t = [0]                              #holds absolute values of timesteps
digital_value = [0]                  #holds values calculated based on last 4 Bits
bit_encoded = []                     #holds array of all calculated bits
bit_queue = []                       #holds last 4 calculated Bits


for i,value in enumerate(data):
    if(value > digital_value[i]):
        current_bit = 1
        if(len(bit_queue) < 4):
            bit_queue.append(current_bit)                   #if queue doesnt have 4 elements dont pop last
        else:
            bit_queue.pop(0)                                #else pop last and add new bit
            bit_queue.append(current_bit)

    if(value <= digital_value[i]):
        current_bit = 0
        if(len(bit_queue) < 4):
            bit_queue.append(current_bit)                   #if queue doesnt have 4 elements dont pop last
        else:
            bit_queue.pop(0)                                 #else pop last and add new bit
            bit_queue.append(current_bit)

    bit_encoded.append(current_bit)                                                       #add appropriate bit to bit encoded array
    slew_factor = np.sum(bit_queue) - 2                                                   #calculate difference from mean (offset by 2)
    digital_value.append(digital_value[i] + (slew_factor * SLEW_STEP_SIZE))               #add newly calculated value to array
    i += 1                                                                                #keep count of digital values
    count_t += TIME_STEP                                          #count timesteps
    t.append(count_t)                                            #add timestep to array

plt.plot(t[:-1],data,"r",label="original data")
plt.plot(t, digital_value,"b",label="bit-encoded signal")
plt.legend(loc="upper right")
plt.title(f'Bit-Encoder with Slew-factor =  + {SLEW_STEP_SIZE}')
plt.xlabel("time t in seconds")
plt.ylabel("Signalvalue in voltage")
plt.show()





    
