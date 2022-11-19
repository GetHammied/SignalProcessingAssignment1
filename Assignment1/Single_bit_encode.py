import numpy as np
import matplotlib.pyplot as plt


txtfile = open("signal.txt", "r")
read = txtfile.readlines()
data = []                                    #array for data to be saved in
SLEW_STEP_SIZE = 0.001                     #FACTOR FOR MANIUPULATING SLEW RATE
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
original_time = [0]
count_original_time = 0


j = 0
for value in data:
    count_original_time += 0.01
    original_time.append(count_original_time)

n_th_element = int(TIME_STEP / 0.01)                        #calculate which n-th element of original data to pick depending on sampling time step

n_data = data[:: n_th_element]                              #pick out every n-th element of data


for i,value in enumerate(n_data):
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
            bit_queue.append(current_bit)                    #if queue doesnt have 4 elements dont pop last
        else:
            bit_queue.pop(0)                                 #else pop last and add new bit
            bit_queue.append(current_bit)

    bit_encoded.append(current_bit)                                                       #add appropriate bit to bit encoded array
    slew_factor = np.sum(bit_queue) - 2                                                   #calculate difference from mean (offset by 2)
    digital_value.append(digital_value[i] + (slew_factor * SLEW_STEP_SIZE))               #add newly calculated value to array
    i += 1                                                                                #keep count of digital values
    count_t += TIME_STEP                                     #count timesteps
    t.append(count_t)                                        #add timestep to array


#plot results

plt.plot(original_time[:-1],data,"r",label="original data")
plt.plot(t, digital_value,"b",label="bit-encoded signal")
plt.legend(loc="upper right")
plt.title(f'Bit-Encoder with Slew-delta = {SLEW_STEP_SIZE} and time step {TIME_STEP}')
plt.xlabel("time t in seconds")
plt.ylabel("Signalvalue in voltage")
plt.show()




'''
# Optional decoding function for Bit-Signals, 2nd optional argument slew_step determines weight of last 4 bits 

def decode_bits(encoded_bits, slew_step = 0.001):
    bit_queue = []
    digital_value = [0]
    i = 0
    for current_bit in encoded_bits:
        if(len(bit_queue) < 4):
            bit_queue.append(current_bit)                   #if queue doesnt have 4 elements dont pop last
        else:
            bit_queue.pop(0)                                #else pop last and add new bit
            bit_queue.append(current_bit)
        slew_factor = np.sum(bit_queue) - 2                     #offset by 2 to get a value between -2 and 2
        digital_value.append(digital_value[i] + (slew_factor * slew_step))  #calculate digital
        i += 1

    return digital_value
'''







    
