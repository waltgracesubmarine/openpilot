import os
import json
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, GaussianNoise
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

os.chdir('C:/Git/steer fault exploration')

MPH_TO_MS = 1 / 2.2369
scale_to = [0, 1]

with open('steer_fault_data', 'r') as f:
  raw = f.read().split('\n')[:-1]
data = []
for line in raw:
  if 'nan' in line:
    continue
  data.append(json.loads(line.replace("'", '"').replace('False', 'false').replace('True', 'true')))  # json loads faster than ast
faults = []
non_faults = []
for idx, line in enumerate(data):
  if idx == 0 or not line['enabled']:
    continue
  # more 'realistic' data above 10 mph, and remove random faults that occurred on straight roads
  if line['v_ego'] > 1 * MPH_TO_MS and abs(line['steering_rate']) > 5:
    if line['fault']:
      if not data[idx - 1]['fault']:  # only include first fault, skip rest of concurrent falts
        faults.append(line)
    else:
      non_faults.append(line)

# print(faults[0].keys())

FAULTS_TIMES = 2
data = faults + random.sample(non_faults, len(faults) * FAULTS_TIMES)  # twice as more non faults to make the model work for its acc


input_keys = ['apply_accel', 'v_ego', 'new_steer', 'apply_steer', 'steer_rate_limited', 'steering_torque_eps', 'steering_torque', 'a_ego', 'steering_rate', 'steering_angle']
bool_keys = ['steer_rate_limited']
scales = {}
for i in [_i for _i in input_keys if _i not in bool_keys]:
  i_data = [line[i] for line in data]
  scales[i] = [np.min(i_data), np.max(i_data)]

x_train = []
for line in data:
  sample = []
  for i in input_keys:
    if i in bool_keys:
      sample.append(int(line[i]))
    else:
      sample.append(np.interp(line[i], scales[i], scale_to))
  x_train.append(sample)

x_train = np.array(x_train)

y_train = np.array([int(line['fault']) for line in data])

x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2)
print('Total faults: {}'.format(len(faults)))
print('Total non-faults: {}'.format(len(faults) * FAULTS_TIMES))
print('train samples: {}'.format(len(x_train)))
print('test samples: {}'.format(len(x_test)))

model = Sequential()
# model.add(GaussianNoise(0.1, input_shape=x_train.shape[1:]))
model.add(Dense(16, activation='relu'))
model.add(Dense(8, activation='relu'))
# model.add(Dense(1))
model.add(Dense(1, activation='sigmoid'))

model.compile(Adam(amsgrad=True), loss='binary_crossentropy', metrics=['acc'])
model.fit(x_train, y_train, batch_size=6, validation_data=(x_test, y_test), epochs=40)

def eval():  # we only care about the accuracy of predicting a fault, keras might predict 50% or more but in reality fault accuracy is much lower
  correct = []
  for idx, smpl in enumerate(x_train):
    if y_train[idx] == 0:
      continue  # we don't care about the model's accuracy on non faults, it would even out to 50% most likely
    pred = round(model.predict_on_batch(np.array([smpl]))[0][0])
    correct.append(pred == y_train[idx])
  print('Total train predictions: {}'.format(len(correct)))
  print('Train accuracy: {}%'.format(round(correct.count(True) / len(correct) * 100, 2)))
  correct = []
  for idx, smpl in enumerate(x_test):
    if y_test[idx] == 0:
      continue
    pred = round(model.predict_on_batch(np.array([smpl]))[0][0])
    correct.append(pred == y_test[idx])
  print('---\nTotal test predictions: {}'.format(len(correct)))
  print('Test accuracy: {}%'.format(round(correct.count(True) / len(correct) * 100, 2)))

def norm_sample(sample_lst):
  normed = []
  print(input_keys)
  assert len(sample_lst) == len(input_keys)
  for v, k in zip(sample_lst, input_keys):
    if k in bool_keys:
      normed.append(int(v))
    else:
      normed.append(np.interp(v, scales[k], scale_to))
  return normed


eval()
