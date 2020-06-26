# coding = utf8

import numpy as np
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--inputs', nargs='+', required=True,
                        help='Input pairwise node similarity file')
    parser.add_argument('--weights', nargs='+', required=True,
                        help='The weight list of each similarity')
    parser.add_argument('--output', required=True,
                        help='Output hybrid node similarity dataset')
    args = parser.parse_args()

    return args

def main(args):
    # load similarity files
    si_matrixs = []
    for i in range(len(args.inputs)):
        file_open = open(args.inputs[i])
        node_size = int(file_open.readline())
        si_matrix = np.zeros((node_size, node_size))
        for line in file_open.readlines():
            arr_line = line.strip().split(',')
            node_1 = int(arr_line[0])
            node_2 = int(arr_line[1])
            similarity = float(arr_line[2])
            si_matrix[node_1, node_2] = similarity
            si_matrix[node_2, node_1] = similarity
        si_matrixs.append(si_matrix)

    com_si_matrix = np.zeros((node_size, node_size))

    for i in range(len(args.inputs)):
        max_s = si_matrixs[i].max()
        min_s = si_matrixs[i].min()
        for j in range(node_size):
            for k in range(node_size):
                si_ = (si_matrixs[i][j,k] - min_s) / (max_s - min_s)
                com_si_matrix += args.weight[i] * si_

    out_put = open(args.output, 'w')

    for i in range(node_size):
        for j in range(i+1, node_size):
            out_put.write(str(i) + ',' + str(j) + ',' + str(com_si_matrix[i,j]) + '\n')
    out_put.close()


if __name__ == "__main__":
    main(parse_args())

