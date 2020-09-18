import tkinter.filedialog
import tkinter.simpledialog
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import wfdb
import peakutils
from scipy import signal
import pandas as pd

# To display any physiological signal from physionet, a dat-File needs to have a complementary hea-File in the same directory.
# Otherwise the display won't work 
# awesome tutorial: https://www.youtube.com/watch?v=WyjGCEWU4zY&t=317s

file = tkinter.filedialog.askopenfilename()
file = file[:-4]
n_samples = tkinter.simpledialog.askinteger('Number of samples', 
        	'Type in the number of samples you want to be displayed (example: 3000, 6000, 10000 etc.)')

#Define ecg
record = wfdb.rdrecord(file, sampto=n_samples)
ann = wfdb.rdann(file, 'dat', sampto=n_samples)

#Filerecord
file_record = record.__dict__
#print(file_record)

wfdb.plot_items(signal=record.p_signal, title='ECG Signal',ann_samp=[ann.sample, ann.sample], time_units='samples', figsize=(10,4))

#Detect R-Peaks
signal_slice = np.ndarray.flatten(record.p_signal[0:n_samples])
smooth_signal = signal.cspline1d(signal_slice, lamb=1000)                   #smoothing the signal (filtering)
#r_peak_index = peakutils.indexes(smooth_signal, thres = 0.45, min_dist = 0.1)    # first peak detection option
peak_index = signal.find_peaks_cwt(smooth_signal, widths= np.arange(60,80))     # second peak detection option

fig, ax = plt.subplots()

ax.set_title('Detect R peak')
ax.plot(signal_slice)

p_min_distance = -20  # marking for p-wave example
p_max_distance = -60

t_min_distance = 20  # marking for t-wave example
t_max_distance = 100

for peak in peak_index:
    ax.axvline(x = peak, color = 'r')
    #ax.axvspan(peak + p_max_distance , peak + p_min_distance, alpha = 0.2) # mark for p-wave
    #ax.axvspan(peak + t_max_distance , peak + t_min_distance, alpha = 0.2) # mark for t-wave
plt.show()

#Display HR

RR_intervall = np.diff(peak_index) / record.fs
heart_rate = 60 / RR_intervall  #BPM

fig,ax = plt.subplots()
ax.set_title('Heart Rate Diagram')
ax.plot(heart_rate)
plt.show()

# Display HRV
df = pd.DataFrame(heart_rate, columns =["Heart Rate"], dtype=float)
HRV = [df.describe()]                                                   # the HRV is nothing else as the normal STD of lots of values
messagebox.showinfo('Statistical analysis of the ECG', HRV)

#Display ECG-Record
messagebox.showinfo('Properties of the selected file', file_record)