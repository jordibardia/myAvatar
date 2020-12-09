import matplotlib.pyplot as plt
import sys

def createGraph(filename):
    loss_vals = []
    for line in open(filename, 'r'):
        vals = line.split()
        if vals[0] != 'Batch':
            continue
        else:
            loss_vals.append(float(vals[len(vals) - 1]))
    
    file_words = filename.split('_')
    plt.plot(loss_vals)
    plt.ylabel("Batch Loss Values")
    plt.xlabel("Training Steps")
    plt.title(file_words[0] + " Batch Loss Progression")
    plt.show()

createGraph(sys.argv[1])