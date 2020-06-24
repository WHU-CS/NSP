# coding = utf8

from numpy import *
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--input', required=True,
                        help='Input graph file')
    parser.add_argument('--output', required=True,
                        help='Output noised dataset')
    parser.add_argument('--ratio', default=0.2, type=float,
                        help='The added noised ratio')
    args = parser.parse_args()

    return args


def load_data_set(file_path):
    data_mat = []
    fr = open(file_path)
    for line in fr.readlines():
        line_array = line.strip().split(',')
        data_mat.append([int(line_array[0]), int(line_array[1])])
    return data_mat


def create_ad_matrix(data_mat_in):
    data_matrix = mat(data_mat_in)
    int_mat = data_matrix.astype(int)
    max_value = int_mat.max()
    ad_matrix = zeros(shape=(max_value+1, max_value+1))

    for i in range(len(data_matrix)):
        a, b = data_matrix[i, 0], data_matrix[i, 1]
        ad_matrix[a, b] = 1

    return ad_matrix, max_value


def add_noise(ratio, data_mat, ad_matrix, max_value):
    add_edge_num = max_value * ratio
    del_edge_num = max_value * ratio

    index = 0

    while index <= add_edge_num:
        node_1 = random.randint(0, max_value)
        node_2 = random.randint(0, max_value)

        while node_1 == node_2:
            node_2 = random.randint(0, max_value)

        if ad_matrix[node_1, node_2] == 0:
            ad_matrix[node_1, node_2] = 1
            ad_matrix[node_2, node_1] = 1
            index += 1

    index = 0

    while index <= del_edge_num:
        del_index = random.randint(0, len(data_mat))
        del_node1 = data_mat[del_index][0]
        del_node2 = data_mat[del_index][1]

        if ad_matrix[del_node1, del_node2] == 1:
            ad_matrix[del_node1, del_node2] = 0
            ad_matrix[del_node2, del_node1] = 0
            index += 1

    return ad_matrix


def main(args):

    data_matrix = load_data_set(args.input)
    ad_matrix, max_value = create_ad_matrix(data_matrix)

    noise_ad_matrix = add_noise(args.ratio, data_matrix, ad_matrix, max_value)

    out_file = open(args.output, 'w')
    for i in range(max_value):
        for j in range(max_value):
            if noise_ad_matrix[i,j] == 1:
                out_file.write(str(i) + ',' + str(j) + '\n')

    out_file.close()


if __name__ == "__main__":
    main(parse_args())


