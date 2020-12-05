import skrf as rf
import matplotlib.pyplot as plt
from scipy import constants
import numpy as np

raw_points = 101
NFFT = 16384
PROPAGATION_SPEED = 70.3 #For RG405

_prop_speed = PROPAGATION_SPEED/100
cables = list()
cables.append(rf.Network('test0.s1p'))
cables.append(rf.Network('test1.s1p'))
cables.append(rf.Network('test2.s1p'))

for cable in cables:
  s11 = cable.s[:, 0, 0]
  window = np.blackman(raw_points)
  s11 = window * s11
  td = np.abs(np.fft.ifft(s11, NFFT))

  #Calculate maximum time axis
  t_axis = np.linspace(0, 1/cable.frequency.step, NFFT)
  d_axis = constants.speed_of_light * _prop_speed * t_axis

  #find the peak and distance
  pk = np.max(td)
  idx_pk = np.where(td == pk)[0]
  print(d_axis[idx_pk[0]]/2)

  # Plot time response
  plt.subplot(211)
  plt.plot(s11)
  plt.xlabel('Sample')
  plt.ylabel('Magnitude')
  plt.title('Return Signal')
  plt.subplot(212)
  plt.plot(d_axis, td)
  plt.xlim([0, 2])
  plt.xlabel("Distance (m)")
  plt.ylabel("Magnitude")
  plt.title("Return loss Time domain")
  plt.legend(['test0 - no cable', 'test1 - 14"', 'test2 - 7"'])

plt.tight_layout()
plt.show()
