import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


def plot_dataframe_pretty(gm_array, plot_title, total_runs, output_file, use_color_scheme):
    gm_array, labels = gm_array
    rcParams.update({'figure.autolayout': True})
    gm_names = list(gm_array[:, 0])
    first_column = [int(x) for x in gm_array[:, 1]]
    second_column = [int(x) for x in gm_array[:, 2]]
    third_column = [int(x) for x in gm_array[:, 3]]
    a_plus_b = [first_column[i] + second_column[i] for i in range(len(first_column))]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    colors = [None] * 3
    if use_color_scheme:
        colors = ['#D62728', '#9467BD', '#8C564B']
    plotted1 = ax.barh(gm_names, first_column, align='center', label=labels[0], color=colors[0])
    plotted2 = ax.barh(gm_names, second_column, align='center', left=first_column, label=labels[1], color=colors[1])
    plotted3 = ax.barh(gm_names, third_column, align='center', left=a_plus_b, label=labels[2], color=colors[2])
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    patch_count = [0] * 16
    plotted_graphs = [plotted1, plotted2, plotted3]
    for plotted in plotted_graphs:
        for patch in plotted.patches:
            width = patch.get_width()
            patch_y = patch.get_y() + 0.1
            patch_location = patch.get_x() + width / 2 - total_runs * 0.035
            if patch_count[int(round(patch_y))] == 0:
                patch_location = min(max(0, patch_location), total_runs * 0.8)
            elif patch_count[int(round(patch_y))] == 1:
                patch_location = min(max(total_runs * 0.1, patch_location), total_runs * 0.9)
            elif patch_count[int(round(patch_y))] == 2:
                patch_location = min(max(total_runs * 0.2, patch_location), total_runs)
            plt.annotate('{0:.0%}'.format(width / total_runs), (patch_location, patch_y))
            patch_count[int(round(patch_y))] += 1
    ax.set_title(plot_title)
    ax.xaxis.set_visible(False)
    plt.savefig(output_file)


if __name__ == '__main__':
    names = ['NoHandsGamer', 'lnguagehackr', 'Rami94', 'lunaloveee', 'Eddie', 'muzzy', 'Fr0zen', 'Fled', 'Briarthorn',
             'Nalguidan', 'Tincho', 'DreadEye', 'Monsanto', 'killinallday', 'Impact', '-']
    columns = ['playoff', 'rank 9-12', 'relegation']
    contents = [['NoHandsGamer', 9744, 248, 8],
                ['lnguagehackr', 6277, 2768, 955],
                ['Rami94', 4763, 3425, 1812],
                ['lunaloveee', 8409, 1366, 225],
                ['Eddie', 8998, 905, 97],
                ['muzzy', 3572, 3849, 2579],
                ['Fr0zen', 7455, 2045, 500],
                ['Fled', 2443, 3775, 3782],
                ['Briarthorn', 1632, 3200, 5168],
                ['Nalguidan', 4690, 3473, 1837],
                ['Tincho', 6014, 2975, 1011],
                ['DreadEye', 6452, 2722, 826],
                ['Monsanto', 5214, 3371, 1415],
                ['killinallday', 3532, 3573, 2895],
                ['Impact', 805, 2305, 6890],
                ['-', 0, 0, 10000]
                ]
    gm_data_frame = np.array(contents), ['a', 'b', 'c']
    plot_dataframe_pretty(gm_data_frame, 'Grandmaster NA Rankings', 10000, 'output.png', True)
