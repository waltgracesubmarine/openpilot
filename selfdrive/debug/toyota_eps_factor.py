#!/usr/bin/env python3
import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model  # pylint: disable=import-error

from tools.lib.route import Route
from tools.lib.logreader import MultiLogIterator

MIN_SAMPLES = 15 * 100


def to_signed(n, bits):
  if n >= (1 << max((bits - 1), 0)):
    n = n - (1 << max(bits, 0))
  return n


def get_eps_factor(lr, plot=False):
  engaged = False
  torque_cmd, eps_torque = None, None
  cmds, eps = [], []

  for msg in lr:
    if msg.which() != 'can':
      continue

    for m in msg.can:
      if m.address == 0x2e4 and m.src == 128:
        engaged = bool(m.dat[0] & 1)
        torque_cmd = to_signed((m.dat[1] << 8) | m.dat[2], 16)
      elif m.address == 0x260 and m.src == 0:
        eps_torque = to_signed((m.dat[5] << 8) | m.dat[6], 16)

    if engaged and torque_cmd is not None and eps_torque is not None:
      # if abs(eps_torque - torque_cmd) <= 100:  # assume current factor is close enough
      cmds.append(torque_cmd)
      eps.append(eps_torque)
    else:
      if len(cmds) > MIN_SAMPLES:
        break
      cmds, eps = [], []

  if len(cmds) < MIN_SAMPLES:
    raise Exception("too few samples found in route")

  lm = linear_model.LinearRegression(fit_intercept=False)
  lm.fit(np.array(cmds).reshape(-1, 1), eps)
  scale_factor = 1. / lm.coef_[0]

  if plot:
    plt.plot(np.array(eps) * scale_factor)
    plt.plot(cmds)
    plt.show()
  return scale_factor


if __name__ == "__main__":
  # to_use = ['14431dbeedbf3558%7C2020-10-19--18-40-06', '14431dbeedbf3558%7C2020-10-17--16-31-47', '14431dbeedbf3558%7C2020-10-19--17-43-38', '14431dbeedbf3558%7C2020-10-16--17-31-39',
  #           '14431dbeedbf3558%7C2020-10-19--12-35-29', 'e010b634f3d65cdb%7C2020-06-10--20-07-25', '14431dbeedbf3558%7C2020-10-19--22-55-58', '14431dbeedbf3558%7C2020-10-19--13-40-57',
  #           '14431dbeedbf3558%7C2020-10-19--14-18-32', '14431dbeedbf3558%7C2020-10-19--22-15-27', '14431dbeedbf3558%7C2020-10-19--12-16-53', '14431dbeedbf3558%7C2020-10-17--21-16-10',
  #           '14431dbeedbf3558%7C2020-10-17--13-32-42', '14431dbeedbf3558%7C2020-10-19--18-33-54', '14431dbeedbf3558%7C2020-10-19--15-23-23', '14431dbeedbf3558%7C2020-10-17--11-14-47']
  to_use = ['a0defbc23933e4f8%7C2020-10-21--20-52-46', 'a0defbc23933e4f8%7C2020-10-21--20-59-45']

  for route in to_use:
    print('working on route: {}'.format(route))
    r = Route(route)
    lr = MultiLogIterator(r.log_paths(), wraparound=False)
    try:
      n = get_eps_factor(lr, plot="--plot" in sys.argv)
      print("\n{}: EPS torque factor: {}\n".format(route, n))
    except Exception as e:
      print(repr(e))
