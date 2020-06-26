# NSP
This repository provides a reference implementation of NSP proposed in "[Noise-Resilient Similarity Preserving 
Network Embedding for Social Networks](https://www.ijcai.org/Proceedings/2019/0455.pdf)",
Zhenyu Qiu, Wenbin Hu, Jia Wu, Zhongzheng Tang and Xiaohua Jia, IJCAI, 2019.

The noise in the network will affect the performance of network embedding. 
The NSP aims to exploit node similarity to address the problem of social network
embedding with noised and learn the a representations for nodes in a social network with noise.

## Basic Usage

### Noise network dataset generation
First of all, to simulate a network with noise, you need to generate the 
noised network dataset by the following command. 

`python add_noise.py --input dataset/xx-network.txt --output Noise_data/xx.txt --ratio x`

#### --input:*input_filename*
The input file should be an edge list and the nodes are numbered starting 
from 0, e.g:
```
0,1
0,2
1,3
1,5
```
#### --output:*output_filename*
The output file contains the an edge list of the network with noise.  

#### --ratio:*noise_ration*
The ratio of noised added, and its value range if [0,1].

### Pairwise node similarity calculation
After obtain a network with noise, you need to calculate multiple pairwise node similarities
by any exiting similarity indexes you interested. [source](https://github.com/CodeZWT/Link-Prediction)

### Comprehensive pairwise node similarity calculation
After obtain the pairwise node similarities by multiple singe similarity indexes,
you need to calculate the the comprehensive pairwise node similarity by the following command.

`python similarity_constr.py --inputs si_1.txt, si_2.txt ... --weights 0.1 0.2 ... --output xx.txt`

#### --inputs:*list of input files*
The list of the input files. The comprehensive pairwise node similarity is calculated 
based on multiple single indexes. For each single index, you need prepare a file contains the 
pairwise node similarity calculated by this index. E.g:
```
0,1,0.5
0,2,0.32
1,2,0.34
```
#### --weights:*list if weights*
The list of the weights. 
### Network embedding
After the above two steps, you can learn the representations of nodes by the following command.

`python main.py --input xx.txt --simialrity xx.txt --iter n1 --beta n2 --d d --output xx.txt`

#### --input:*input_filename*
The input file should be an edge list and the nodes are numbered starting 
from 0.

#### --similarity:*similarity_filename*
The comprehensive pairwise node similarity file.

#### --iter
The number of iteration; the default value is 100

#### --beta
The value of beta; the default value is 1

#### --d
The number of latent dimensions to learn for each nodes; the default is 128

#### --output:*output_filename*
The output is the learned representation of the input network, all lines are
node ID and *d* dimensional representation:
```
0 0.2341233 0.2347435 ...
1 0.3424556 0.3214564 ...
2 0.2123454 0.2857393 ...
...
```

## Baselines
In our paper, we used the following methods for comparision:
* `DeepWalk` 'Deepwalk:online learning of social representations' [source](https://github.com/phanein/deepwalk.git)
* `Line` 'Line: Large-scale information network embedding' [source](https://github.com/thunlp/OpenNE.git)
* `M-NMF` 'Community preserving network embedding' [source](https://github.com/benedekrozemberczki/M-NMF.git)
* `GraRep` 'Grarep: Learning graph representations with global structural information' [source](https://github.com/thunlp/OpenNE.git)
* `Node2vec` ' node2vec: Scalable feature learning for networks' [source](https://github.com/aditya-grover/node2vec.git)


## Citing
If you find NSP useful in your research, we ask that you city the following paper:
```
@inproceedings{DBLP:conf/ijcai/QiuH0TJ19,
  author    = {Zhenyu Qiu and
               Wenbin Hu and
               Jia Wu and
               Zhongzheng Tang and
               Xiaohua Jia},
  title     = {Noise-Resilient Similarity Preserving Network Embedding for Social
               Networks},
  booktitle = {Proceedings of the Twenty-Eighth International Joint Conference on
               Artificial Intelligence, {IJCAI} 2019, Macao, China, August 10-16,
               2019},
  pages     = {3282--3288},
  year      = {2019},
}

```
If you have any questions, please email to qiuzy@whu.edu.cn
