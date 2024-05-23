import numpy as np
import json
import os
import matplotlib.pyplot as plt
import sys

def load_json_file(filename):
    # Open the JSON file for reading
    with open(filename, 'r') as file:
    # Load its content and turn it into a Python dictionary
        return json.load(file)
    
def get_real(texto):
    return float(texto.split("+")[0])

def extract_json(jsonfile):
    buffers = {}
    for key in jsonfile:
        baselines = []
        for baseline in jsonfile[key]:
            integrations = []
            for integration in baseline:
                channels = np.array([])
                for channel in integration:
                    complex_num = format_to_complex(channel)
                    channels = np.append(channels,complex_num)
                integrations.append(channels)
            baselines.append(integrations)
        buffers[key] = baselines
    return buffers
                

def format_to_complex(s):
    # Remove the 'i' at the end
    s = s.replace('i', '')
    # Split the string into real and imaginary parts
    parts = s.split('+')
    real_part = float(parts[0])
    imag_part = float(parts[1])
    # Create the complex number using numpy
    complex_number = complex(real_part, imag_part)
    return complex_number  

if __name__ == "__main__":
    print("que onda")
    json_path_ref = os.path.abspath("resources/preliminar_result/corr_buffer_512_normalRand.json")
    corr_results = load_json_file(json_path_ref)
    data = extract_json(corr_results)
    plt.figure()
    #plt.plot(np.abs(data['buf_a_xx'][3][0]))
    plt.plot(np.abs(data['buf_a_xy'][0][2]))
    #plt.plot(np.abs(data['buf_a_yy'][3][2]))
    
    for key in data:
        print(len(data[key][0][0]))
    plt.show()