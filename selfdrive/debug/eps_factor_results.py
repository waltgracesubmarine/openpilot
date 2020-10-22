import numpy as np
import matplotlib.pyplot as plt

data = [{'miles': 9.58825, 'factor': 0.8859250863366187}, {'miles': 6.48633, 'factor': 0.8781094350554707}, {'miles': 19.3983, 'factor': 0.9758311448751528},
        {'miles': 74.4485, 'factor': 1.0375213262954404}, {'miles': 1.64407, 'factor': 0.8610264964672084}, {'miles': 3.9699, 'factor': 0.9269691588129849},
        {'miles': 4.08059, 'factor': 0.9145857061505257}, {'miles': 16.715, 'factor': 0.9167369871815209}, {'miles': 1.27698, 'factor': 0.9718697693101586},
        {'miles': 14.2211, 'factor': 0.8996036667864392}, {'miles': 3.89577, 'factor': 1.0405592283780654}, {'miles': 3.92833, 'factor': 0.9989614999749382},
        {'miles': 3.88626, 'factor': 0.8639352841524472}, {'miles': 3.84592, 'factor': 0.9199012714741803}, {'miles': 3.83296, 'factor': 0.8754803559581712},
        {'miles': 75.0482, 'factor': 0.8776047319911336}]

data_filtered = [{'miles': 74.4485, 'factor': 0.9398601268802427}, {'miles': 3.88626, 'factor': 0.8727060958492365}, {'miles': 3.9699, 'factor': 0.9251274335155091},
                 {'miles': 75.0482, 'factor': 0.8803644959678146}, {'miles': 14.2211, 'factor': 0.9043003173790769}, {'miles': 9.58825, 'factor': 0.8965687068323793},
                 {'miles': 6.48633, 'factor': 0.8813382210529348}, {'miles': 1.27698, 'factor': 0.9719863396334021}, {'miles': 16.715, 'factor': 0.9232781407097753},
                 {'miles': 19.3983, 'factor': 0.9833614243304091}, {'miles': 3.89577, 'factor': 0.9121841228586717}, {'miles': 3.92833, 'factor': 0.9994538626794632},
                 {'miles': 3.84592, 'factor': 0.9048143040668307}, {'miles': 1.64407, 'factor': 0.8743246712664462}, {'miles': 4.08059, 'factor': 0.9019872174989512},
                 {'miles': 3.83296, 'factor': 0.8885852782527808}]

data = [i for i in data if i['miles'] < 70]  # remove 2 outliers for now
data_filtered = [i for i in data_filtered if i['miles'] < 70]  # remove 2 outliers for now
plt.scatter([i['miles'] for i in data], [i['factor'] for i in data], label='EPS factor (raw)')
plt.scatter([i['miles'] for i in data_filtered], [i['factor'] for i in data_filtered], label='EPS factor (filtered)')
plt.legend()
plt.xlabel('route length (in miles)')
plt.ylabel('EPS factor')
plt.title('EPS factor plotted from {} routes using linear reg.'.format(len(data)))
plt.show()

data = [i['factor'] for i in data]
data_filtered = [i['factor'] for i in data_filtered]

print(f'Raw data:      mean: {np.mean(data).round(4)}, std.: {np.std(data).round(4)}')
print(f'Filtered data: mean: {np.mean(data_filtered).round(4)}, std.: {np.std(data_filtered).round(4)}')