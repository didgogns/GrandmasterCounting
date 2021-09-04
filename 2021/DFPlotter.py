import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


'''
gm_array: tuple of (numpy data, column name) with format
[
player name,
(# of runs with rank 1-2),
(with rank 3-6),
(with rank 7-8),
(with rank 9-12),
(with rank 13-16)
]
plot_title: given by main.py
total_runs: given by main.py (100k)
output_file: location to store output png file
'''


def plot_dataframe_pretty(gm_array, plot_title, total_runs, output_file, use_color_scheme):
    gm_array, labels = gm_array
    rcParams.update({'figure.autolayout': True})
    gm_names = list(gm_array[:, 0])
    number_of_player = len(gm_names)
    column_data = [[int(x) for x in gm_array[:, idx]] for idx in range(1, 6)]
    column_lefts = [[0] * number_of_player] * 5
    column_lefts[0] = [0 for _ in range(number_of_player)]
    for idx in range(1, 5):
        column_lefts[idx] = [column_lefts[idx - 1][i] + column_data[idx - 1][i] for i in range(number_of_player)]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = ['#81AB3F', '#96C74A', '#C1FF61', '#FFF861', '#FF7D61']
    plotted_graphs = [
        ax.barh(gm_names, column_data[idx], align='center', left=column_lefts[idx], label=labels[idx], color=colors[idx])
        for idx in range(5)
    ]
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    patch_count = [0] * 16
    for plotted in plotted_graphs:
        for patch in plotted.patches:
            width = patch.get_width()
            patch_y = patch.get_y() - 0.3
            if patch_count[int(round(patch_y))] > 2:
                patch_y = patch.get_y() + 0.2
            patch_location = patch.get_x() + width / 2
            if patch_count[int(round(patch_y))] == 0:
                patch_location = min(max(0, patch_location), total_runs * 0.87)
            elif patch_count[int(round(patch_y))] == 1:
                patch_location = min(max(total_runs * 0.09, patch_location), total_runs * 0.935)
            elif patch_count[int(round(patch_y))] == 2:
                patch_location = min(max(total_runs * 0.155, patch_location), total_runs * 1)
            elif patch_count[int(round(patch_y))] == 3:
                patch_location = min(max(total_runs * 0.09, patch_location), total_runs * 0.91)
            elif patch_count[int(round(patch_y))] == 4:
                patch_location = min(max(total_runs * 0.155, patch_location), total_runs)
            font_size = 10 if patch_count[int(round(patch_y))] > 2 else 7
            patch_location -= 0.035 * total_runs if font_size == 10 else 0.025 * total_runs
            patch_location = max(0, patch_location)
            plt.annotate('{0:.0%}'.format(width / total_runs), (patch_location, patch_y), fontsize=font_size)
            patch_count[int(round(patch_y))] += 1
    for i in range(number_of_player):
        patch_location = max(0, column_lefts[3][i] / 2 - total_runs * 0.035)
        plt.annotate('{0:.0%}'.format(column_lefts[3][i] / total_runs), (patch_location, i - 0.2))
    ax.set_title(plot_title)
    ax.xaxis.set_visible(False)
    plt.savefig(output_file)


if __name__ == '__main__':
    names = ['NoHandsGamer', 'lnguagehackr', 'Rami94', 'lunaloveee', 'Eddie', 'muzzy', 'Fr0zen', 'Fled', 'Briarthorn',
             'Nalguidan', 'Tincho', 'DreadEye', 'Monsanto', 'killinallday', 'Impact', '-']
    columns = ['playoff', 'rank 9-12', 'relegation']
    contents = [['NoHandsGamer', 100, 100, 9544, 248, 8],
                ['lnguagehackr', 100, 100, 6077, 2768, 955],
                ['Rami94', 100, 100, 4563, 3425, 1812],
                ['lunaloveee', 100, 100, 8209, 1366, 225],
                ['Eddie', 100, 100, 8798, 905, 97],
                ['muzzy', 100, 100, 3372, 3849, 2579],
                ['Fr0zen', 100, 100, 7255, 2045, 500],
                ['Fled', 100, 100, 2243, 3775, 3782],
                ['Briarthorn', 100, 100, 1432, 3200, 5168],
                ['Nalguidan', 100, 100, 4490, 3473, 1837],
                ['Tincho', 100, 100, 6014, 2775, 1011],
                ['DreadEye', 100, 100, 6252, 2722, 826],
                ['Monsanto', 100, 100, 5014, 3371, 1415],
                ['killinallday', 100, 100, 3332, 3573, 2895],
                ['Impact', 100, 100, 605, 2305, 6890],
                ['-', 0, 0, 0, 0, 10000]
                ]
    gm_data_frame = np.array(contents), ['a', 'b', 'c', 'd', 'e']
    plot_dataframe_pretty(gm_data_frame, 'Grandmaster NA Rankings', 10000, 'output.png', True)
