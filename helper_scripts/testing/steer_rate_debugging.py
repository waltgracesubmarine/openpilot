import os
import numpy as np
import json

os.chdir('C:/Git/steer fault exploration')

MPH_TO_MS = 1 / 2.2369

with open('steer_fault_data', 'r') as f:
  raw = f.read().split('\n')[:-1]
data = []
for line in raw:
  if 'nan' in line:
    continue
  data.append(json.loads(line.replace("'", '"').replace('False', 'false').replace('True', 'true')))  # json loads faster than ast
faults = []
for idx, line in enumerate(data):
  if idx == 0:
    continue
  # more 'realistic' data above 10 mph, and remove random faults that occurred on straight roads
  if line['fault'] and line['v_ego'] > 10 * MPH_TO_MS and abs(line['steering_rate']) > 5:
    if not data[idx - 1]['fault']:  # only include first fault, skip rest of concurrent falts
      faults.append(line)

print('Total faults: {}'.format(len(faults)))
faults_steer_rate = [line['steering_rate'] for line in faults]
print('Avg. fault steer rate: {}'.format(np.mean(np.abs(faults_steer_rate))))
print('Std. fault steer rate: {}'.format(np.std(np.abs(faults_steer_rate))))
print('Max fault steer rate: {}'.format(max(np.abs(faults_steer_rate))))
print('Min fault steer rate: {}'.format(min(np.abs(faults_steer_rate))))
faults_towards_center = [line for line in faults if (line['steering_angle'] < 0 and line['steering_rate'] > 0) or (line['steering_angle'] > 0 and line['steering_rate'] < 0)]
faults_away_from_center = [line for line in faults if (line['steering_angle'] < 0 and line['steering_rate'] < 0) or (line['steering_angle'] > 0 and line['steering_rate'] > 0)]
print('Faults occuring when moving towards center: {}'.format(len(faults_towards_center)))
print('Faults occuring when moving away from center: {}'.format(len(faults_away_from_center)))
print('Percentage of faults moving towards center: {}%'.format(round(len(faults_towards_center) / len(faults) * 100, 2)))
