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

    colors = ['#81AB3F', '#96C74A', '#ABE356', '#C1FF61', '#FFF861']
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
            if patch_count[int(round(patch_y))] > 3:
                patch_y = patch.get_y() + 0.2
            patch_location = patch.get_x() + width / 2
            if patch_count[int(round(patch_y))] == 0:
                patch_location = min(max(0, patch_location), total_runs * 0.805)
            elif patch_count[int(round(patch_y))] == 1:
                patch_location = min(max(total_runs * 0.09, patch_location), total_runs * 0.87)
            elif patch_count[int(round(patch_y))] == 2:
                patch_location = min(max(total_runs * 0.155, patch_location), total_runs * 0.935)
            elif patch_count[int(round(patch_y))] == 3:
                patch_location = min(max(total_runs * 0.22, patch_location), total_runs * 1)
            elif patch_count[int(round(patch_y))] == 4:
                patch_location = min(max(total_runs * 0.155, patch_location), total_runs)
            font_size = 10 if patch_count[int(round(patch_y))] > 3 else 7
            patch_location -= 0.035 * total_runs if font_size == 10 else 0.025 * total_runs
            patch_location = max(0, patch_location)
            plt.annotate('{0:.0%}'.format(width / total_runs), (patch_location, patch_y), fontsize=font_size)
            patch_count[int(round(patch_y))] += 1
    for i in range(number_of_player):
        patch_location = column_lefts[2][i] / 2 - total_runs * 0.035
        patch_location = min(max(total_runs * 0.035, patch_location), total_runs * 0.82)
        plt.annotate('{0:.0%}'.format(column_lefts[2][i] / total_runs), (patch_location, i - 0.2))
        patch_location = (column_lefts[4][i] + column_lefts[2][i]) / 2 - total_runs * 0.035
        patch_location = min(max(total_runs * 0.09, patch_location), total_runs * 0.91)
        plt.annotate('{0:.0%}'.format((column_lefts[4][i] - column_lefts[2][i]) / total_runs), (patch_location, i - 0.2))
    ax.set_title(plot_title)
    ax.xaxis.set_visible(False)
    plt.savefig(output_file)


if __name__ == '__main__':
    contents = [['Floki', '25085', '49826', '70268', '91242', '763579',
                 '-10511684'],
                ['Leta', '25290', '49681', '69968', '91751', '763310',
                 '-10509250'],
                ['Bunnyhoppor', '25152', '49829', '70233', '91778', '763008',
                 '-10506080'],
                ['Seiko', '25250', '49240', '70204', '92612', '762694',
                 '-10496332'],
                ['Frenetic', '130521', '133733', '134345', '131947', '469454',
                 '-7116691'],
                ['Felkeine', '129245', '133556', '135335', '134396', '467468',
                 '-7080541'],
                ['Rdu', '129527', '133873', '135146', '134570', '466884',
                 '-7073264'],
                ['Furyhunter', '129460', '133755', '135428', '134749', '466608',
                 '-7073060'],
                ['Jarla', '130459', '133522', '134915', '134271', '466833',
                 '-7071878'],
                ['ZloyGruzin', '130501', '133283', '135765', '133977', '466474',
                 '-7065966'],
                ['Casie', '130288', '133927', '134974', '134445', '466366',
                 '-7064759'],
                ['xBlyzes', '132017', '134091', '134592', '133176', '466124',
                 '-7061382'],
                ['Viper', '212567', '181398', '159983', '141760', '304292',
                 '-5356123'],
                ['J4YOU', '214687', '183373', '159731', '139517', '302692',
                 '-5341080'],
                ['SuperFake', '214793', '183439', '159675', '139584', '302509',
                 '-5339891'],
                ['Gaby', '215158', '183474', '159438', '140225', '301705',
                 '-5332019']]
    gm_data_frame = np.array(contents), ['rank 1-2', 'rank 3-4', 'rank 5-6', 'rank 7-8', 'rank 9-16']
    plot_dataframe_pretty(gm_data_frame, 'EU Grandmaster standings', 1000000, 'output.png', True)
