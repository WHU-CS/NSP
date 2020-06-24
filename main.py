# coding = utf-8
import numpy as np
from tqdm import tqdm
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--input', required=True,
                        help='Input graph file')
    parser.add_argument('--similarity', required=True,
                        help='The comprehensive node similarity file')
    parser.add_argument('--iter', default=100, type=int,
                        help='The number of iteration')
    parser.add_argument('--output', required=True,
                        help='Output noised dataset')
    parser.add_argument('--beta', default= 1.0, type=float,
                        help='The weight of the comprehensive similarity')
    parser.add_argument('--d', default=128, type=int,
                        help='The dimensional size of representations')
    args = parser.parse_args()

    return args


def load_data(file_path_a, file_path_s):
    fr_a = open(file_path_a)
    fr_s = open(file_path_s)

    data_mat_a = []
    data_mat_s = []
    data_arr_s = []
    for line in fr_a.readlines():
        line_arr = line.strip().split('\t')
        data_mat_a.append([int(line_arr[0]), int(line_arr[1])])

    for line in fr_s.readlines():
        line_arr = line.split(',')
        data_mat_s.append([int(line_arr[0]), int(line_arr[1])])
        data_arr_s.append([float(line_arr[2])])

    data_matrix_a = np.array(data_mat_a)
    data_matrix_s = np.array(data_mat_s)
    data_array_s = np.array(data_arr_s)

    max_value = data_matrix_a.max()

    ad_matrix = np.zeros(shape=(max_value+1, max_value+1))
    s_matrix = np.zeros(shape=(max_value+1, max_value+1))
    c_matrix = np.zeros(shape=(max_value+1, max_value+1))
    h_matrix = np.ones(shape=(max_value+1, max_value+1))
    d_matrix = np.zeros(shape=(max_value+1, max_value+1))

    for i in range(len(data_mat_a)):
        a, b = data_matrix_a[i, 0], data_matrix_a[i, 1]
        ad_matrix[a, b] = 1

    for i in range(len(data_mat_s)):
        a, b = data_matrix_s[i, 0], data_matrix_s[i, 1]
        s_matrix[a,b] = data_array_s[i]

    mean_s = data_array_s.mean()
    max_s = data_array_s.max()
    sum_s = s_matrix.sum(axis=1)

    for i in range(max_value+1):
        for j in range(max_value+1):
            if ad_matrix[i, j] > 0 and s_matrix[i, j] < mean_s/10:
                c_matrix[i, j] = 1
                h_matrix[i, j] = 0.5
            elif ad_matrix[i, j] == 0 and s_matrix[i, j] > max_s * 0.5:
                c_matrix[i, j] = s_matrix[i, j] / max_s
                h_matrix[i, j] = 0.5
            elif ad_matrix[i,j] == 0:
                c_matrix[i, j] = 0.1
            else:
                c_matrix[i, j] = 2

            if i == j:
                d_matrix[i][j] = sum_s[i]

    return c_matrix, h_matrix, s_matrix, d_matrix


def NSP_emb(C,H, S, D, r, step, d):
    M = np.random.random((len(C), d))
    U = np.random.random((len(C), d))

    for i in tqdm(range(step)):
        M = M * (np.dot((C * H * H), U) / np.dot((np.dot(M, U.T) * H * H), U))
        U = U * ((np.dot((C.T * H.T * H.T), M) + r * np.dot(S, U)) /
                 (np.dot(np.dot(U, M.T) * H.T * H.T, M) + r * np.dot(D, U)))
    return M, U


def main(args):
    c, h, s, d = load_data(args.input, args.similarity)
    m, u = NSP_emb(c, h, s, d, args.beta, args.iter, args.d)

    fr = open(args.output, 'w')
    for i in range(len(u)):
        fr.write(str(i) + '\t')
        for j in range(128):
            fr.write(str(u[i, j]) + ' ')
        fr.write('\n')
    fr.close()


