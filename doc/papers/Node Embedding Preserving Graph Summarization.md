Node Embedding Preserving Graph Summarization

HOUQUAN ZHOU, CAS Key Laboratory of AI Security, Institute of Computing Technology,
Chinese Academy of Sciences, Haidian District, China and University of Chinese Academy of Sciences,
Huairou District, China
SHENGHUA LIU, CAS Key Laboratory of AI Security, Institute of Computing Technology, Chinese
Academy of Sciences, Haidian District, China and University of Chinese Academy of Sciences, Huairou
District, China
HUAWEI SHEN, CAS Key Laboratory of AI Security, Institute of Computing Technology, Chinese
Academy of Sciences, Haidian District, China and University of Chinese Academy of Sciences, Huairou
District, China
XUEQI CHENG, CAS Key Laboratory of AI Security, Institute of Computing Technology, Chinese
Academy of Sciences, Haidian District, China and University of Chinese Academy of Sciences, Huairou
District, China

Graph summarization is a useful tool for analyzing large-scale graphs. Some works tried to preserve original
node embeddings encoding rich structural information of nodes on the summary graph. However, their
algorithms are designed heuristically and not theoretically guaranteed. In this article, we theoretically study
the problem of preserving node embeddings on summary graph. We prove that three matrix-factorization-
based node embedding methods of the original graph can be approximated by that of the summary graph,
and we propose a novel graph summarization method, named HCSumm, based on this analysis. Extensive
experiments are performed on real-world datasets to evaluate the effectiveness of our proposed method. The
experimental results show that our method outperforms the state-of-the-art methods in preserving node
embeddings.
CCS Concepts: • Information systems → Data mining; Social networks;

Additional Key Words and Phrases: Graph summarization, hierarchical clustering, node embedding

ACM Reference Format:
Houquan Zhou, Shenghua Liu, Huawei Shen, and Xueqi Cheng. 2024. Node Embedding Preserving
Graph Summarization. ACM Trans. Knowl. Discov. Data. 18, 6, Article 145 (April 2024), 19 pages.
https://doi.org/10.1145/3649505

This article is partially supported by the National Science Foundation of China under Grants No. U21B2046 and No.
6237075198.
Authors’ address: H. Zhou, S. Liu (Corresponding author), H. Shen, and X. Cheng, CAS Key Laboratory of AI Security,
Institute of Computing Technology, Chinese Academy of Sciences, 6 Zhongguancun South Street, Haidian District, Beijing,
China, 100190 and University of Chinese Academy of Sciences, No. 1 Yanqihu East Road, Huairou District, Beijing, China;
e-mails: zhouhouquan18z@ict.ac.cn, liushenghua@ict.ac.cn, shenhuawei@ict.ac.cn, cxq@ict.ac.cn.

This work is licensed under a Creative Commons Attribution International 4.0 License.

© 2024 Copyright held by the owner/author(s).
ACM 1556-4681/2024/04-ART145
https://doi.org/10.1145/3649505

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:2

1 INTRODUCTION

H. Zhou et al.

Graphs are widely used to represent various objects in real-world and relationships among
them, including social networks, computer networks, and transportation networks, and so
on. And graph-related applications have been widely studied in various fields [21, 38]. Recent
years have witnessed the explosive growth of data size and such large scale brings great
challenge to processing, analyzing and understanding graph data. To tackle this problem, some
researchers resort to graph summarization. Given a graph G, graph summarization finds a
compact representation of it. The typical form is a summary graph by grouping nodes in G
into supernodes and aggregating edges in G into superedges. Figure 1 shows a small example
of graph summarization. The original graph with nine nodes are summarized into a summary
graph with three supernodes and six superedges. The summary graph is smaller and easier to
process and analyze than the original graph and thus can be used to analyze the original graph
[8, 23, 26, 29, 36].

Generally, a good summary graph is expected to keep the properties of the original graph. Most
graph summarization methods aims to preserve the adjacency matrix. However, the adjacency
matrix is only the most fundamental representation of a graph and fails to represent the high-order
properties of a graph. However, node embedding methods have shown great power in capturing
the structural properties and have become a fundamental tool in graph mining. Typically, node
embedding methods learn low-dimensional representations of nodes in a graph, which can be
used for various downstream tasks, such as link prediction, node classification, and anomaly
detection. Moreover, graph summarization may capture high-order relations and help learn
high-quality node embeddings [3, 22]. Thus, it is important to preserve the node embeddings of
the original graph in the summary graph.

Several studies have attempted to learn node embeddings for large-scale graphs by combin-
ing graph summarization and node embedding methods. They first summarize input graphs into
smaller summary graphs, and then learn summary embeddings on them, which are subsequently
recovered to approximate the original node embeddings. The main objective of these approaches
is to preserve the node embeddings of the original graph in the summary graph. Despite the
empirical success of these methods, there is a key limitation that they summarize input graphs
heuristically and do not investigate the theoretical connection between input graphs and summary
graphs.

In this work, we study the theoretical connection between them in node embedding methods.
We analyze three matrix-factorization-based node embedding methods, namely, NetMF [33],
DeepWalk [32], and LINE [40]. These three methods learn node embeddings by factorizing the
proximity matrix [33] of the input graph. By showing that the proximity matrix in these methods
can be approximated by the one of the summary graph, we provide theoretical foundation for
learning node embeddings via summary graphs. We further analyze the error raised by the
summarization and relate it to a trace optimization problem. Based on the analysis, propose
a novel graph Summarization method based on Hierarchical Clustering, named HCSumm, to
minimize the error. We conduct extensive experiments on several real-world datasets and show
that our method outperforms several state-of-the-art methods with better summary.

In summary, our contributions include:

— Theory: We reveal the theoretical connection between the proposed scheme and three node-
embedding learning methods, which provides theoretical foundation for learning node em-
beddings via summary graphs.

— Method: Based on the theoretical analysis, we propose a graph summarization method

HCSumm based on hierarchical clustering.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:3

Fig. 1. Example of graph summarization.

— Effectiveness: We perform extensive experiments on several real-world datasets and the
experimental results show that our HCSumm algorithm outperforms the state-of-the-art
methods with better node embedding preservation.

— Scalability: Our HCSumm algorithm runs fast and scales linearly in the size of graphs.

2 RELATED WORK
2.1 Graph Summarization

Graph summarization methods can be categorized based on many aspects. Here, we categorize
them according to their objectives. See the comprehensive survey [25] for more knowledge about
this topic.

Error of adjacency matrix: These methods try to minimize some error metrics between the
original and reconstructed adjacency matrices and are the main focus of this article. k-Gs [20]
aimed to find a summary graph with at most k supernodes, such that the L1 reconstruction
error is minimized. Riondato et al. [35] revealed the connection between the geometric clustering
problem and the graph summarization problem under multiple error metrics (including L1
error, L2 error and cut-norm error), and they proposed a polynomial-time approximate graph
summarization method based on geometric clustering algorithms. Beg et al. [2] developed a
randomized algorithm SAA-Gs using weighted sampling and count-min sketch [4] techniques
to find promising node pairs efficiently. SpecSumm [27] reformulate the graph summarization
problem as a trace optimization problem and propose a spectral algorithm based on k-means
clustering on the eigenvectors of the adjacency matrix.

Total edge number: In this kind of method, the objective function is defined as number of
edges in summary graph plus edge corrections. In Reference [28], Navlakha et al. proposed two
algorithms: Greedy and Randomized. The former considers all possible node pairs at each step,
and merges the best pair (u, v), which results in the greatest decrease of the total edge number. The
latter samples a supernode as u randomly at each step, checks all other supernodes, finds the best v
and merges them together. This process continues until the summary graph becomes smaller than
a given size. However, both algorithms are computationally expensive. To address this problem,
SWeG [39] reduces the search space by grouping supernodes, according to their shingle values,
and only considers merging node pairs in the same groups. Reference [44] further uses weighted
LSH and scales to large graphs with tens of billions of edges.

Encoding length: These kinds of methods often adopt the MDL principle and use the total
encoding length as the objective function. They typically optimize the total description length
under their proposed encoding scheme. LeFevre and Terzi [20] formulated the graph summa-
rization problem Gs based on the MDL principle, and they proposed three algorithms Greedy,
SamplePairs, and LinearCheck. Lee et al. [19] designed a dual-encoding scheme and proposed

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:4

H. Zhou et al.

Table 1. Major Symbols and Definitions

Symbol
G=(V, E)
Gs =(Vs , Es )
Gr =(V, Er )
vi
Sk
di , Dk
A, As , Ar
D, Ds
L, Ls , Lr
A, L
P, Q
R
E, Es

Definition
Original graph with nodeset V and edgeset E
Summary graph with supernodes Vs and superedges Es
Reconstructed graph with nodeset V and edgeset Er
Node i in the original graph G
Supernode k in the summary graph Gs
Degree of node i and supernode k
Adjacency matrix of original, summary, reconstructed graphs
Degree matrix of original and summary graphs
(Combinatorial) Laplacian matrices of original, summary, reconstructed graphs
Normalized adjacency matrix and normalized Laplacian matrix
Membership and reconstruction matrix in summarization
Restoration matrix for recovering the original embeddings
Embeddings of original graph and summary graph

a sparse summarization algorithm SSumM, which reduces the number of node and sparsifies the
graph simultaneously. By dropping less important edges and encoding them as errors, SSumM is
able to obtain a compact and sparse summary graph. Different from methods mentioned above,
VoG [18] adopted a vocabulary-based encoding scheme, which encodes the graph using frequent
patterns in real-world graphs, such as cliques, stars, and bipartite cores.

Methods mentioned above mainly focus on static simple graphs. There are works aiming to
summarize other types of graphs, including dynamic graphs [1, 34, 37], attributed graphs [11, 16,
42], and streaming graphs [17, 41].

2.2 Graph Summarization Preserving Node Embeddings

There are some existing works that aim to learn node embeddings via summary graphs [25, 43]. The
typical approach is to coarsen the original graph into a smaller summary graph and apply represen-
tation learning methods on it to obtain intermediate embeddings. The embeddings of the original
nodes are then restored with a further refinement step. For example, HARP [3] finds a series of
smaller graphs that preserve the global structure of the input graph and learns representations hi-
erarchically. HSRL [9] learns embeddings on multi-level summary graphs, and concatenate them
to restore original embeddings. MILE [22] repeatedly coarsens the input graph into smaller ones
using a hybrid matching strategy, and finally refines the embeddings via GCN to obtain the original
node embeddings. GPA [24] uses METIS [15] to partition the graphs, and smooths the restored em-
beddings via a propagation process. GraphZoom [5] employs an extra graph fusion step to combine
the structural information and feature information, and then uses a spectral coarsening method
to merge nodes based on their spectral similarities. Embeddings are then refined by a graph filter
to ensure feature smoothness. Reference [7] learns embeddings of the given subset of nodes by
coarsening the remaining nodes, which is not capable to learn embeddings of the remaining ones.

3 CR RECONSTRUCTION SCHEME

In this section, we introduce the configuration-based reconstruction (CR) scheme after intro-
ducing some basic concepts of graph summarization. We list the frequently used symbols in Table 1
for readability.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:5

3.1 Graph Summarization and Reconstruction Scheme
Given an input graph G = (V, E) with n = |V | nodes, graph summarization aims to find a smaller
summary graph Gs = (Vs , Es ) (with ns = |Vs | nodes) that preserves the structural information of
the original graph. The supernode set Vs forms a partition of the original node set V such that
every node v ∈ V belongs to exactly one supernode S ∈ Vs . The supernodes are connected via
superedges Es , which are weighted by the sum of original edges between the constituent nodes.
That is, superedge As (k, l) between supernodes Sk , Sl is defined as

(cid:2)

(cid:2)

As (k, l) =

A(i, j).

vi ∈Sk

vj ∈Sl

(1)

(cid:3)

Degree of supernodes is defined as the sum of node degrees within supernode Sp , i.e., d
=
i ∈Sp di . The adjacency matrix of the summary graph As can be formulated using a membership

(s)
p

matrix P ∈ Rns ×n as As = PAP(cid:4), where

P(k, i) =

(cid:4)

1
0

if vi ∈ Sk ,
otherwise.

(2)

One could find a good summary graph by making the summary graph close to the original
graph, for example, minimizing dis(G, Gs ) for some distance metric dis. However, the summary
graph and the original graph have different size, and it is difficult to directly compare two graphs
with different sizes.

This issue can be avoided by introducing a reconstructed graph. Given the summary graph Gs ,
the original graph G can be approximated with the reconstructed graphs Gr with adjacency matrix
Ar defined as

Ar = QAs Q
(3)
where Q ∈ Rn×ns is the reconstruction matrix. The reconstructed graph Gr has the same size with
the original graph G, and is comparable to it. For example, one can minimize the difference of
adjacency matrices (cid:5)A − Ar (cid:5) for some matrix norm. Note that Ar can be seen as a low-rank
approximation of the original A.

(cid:4) ,

A simple and intuitive reconstruction method is the uniform reconstruction scheme, which is

widely applied in current works. The corresponding Q and Ar are

(cid:4)

Q(i, k) =

1
|Sk |
0
Ar (i, j) = 1

if vi ∈ Sk ,
otherwise,

(4)

(5)

|Sk | As (k, l) 1
|Sl | ,
where Sk and Sl are the supernodes to which node i and node j belong, respectively.

vi ∈ Sk , vj ∈ Sl ,

It can be seen from Equation (5) that the edges between two supernodes Sp and Sl , i.e., As (k, l),
are equally assigned to each node pair between them, and each node pair has the same connec-
tion weight. Thus, this approach assumes the G(n, p) random graph model (or Erdős-Rényi model
equivalently) [6] and SBM (Stochastic Block Model) [12]. However, real-world graphs have highly
skewed degree distributions. Therefore, this uniform reconstruction scheme is not suitable for
real-world graphs.

Thus, we introduce the configuration-based reconstruction scheme [45]. Different from the

uniform reconstruction scheme, it reconstructs Ar based on node degrees:

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:6

H. Zhou et al.

Definition 1. (CR Scheme) The configuration-based reconstruction scheme (CR scheme)

calculates Ar (i, j) as follows:

Ar (i, j) = di
Dk

dj
Dl
where Sk and Sl are the supernodes to which node i and node j belong, respectively. We use di
and dj to denote the degrees of nodes i and j; and Dk and Dl to denote the degrees of supernodes
Sk and Sl . The corresponding Q matrix is

vi ∈ Sk , vj ∈ Sl ,

As (k, l)

(6)

,

(cid:4)

Q(i, k) =

di
Dk
0

if vi ∈ Sk ,
otherwise.

(7)

In this way, the reconstructed edge weight Ar (i, j) is proportional to the product of endpoints’
degrees. This approach is based on the configuration model [30] and the DC-SBM (degree-
corrected stochastic block model) [14], which has proved successful
in modularity-based
community detection [31].

Note that the proposed CR scheme is able to preserve the degrees of nodes, as show below:

Property 1 (Degree Preservation).

n(cid:2)

j=1

Ar (i, j) = di =

n(cid:2)

j=1

A(i, j) .

Proof.

(cid:2)

j

Ar (i, j) =

(cid:2)

(cid:2)

l

j ∈Sl

di
Dk

As (k, l)

=

dj
Dl

(cid:2)

l

di
Dk

As (k, l) = di .

Thus, we also call the CR scheme degree-preserving scheme.

(8)

(cid:2)

4 CONNECTION WITH NODE EMBEDDING METHODS
In this section, we present the connection of the proposed CR scheme and three matrix-
factorization-based node embedding methods: DeepWalk [32], LINE [40], and NetMF [33]. In short,
we show that learning node embeddings on a summary graph with restoration is equivalent to
learning embeddings on the reconstructed graph under the CR scheme.

4.1 Matrix-factorization-based Node Embedding Methods

DeepWalk. DeepWalk [32] is an unsupervised graph representation learning method inspired by
the success of word2vec in text embedding. It generates random walk sequences and treats them
as sentences that are later fed into a skip-gram model with negative sampling to learn latent node
representations.

LINE. LINE [40] learns embeddings by optimizing a carefully designed objective function that

aims to preserve both the first-order and second-order proximity.

NetMF. NetMF aims to unify some node embedding methods into a matrix factorization
framework [33]. It shows that DeepWalk is implicitly approximating and factorizing the following
proximity matrix:

(cid:5)

(cid:5)

(cid:6)

(cid:6)

M (cid:2) log

vol(G)
b

1
T

T(cid:2)

(D

τ =1

−1A)τ

−1

D

,

(9)

where T and b are the context window size and the number of negative samples in DeepWalk,
respectively.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:7

Similarly, LINE is equivalent to factorizing a similar matrix to Equation (9) and is a special case

of DeepWalk for T = 1:

M (cid:2) log

(cid:7)

vol(G)
b

(cid:8)

−1AD

D

−1

.

We throw out the element-wise log function and constant factors away, and extract a form of

kernel matrix defined as follows.

Definition 2 (Kernel Matrix).

(10)
where τ is a positive integer, and A and D are adjacency matrix and degree matrix of G, respectively.
We omit the subscript τ if there is no ambiguity.

Kτ (G) (cid:2) (D

−1A)τ D

−1,

4.2 Approximating Kernel Matrix
Now, we show that, under the configuration-based reconstruction scheme [see Equations (6)
and (7)], the kernel matrix on the original graph, K(G), can be approximated with the same kernel
matrix on the summary graph, K(Gs ), in a closed form.

Theorem 1. Given Ar (reconstructed by the configuration-based scheme, see Equation (6)) as a low-
rank approximation of the original adjacency matrix A, the kernel matrix of G can be approximated
by the one on Gs as follows:

K(G) ≈

(cid:9)

(cid:10)τ

−1

D
(cid:10)τ

−1Ar
D
(cid:9)
−1
= R
s As
D
= R K(Gs ) R

D
(cid:4),

(cid:4)

−1
s R

(11)

(12)

(cid:2)

(13)

where R ∈ Rn×ns is the restoration matrix:

R(i, p) =

(cid:4)

1
0

if vi ∈ Sk ,
otherwise,

Proof. See Appendix.

Corollary 1. Let τ takes values in {1, 2, . . . ,T } and sum them together, we have

T(cid:2)

(D

τ =1

−1A)τ D

−1 ≈

T(cid:2)

τ =1

(D

−1Ar )τ D

−1 = R

where R is defined in Equation (12).

4.3 Approximating Node Embeddings

(cid:6)

(D

−1
−1
s As )τ D
s

(cid:4),

R

(cid:5)

T(cid:2)

τ =1

Based on Theorem 1, we now discuss how to approximate node embeddings for the original nodes.
Since DeepWalk and LINE can be viewed as special cases of NetMF, we focus on NetMF in the
following discussion.

Theorem 2. Embeddings learned by NetMF on the original graph G, E, can be approximated
by embeddings learned by NetMF on the summary graph Gs , Es , using the restoration matrix R in
Equation (12), i.e.,

E ≈ R Es .

(14)

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:8

H. Zhou et al.

Proof. Consider Ar as a low-rank approximation of A, and replace A by Ar in the NetMF matrix.

According to Corollary 1:

M = log

≈ log

= log

(cid:5)

(cid:5)

(cid:5)

vol(G)
bT

vol(G)
bT

vol(G)
bT
(cid:5)

T(cid:2)

τ =1
T(cid:2)

(D

−1A)τ D

−1

(cid:6)

(cid:6)

(D

−1Ar )τ D

−1

τ =1
(cid:5)

T(cid:2)

R

τ =1
(cid:5)

(cid:6)

(cid:6)

(D

−1
−1
s As )τ D
s

(cid:4)

R

(cid:6) (cid:6)

(D

−1
−1
s As )τ D
s

(cid:4)

· R

T(cid:2)

τ =1

vol(G)
bT

1 = R · log

= R Ms R

(cid:4).

Here Ms is the corresponding matrix DeepWalk factorizing on summary graph Gs .

Suppose Ms is factorized into Ms = Xs Y(cid:4)

s , then M ≈ (RXs )(RYs )(cid:4). That is, embeddings of
original graph G can be approximated by embeddings learned on summary graph Gs with a
restoration matrix R:

E ≈ R · Es .

(15)
(cid:2)

According to Theorem 2 and the definition of R matrix (R(i, p) = 1 if vi ∈ Sp ), we can conclude
that nodes in the same supernode get the same embeddings after restoration. This approach,
is exactly the way how related works (including HARP, MILE, and GraphZoom) restore the
embeddings. Thus, Theorem 2 provides a theoretical interpretation for the restoration step of
existing methods.

5 PROPOSED METHODS

In this section, we first reveal that the error of kernel matrix is closely related to the error of
the normalized adjacency matrix. Then, by showing that the latter error is bounded by a trace
maximization objective function, we propose a summarization method HCSumm based on spectral
clustering.

5.1 Kernel Matrix Error Analysis
From the previous section, it is known that the kernel matrix is closely related to many graph
properties and graph mining tasks. Hence, it is important to preserve the kernel matrix of the
original graph. One may ask that how much the error of kernel matrix is introduced by replacing
A by Ar ? The following theorem gives a brief analysis.

Theorem 3. By replacing A by Ar , the error of kernel matrix is bounded by

(cid:5)Kτ (G) − Kτ (Gs )(cid:5)F ≤ C · τ · (cid:5)D

− 1

2 AD

− 1
2 − D

− 1

2 Ar D

− 1
2 (cid:5)F,

(16)

where C = (cid:5)D− 1

2 (cid:5)2

2 is a constant only depending on the input graph.

1This equation holds, since each row of R contains exactly one non-zero value “1.” Thus, we can take it out of the log
function.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:9

Proof. Note that the kernel matrix Kτ (G) can be rewritten as
− 1
2 .

Kτ (G) = D

− 1
2 )τ D

− 1
2 (D

2 AD

− 1

Then,

=

=

(cid:12)

− 1
2

(cid:5)Kτ (G) − Kτ (Gr )(cid:5)F
(cid:11)
(cid:11)
− 1
(D
(cid:11)D
(cid:11)
(cid:11)
(cid:11)
(cid:11)
(cid:11)(D
(cid:11)D

2 AD

2 AD

(cid:11)
(cid:11)
(cid:11)

− 1

·

2

− 1
2
(cid:11)
2
(cid:11)
− 1
(cid:11)(D

− 1
2 )τ − (D

− 1

2 Ar D

− 1

2 )τ

(cid:13)

D

− 1
2 )τ − (D

− 1

− 1

2 )τ

2 Ar D
(cid:11)
(cid:11)
(cid:11)
F

2 )τ

− 1

,

= C ·

2 AD

− 1
2 )τ − (D

− 1

2 Ar D

(cid:11)
(cid:11)
(cid:11)

F

− 1
2

(cid:11)
(cid:11)
(cid:11)
F

where C = (cid:5)D− 1

2 (cid:5)2
2
Denote A = D− 1

= d −1
2 AD− 1

min is a constant only depending on the input graph.

2 and Ar = D− 1
Aτ − Aτ
r

2 Ar D− 1
= (Aτ −1 − Aτ −1

r

2 for notation simplicity, we have

)A + Aτ −1

r

(A − Ar ).

And

(cid:5)Aτ − Aτ
r

(cid:5)F ≤ (cid:5)A(Aτ −1 − Aτ −1

r

)(cid:5)F + (cid:5)Aτ −1

r

(A − Ar )(cid:5)F

≤ (cid:5)A (cid:5)2(cid:5)Aτ −1 − Aτ −1

r

(cid:5)F + (cid:5)Ar (cid:5)τ −1

2

(cid:5)A − Ar (cid:5)F

((cid:5)A (cid:5)2 ≤ 1 and (cid:5)Ar (cid:5)2 ≤ 1)

≤ (cid:5)Aτ −1 − Aτ −1

r

(cid:5)F + (cid:5)A − Ar (cid:5)F.

Applying it recursively, we have

(cid:5)Aτ − Aτ
r

(cid:5)F ≤ τ (cid:5)A − Ar (cid:5)F.

Thus,

(cid:5)Kτ (G) − Kτ (Gr )(cid:5)F ≤ C · τ ·

(cid:11)
(cid:11)
(cid:11)D

− 1

2 AD

− 1
2 − D

− 1

2 Ar D

− 1
2

(cid:11)
(cid:11)
(cid:11)
F

,

where C = (cid:5)D

1
2

−c (cid:5)2

2 is a constant only depending on the input graph.

(17)

(cid:2)

5.2 HCSumm
Theorem 3 states that the error of τ -order kernel matrix is bounded by τ times the error of A.
Hence, we aim to design algorithms minimizing the error of A − Ar to preserve the kernel matrix.

Lemma 1. Let Ar be the adjacency matrix of Gr . Then, Ar can be written as

Ar = Π · A · Π,

where Π = YY(cid:4) is a projection matrix on the column space of D
(cid:4) √

(cid:4) √

1

2 P(cid:4) and Y = D

1

2 P(cid:4)(PDP)− 1
2 :

Y(i, k) =

di√
Dk

0

if i ∈ Sk ,
otherwise,

di dj
Dk

Π(i, j) =

0

Proof. Let Ar be the normalized adjacency matrix of Gr . Then,

Ar (i, j) = 1√
di

Ar (i, j) 1(cid:14)
dj

= 1√
di

di
Dk

As (k, l)

dj
Dl

1(cid:14)
dj

=

if i, j ∈ Sk ,
otherwise.

√

di
Dk

As (k, l)

(cid:14)

dj
Dl

.

(18)

(19)

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:10

H. Zhou et al.

And given the definition of Π in Equation (19), we have

(ΠAΠ)(i, j) =

=

=

=

(cid:2)

a ∈Sk,b ∈Sl
(cid:2)

a ∈Sk,b ∈Sl
(cid:2)

a ∈Sk,b ∈Sl
√

Π(i, a) A(a, b)
(cid:14)
didj
√

dida
Dk

A(a, b)
√
dadb
(cid:14)

Π(b, j)

(cid:14)

dbdj
Dl

√

di
Dk
(cid:14)

A(a, b)

dj
Dl

di
Dk

As (k, l)

dj
Dl

= Ar (i, j).

(cid:2)

From the above lemma, the error of the normalized adjacency matrix can be formulated as (cid:5)A −

ΠAΠ(cid:5)F, which is further bounded by
(cid:5)A − ΠAΠ(cid:5)F = (cid:5)A − ΠA + ΠA − ΠAΠ(cid:5)F

≤ (cid:5)A − ΠA (cid:5)F + (cid:5)ΠA − ΠAΠ(cid:5)F
≤ (cid:5)A − ΠA (cid:5)F + (cid:5)A − AΠ(cid:5)F
= (cid:5)A − ΠA (cid:5)F + (cid:5)ΠA − A (cid:5)F
= 2(cid:5)A − ΠA (cid:5)F.

(Π is a projection matrix and hence (cid:5)Π(cid:5)2 = 1)

Although there is a factor of 2, we find that these two terms are very close in practice. Hence, it

is a good choice to use (cid:5)A − ΠA (cid:5) as an approximation of (cid:5)A − ΠAΠ(cid:5)F.

(cid:5)A − ΠA (cid:5) is easier to analyze and equivalent to a trace optimization problem:

(cid:5)A − ΠA (cid:5)2
F

= tr((A − ΠA)(A − ΠA)(cid:4))
= tr(AA − AΠA − ΠAA + ΠAAΠ)
= tr(A2) − tr(ΠA2)
= tr(A2) − tr(Y

(cid:4)A2Y).

(20)

Since tr(A2) is a constant, minimizing (cid:5)A − ΠA (cid:5)2

F is equivalent to maximizing tr(Y(cid:4)A2Y)
where Y(cid:4)Y = I, which is a trace maximization problem. If we relax the constraint that the Y is a
discrete solution obtained from a summary graph, then this trace maximization problem can be
easily solved by calculating the first k large eigenvectors of A2 using the Rayleigh-Ritz theorem.
Since A2 and A share the eigenvectors, we can use the first k singular vectors of A instead to
avoid calculating A2.

To obtain the discrete solution from the continuous solution, the typical way is using the k-
means algorithm to partition the rows of Y into k clusters. However, the cluster number in k-means
is relatively small compared to the summary graph size in graph summarization problem, which
makes k-means insufficient in our scenario. Thus, we use hierarchical clustering with ward link-
age (also known as Ward’s method) instead. Ward’s method is a hierarchical clustering algorithm
sharing the same objective function with k-means but working in a bottom-up approach. It starts
with each data point as a cluster and iteratively merge the cluster pair raising the minimal cost
increment.

Based on the above analysis, we propose a graph summarization algorithm HCSumm using hi-
erarchical clustering, described in Algorithm 1. First, it computes the first d singular vectors of
A. To enhance the efficiency, we use randomized SVD [10] instead of eigen-decomposition to

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:11

ALGORITHM 1: HCSumm
Input: Graph G = (V, E, A), Summary graph size k, Singular vector number d
Output: Summary graph Gs
1: A ← normalized adjacency matrix
2: Z ← randomizedSVD(A, d)
3: P ← partition the rows of Z into k clusters using Ward’s method
4: Gs ← construct the summary graph using P
5: return Return Gs

ALGORITHM 2: HCSumm-Large
Input: Graph G = (V, E, A), Summary graph size k, Singular vector number d
Output: Summary graph Gs
1: A ← normalized adjacency matrix
2: Z ← randomizedSVD(A, d)
3: n ← |V |
4: while n > k do
5:

6:
7:

x ← arg minv deg(v)
y ← arg minv (cid:5)Z [x] − Z [v](cid:5)2
Merge x and y
n ← n − 1

8:
9: end while
10: return Return Gs

calculate the singular vector of A. Then, it clusters the rows of Z into k clusters using Ward’s
method. Finally, the summary graph is constructed according to the clustering result partition P
and returned.

Algorithm 1 still bears the efficiency problem facing large input graphs, since Ward’s method
needs to keep track of all the pairwise distances between clusters. Thus, we propose HCSumm-
Large (Algorithm2) for large-scale graphs using a degree heuristic. In each step, it chooses a node
x with the minimum degree and find another node y nearest to x. To find the closest node to x, we
use faiss [13] library and build a simple IVF index on Z . Then, it merges the two nodes together
and repeats the process until all the nodes are merged into k supernodes.

6 EXPERIMENTS

In this section, we design experiments to answer the following research questions:

— Summary Quality: How well does HCSumm preserve the normalized adjacency matrix of

input graphs?

— Node Embedding Preservation: How well does HCSumm preserve the node embeddings

of input graphs?

— Scalability: How does HCSumm scale with the input graph size?

6.1 Experimental Setup

Datasets. We evaluate HCSumm on four real-world social network datasets frequently used in
node embedding learning. The statistics of these datasets are shown in Table 2. Cora dataset is a
citation network of machine learning papers and labels are the research areas of papers. BlogCat-
alog dataset is a social network of bloggers at BlogCatalog website and labels are the interests of

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:12

H. Zhou et al.

Table 2. Dataset Statistics

Dataset
Cora
BlogCatalog
Flickr
YouTube

#Nodes
2,307
10,312
89,250
1,138,499

#Edges
5,278
667,966
5,899,882
2,990,443

#Labels
7
39
195
47

bloggers. Flickr dataset is a user social network on Flickr website and labels are the user interest
groups. YouTube dataset is a network of users on YouTube website and labels are the user interest
tags.

Baselines. We compare our HCSumm with two baselines, GraphZoom and SpecSumm. Graph-
Zoom2 is the state-of-the-art graph summarization method for learning node embeddings and
show significant better performance than earlier methods such as HARP and MILE. SpecSumm3
shares the similar approach with HCSumm, but aims at minimize the reconstruction error of the
adjacency matrix. It computes the first d eigenvectors of the adjacency matrix and uses mini-batch
k-means to obtain the summary graph.

Summary sizes. We summarize input graphs with different summary sizes and evaluate the
quality of them. To make a fair comparison, we should evaluate the summary quality of different
methods with the same summary sizes. For our method HCSumm and SpecSumm, the summary
size is a parameter that can be set by users. For GraphZoom, it is a multi-level summarization
method and produces summary graphs with different sizes in each level. Summary size of each
level is fixed and users can only set the number of level but not the summary size. For more details,
please refer to the original paper [5]. Thus, to make a fair comparison, we set the summary sizes
in HCSumm and SpecSumm to the same values as GraphZoom’s summary sizes in different levels.

Implementation details. We implement HCSumm in Python3. For SpecSumm and GraphZoom,
we use the source code released by the authors. All experiments are performed on a machine with
a 2.4 GHz Intel Xeon E5-2640 CPU and 128 GB memory. GraphZoom has a variant version utilizing
node features. We use the feature-fusion version of GraphZoom on Flickr, since it has node features
and use the vanilla version on other datasets without node features. For our method, we run the
vanilla HCSumm (Algorithm 1) on the BlogCatalog dataset and HCSumm-Large (Algorithm 2) on
the other two datasets.

6.2 Summary Quality
We first evaluate the summary graph quality of different methods. Two metrics, (cid:5)A − ΠAΠ(cid:5)F and
(cid:5)A − ΠA (cid:5)F are applied to measure the quality. The former is the Frobenius norm of the difference
between the original normalized adjacency matrix and the reconstructed one, and the latter is the
objective function in the trace optimization problem (see Equation (20)). Due to the memory limit,
we only evaluate on BlogCatalog and Flickr datasets.

Experimental Results. The results are listed in Table 4. From the table, we notice that the
error1 and error2 terms, i.e., (cid:5)A − ΠAΠ(cid:5)F and (cid:5)A − ΠA (cid:5)F, are very close and the ratio of them
is far from the theoretical bound of 2. Thus, it is reasonable to use (cid:5)A − ΠA (cid:5)F as a surrogate of
(cid:5)A − ΠAΠ(cid:5)F. For BlogCatalog and Cora dataset, our method achieves the smallest error measures.
For Flickr dataset, HCSumm always outperforms SpecSumm. Compared to GraphZoom, HCSumm

2https://github.com/cornell-zhang/GraphZoom
3https://version.helsinki.fi/ads/specsumm

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:13

Table 4. Error Measures of Summary Graphs

Size

1170
(r = 43.21%)

523
(r = 15.62%)

230
(r = 9.97%)

Method
error1 error2
HCSumm 15.93 17.37
20.56
GraphZoom 18.35
SpecSumm 20.70
23.39
HCSumm 20.56 21.38
23.88
GraphZoom 22.78
SpecSumm 24.17
25.81
HCSumm 24.29 25.10
25.17
26.62

GraphZoom 24.31
SpecSumm 25.91

(a) Cora

Size

6997
(r = 67.85%)

4539
(r = 44.01%)

2891
(r = 28.03%)

Method
HCSumm

error1 error2
5.96
4.60
6.81
GraphZoom 5.30
6.95
SpecSumm 5.39
7.72
6.30
HCSumm
8.29
GraphZoom 7.01
8.23
SpecSumm 6.78
8.54
7.33
HCSumm
8.93
GraphZoom 8.04
SpecSumm 7.74
8.88
(b) BlogCatalog

Size

22525
(r = 25.24%)

7482
(r = 8.38%)

2954
(r = 3.31%)

Method
HCSumm

error1 error2
29.14
26.86
GraphZoom 24.37 27.83
29.19
SpecSumm 26.48
29.84
28.94
HCSumm
GraphZoom 28.24 29.62
SpecSumm 28.96
30.01
HCSumm 29.42 29.91
30.01
30.13

GraphZoom 29.43
SpecSumm 29.68
(c) Flickr

r stands for the summary ratio. error1 and error2 refer to (cid:5) A − Π A (cid:5)F and (cid:5) A − Π AΠ (cid:5)F, respectively.

Fig. 2. Kernel matrix error of BlogCatalog datasets. The x-axis is the summary graph size. Our method
achieves the smallest kernel matrix error.

does not achieve the smallest error when the summary size is 22,525. As the summary size goes
smaller, the errors of HCSumm gradually approaches that of GraphZoom and outperforms it when
the summary size is 2,954.

Kernel Matrix Error. We also calculate the kernel matrix (see Equation (9)) error of different
summarization ratios. The kernel matrix error is defined as the Frobenius norm of the difference
between the original kernel matrix and the kernel matrix of the summary graph. Since the node
embeddings are directly from the kernel matrix, the kernel matrix error can reflect how well the
node embeddings are preserved by different methods. Due to the memory limit (the kernel matrix
is dense), we only calculate the kernel matrix error on BlogCatalog dataset. The results are shown
in Figure 2. From the results, we can see that HCSumm achieves the smallest kernel matrix error
and thus preserves the node embeddings best. This result is consistent with the node classification
performance in the next section.

6.3 Node Embedding Preservation

In this experiment, we aim to evaluate how well HCSumm preserves the node embeddings.
We evaluate it by downstream node classification tasks. We run NetMF and DeepWalk on the
summary graphs and restore the embeddings of the original nodes (Equation (15)). Then, we
use the restored embeddings to train a Logistic Regression classifier and evaluate the perfor-
mance. We set the training ratios to {0.20, 0.40, 0.60, 0.80} on BlogCatalog and Cora dataset and
{0.02, 0.04, 0.06, 0.08} on Flickr and YouTube dataset and report the mean accuracy (for Cora
dataset) and the micro f1 scores and macro f1 scores (for other three datasets) of five average runs.
The dimension of the embedding is set to 128 in all experiments. We do not run SpecSumm on
YouTube dataset due to its long run time on such a large dataset.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:14

H. Zhou et al.

Fig. 3. NetMF performance on the node classification task.

6.3.1 NetMF. Parameter Settings. We set T = 10 in NetMF. For graphs larger than 20,000

nodes, we use the variant NetMF-large [33] instead of the original NetMF.

Experimental Results. Mean micro f1 scores and macro f1 scores of five average runs are
shown in Figure 3.4 It can be seen that both the micro f1 scores and macro f1 scores drop af-
ter summarization. Compared to baselines, our HCSumm method achieves the slightest drop on
Cora, BlogCatalog and Flickr dataset. On YouTube dataset, despite that GraphZoom outperforms

4NetMF cannot run on the YouTube dataset (exceeds memory limit), hence some results are missing in the figure.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:15

Fig. 4. DeepWalk performance on the node classification task.

HCSumm when the summary size is GraphZoom shows an unstable performance on different sum-
mary sizes. For example, the micro f1 score drops under 0.28 when the summary size is 48,532 and
goes up to 0.34 when the summary size is 21,669. On the contrary, HCSumm method achieves a
stable and relative good performance on all summary sizes. Overall, our HCSumm method can pre-
serve the node embedding information better than baselines and are consistent with the results in
the previous section.

6.3.2 DeepWalk. Parameter Settings. The window size and the negative samples b are set to
10 and 1, respectively. The number of walks per node is set to 10 and the length of each walk is 80.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:16

H. Zhou et al.

Fig. 5. Scalability of HCSumm method.

Experimental Results. Similar to NetMF, we report the mean micro f1 scores and macro f1
scores of five average runs in Figure 4. HCSumm outperforms other baselines on Cora, BlogCatalog,
and Flickr dataset and is slightly worse than GraphZoom only on YouTube dataset. In general,
HCSumm preserves the node embeddings better than baselines and is consistent with the results
in the previous section.

6.4 Scalability

In this experiment, we evaluate the efficiency and scalability of our HCSumm method. We sample
graphs with different sizes ranging from 1,000 to 1 million the largest YouTube dataset and record
the running time of HCSumm method on these graphs. We represent the average running time
of 5 runs in Figure 5. It can be seen that the running time of HCSumm method is linear with the
graph size.

7 CONCLUSION

In this work, we study the connection between graph summarization and node embedding learning.
We reveal that three matrix-factorization-based node embeddings (DeepWalk, LINE, and NetMF)
of the original graph and the summary graph are closely related via a configuration-based recon-
structed graph. We analyze the upper bound of node embedding error and propose HCSumm to
summarize input graphs while preserving node embeddings. Extensive experiments on real-world
datasets show that HCSumm preserves the node embedding better than baselines. Overall, our
study helps understand the existing works of learning node embeddings via graph summarization
and provides theoretical insights for future works on this problem.

APPENDIX

A PROOFS
A.1 Proof of Theorem 1
Before we prove Theorem 1, we first introduce Lemmas 2 and 3.

Lemma 2.

−1
−1Q = D
s
where Q is the reconstruction matrix (Equation (7)), D and Ds are degree matrix of the original graph
and the summary graph.

Q

D

(cid:4)

,

Proof. The (p, q)th entry in Q(cid:4)D−1Q is

(cid:4)

Q

−1Q(p, q) =

D

(cid:2)

i

Q(i, p) 1
di

Q(i, q).

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:17

It is easy to see that the result is not zero only when p = q (since a node vi cannot belong to two
supernodes Sp and Sq simultaneously). And diagonal items are (note that d

(cid:3)

=

vi ∈Sp di ):

(s)
p

(cid:4)

Q

−1Q(p, p) =

D

(cid:2)

vi ∈Sp
(cid:2)

vi ∈Sp

=

Q(i, p) 1
di

Q(i, p) =

(cid:2)

vi ∈Sp

di
Dp

1
di

di
Dp

di
Dp

1
Dp

= 1
Dp

−1
= D
s

(p, p).

Lemma 3.

−1
RD
s

= D

−1Q.

Proof. Suppose vi ∈ Sk , then the (i, k)-th entry of RD−1
s

And the (i, k)th entry of D−c Q is

−1
RD
s

is
(i, k) = 1 · (Dk )−1 = 1
Dk

.

D

−1Q(i, k) = 1
di

di
Dk

= 1
Dk

.

Thus, RD−1
s

= D−1Q.

Now, we prove Theorem 1. Denote Kτ (G) =
Prove by induction. When τ = 1,

(cid:10)

(cid:9)

D−1Ar

τ D−1 for convenience.

K1(Gr ) = D
= RD
= R K1(Gs ) R
Suppose the lemma holds for τ = i, i.e., Ki (Gr ) = R Ki (Gs ) R(cid:4). For the case τ = i + 1,

−1 = D
(cid:4)
−1
s R
(cid:4).

−1Ar D
−1
s As D

−1QAs Q

(Lemma 3)

−1

D

(cid:4)

Ki+1(Gr ) = D
= D
5 = D

−1Ar Ki (Gr ) = D
−1QAs Q
−1QAs (Q

R Ki (Gs ) R
(cid:4)

D

(cid:4)

(cid:4)

−1Q)Ds Ki (Gs ) R

(cid:4)

−1Ar R Ki (Gs ) R

(cid:4)

(cid:2)

(21)

(cid:2)

(Lemmas 2 and 3)

= RD
= R Ki+1(Gs ) R
Applying principal of induction finishes the proof.

(cid:4).

−1
s As Ki (Gs ) R

(cid:4)

REFERENCES
[1] Bijaya Adhikari, Yao Zhang, Aditya Bharadwaj, and B. Aditya Prakash. 2017. Condensing temporal networks using

propagation. In Proceedings of the ICDM.

[2] Maham Anwar Beg, Muhammad Ahmad, Arif Zaman, and Imdadullah Khan. 2018. Scalable approximation algorithm

for graph summarization. In Proceedings of the PAKDD.

[3] Haochen Chen, Bryan Perozzi, Yifan Hu, and Steven Skiena. 2018. HARP: Hierarchical representation learning for

networks. In Proceedings of the AAAI.

[4] Graham Cormode and Shan Muthukrishnan. 2005. An improved data stream summary: The count-min sketch and its

applications. J. Algor. 55, 1 (2005), 58–75.

5D−c Q = RD−c
s

⇒ Q = Dc RD−c
s

⇒ QDc
s

= Dc R.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

145:18

H. Zhou et al.

[5] Chenhui Deng, Zhiqiang Zhao, Yongyu Wang, Zhiru Zhang, and Zhuo Feng. 2020. GraphZoom: A multi-level spectral

approach for accurate and scalable graph embedding. In Proceedings of the ICLR.

[6] P. Erdös and A. Rényi. 1959. On random graphs I. Publicationes Mathematicae Debrecen 6 (1959), 290.
[7] Matthew Fahrbach, Gramoz Goranci, Richard Peng, Sushant Sachdeva, and Chi Wang. 2020. Faster graph embeddings

via coarsening. In Proceedings of the ICML.

[8] Wenfei Fan, Jianzhong Li, Xin Wang, and Yinghui Wu. 2012. Query preserving graph compression. In Proceedings of

the ACM SIGMOD International Conference on Management of Data. 157–168.

[9] G. Fu, C. Hou, and X. Yao. 2019. Learning topological representation for networks via hierarchical sampling. In Pro-

ceedings of the IJCNN.

[10] Nathan Halko, Per-Gunnar Martinsson, and Joel A. Tropp. 2011. Finding structure with randomness: Probabilistic

algorithms for constructing approximate matrix decompositions. SIAM Rev. 53, 2 (2011), 217–288.

[11] Nasrin Hassanlou, Maryam Shoaran, and Alex Thomo. 2013. Probabilistic graph summarization. In Proceedings of the

WAIM.

[12] Paul W. Holland, Kathryn Blackmond Laskey, and Samuel Leinhardt. 1983. Stochastic blockmodels: First steps. Soc.

Netw. 5, 2 (1983), 109–137.

[13] Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019. Billion-scale similarity search with GPUs. IEEE Trans. Big Data

7, 3 (2019), 535–547.

[14] Brian Karrer and Mark E. J. Newman. 2011. Stochastic blockmodels and community structure in networks. Phys. Rev.

E 83, 1 (2011), 016107.

[15] George Karypis and Vipin Kumar. 1998. A fast and high quality multilevel scheme for partitioning irregular graphs.

SIAM J. Sci. Comput. (1998), 359392.

[16] Kifayat Ullah Khan, Waqas Nawaz, and Young-Koo Lee. 2017. Set-based unified approach for summarization of a

multi-attributed graph. In Proceedings of the WWW. 543–570.

[17] Jihoon Ko, Yunbum Kook, and Kijung Shin. 2020. Incremental lossless graph summarization. In Proceedings of the

KDD.

[18] Danai Koutra, U. Kang, Jilles Vreeken, and Christos Faloutsos. 2014. Vog: Summarizing and understanding large graphs.

In Proceedings of the SDM.

[19] Kyuhan Lee, Hyeonsoo Jo, Jihoon Ko, Sungsu Lim, and Kijung Shin. 2020. SSumM: Sparse summarization of massive

graphs. In Proceedings of the KDD.

[20] Kristen LeFevre and Evimaria Terzi. 2010. GraSS: Graph structure summarization. In Proceedings of the ICDM.
[21] Xiangfeng Li, Shenghua Liu, Zifeng Li, Xiaotian Han, Chuan Shi, Bryan Hooi, He Huang, and Xueqi Cheng. 2020.
Flowscope: Spotting money laundering based on graphs. In Proceedings of the AAAI Conference on Artificial Intelligence,
Vol. 34. 4731–4738.

[22] Jiongqian Liang, Saket Gurukar, and Srinivasan Parthasarathy. 2020. MILE: A multi-level framework for scalable graph

embedding. Retrieved from https://arXiv:1802.09612

[23] Yuzhi Liang, Yukun Wang, Kai Lei, Min Yang, Ziyu Lyu et al. 2020. Reachability preserving compression for dynamic

graph. Info. Sci. 520 (2020), 232–249.

[24] Wenqing Lin, Feng He, Faqiang Zhang, Xu Cheng, and Hongyun Cai. 2020. Initialization for network embedding: A

graph partition approach. In Proceedings of the WSDM.

[25] Yike Liu, Tara Safavi, Abhilash Dighe, and Danai Koutra. 2018. Graph summarization methods and applications: A

survey. Comput. Surveys 51, 3 (2018), 1–34.

[26] Hossein Maserrat and Jian Pei. 2010. Neighbor query friendly compression of social networks. In Proceedings of the

16th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining. 533–542.

[27] Arpit Merchant, Michael Mathioudakis, and Yanhao Wang. 2022. Graph summarization via node grouping: A spectral

algorithm. In Proceedings of the 16th ACM International Conference On Web Search And Data Mining.

[28] Saket Navlakha, Rajeev Rastogi, and Nisheeth Shrivastava. 2008. Graph summarization with bounded error. In Pro-

ceedings of the SIGMOD.

[29] Amin Emamzadeh Esmaeili Nejad, Mansoor Zolghadri Jahromi, and Mohammad Taheri. 2021. Graph compression

based on transitivity for neighborhood query. Info. Sci. 576 (2021), 312–328.

[30] Mark Newman. 2018. Networks. Oxford University Press.
[31] M. E. J. Newman. 2006. Modularity and community structure in networks. Proc. Natl. Acad. Sci. U.S.A. 103, 23 (2006),

8577–8582. https://doi.org/10.1073/pnas.0601602103

[32] Bryan Perozzi, Rami Al-Rfou, and Steven Skiena. 2014. DeepWalk: Online learning of social representations. In Pro-

ceedings of the KDD.

[33] Jiezhong Qiu, Yuxiao Dong, Hao Ma, Jian Li, Kuansan Wang, and Jie Tang. 2018. Network embedding as matrix

factorization: Unifying deepwalk, LINE, PTE, and node2vec. In Proceedings of the WSDM.

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

Node Embedding Preserving Graph Summarization

145:19

[34] Qiang Qu, Siyuan Liu, Christian S. Jensen, Feida Zhu, and Christos Faloutsos. 2014. Interestingness-driven diffusion

process summarization in dynamic networks. In Proceedings of the ECML-PKDD.

[35] Matteo Riondato, David García-Soriano, and Francesco Bonchi. 2017. Graph summarization with quality guarantees.

Data Min. Knowl. Discov. 31, 2 (2017), 314–349.

[36] Amin Sadri, Flora D Salim, Yongli Ren, Masoomeh Zameni, Jeffrey Chan, and Timos Sellis. 2017. Shrink: Distance

preserving graph compression. Info. Syst. 69 (2017), 180–193.

[37] Neil Shah, Danai Koutra, Tianmin Zou, Brian Gallagher, and Christos Faloutsos. 2015. Timecrunch: Interpretable

dynamic graph summarization. In Proceedings of the KDD.

[38] Hua-Wei Shen, Xue-Qi Cheng, and Jia-Feng Guo. 2011. Exploring the structural regularities in networks. Phys. Rev. E

84, 5 (2011), 056111.

[39] Kijung Shin, Amol Ghoting, Myunghwan Kim, and Hema Raghavan. 2019. Sweg: Lossless and lossy summarization

of web-scale graphs. In Proceedings of the WWW.

[40] Jian Tang, Meng Qu, Mingzhe Wang, Ming Zhang, Jun Yan, and Qiaozhu Mei. 2015. LINE: Large-scale information

network embedding. In Proceedings of the WWW.

[41] Nan Tang, Qing Chen, and Prasenjit Mitra. 2016. Graph stream summarization: From big bang to big crunch. In

Proceedings of the SIGMOD.

[42] Ye Wu, Zhinong Zhong, Wei Xiong, and Ning Jing. 2014. Graph summarization for attributed graphs. In Proceedings

of the ICIEE.

[43] Yujun Yan, Jiong Zhu, Marlena Duda, Eric Solarz, Chandra Sripada, and Danai Koutra. 2019. GroupINN: Grouping-
based interpretable neural network-based classification of limited, noisy brain data. In Proceedings of the KDD.
[44] Quinton Yong, Mahdi Hajiabadi, Venkatesh Srinivasan, and Alex Thomo. 2021. Efficient graph summarization using
weighted lsh at billion-scale. In Proceedings of the International Conference on Management of Data. 2357–2365.
[45] Houquan Zhou, Shenghua Liu, Kyuhan Lee, Kijung Shin, Huawei Shen, and Xueqi Cheng. 2021. DPGS:

Degree-preserving graph summarization. In Proceedings of the SDM (2021).

Received 16 April 2023; revised 22 September 2023; accepted 29 January 2024

ACM Trans. Knowl. Discov. Data., Vol. 18, No. 6, Article 145. Publication date: April 2024.

