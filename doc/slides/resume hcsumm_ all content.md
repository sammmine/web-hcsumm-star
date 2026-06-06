<!-- Slide number: 1 -->
# Introduction: Software Evolution Problem

Software systems grow over time
Call graphs become large and complex
Developers lose the big-picture understanding

### Notes:

<!-- Slide number: 2 -->
# Problem Formulation

Input: Directed Call Graph (CG)
Goal: Summarize into cluster-based graph
Preserve structure while simplifying complexity

### Notes:

<!-- Slide number: 3 -->
# Existing Approach: HCSumm

Adjacency → Normalization → Spectral Embedding → Clustering
Graph becomes undirected
Execution flow information is lost

### Notes:

<!-- Slide number: 4 -->
# Research Gap

Execution paths are ignored
Directionality is removed (?)
Behavioral information is missing

### Notes:

<!-- Slide number: 5 -->
# Proposed Idea

Combine structural + execution information
Use dual representation for each node

### Notes:

<!-- Slide number: 6 -->
# Proposed Method (Structure + Behavior)
Embedding 🡪 node2vec
Generate e(v)
Normalize → e’(v)
AHC🡪 Ward + Euclidean dist
Source Code
Call Graph
x(v) = [αe’(v) || βfe’(v)]
Summary Graph
Path Extraction
Normalize → f’(v)
Generate f(v)

### Notes:

<!-- Slide number: 7 -->
# What is Dual Representation

e(v): structural embedding (node2vec)
f(v): execution path features
Both capture complementary information

### Notes:

<!-- Slide number: 8 -->
# Feature Fusion

x(v) = [ e'(v) || f'(v) ]
Combine normalized embeddings
Balanced contribution of both features

### Notes:

<!-- Slide number: 9 -->
# Why Normalization?

Avoid dominance of one feature
Ensure fair contribution
Stabilize distance computation

### Notes:

<!-- Slide number: 10 -->
# Distance Computation

Euclidean distance on x(v)
Captures both structure and execution similarity

### Notes:

<!-- Slide number: 11 -->
# Clustering Method

Ward linkage
Minimize intra-cluster variance
Uses Euclidean distance

### Notes:

<!-- Slide number: 12 -->
# Running the Experiment
Goals:
(G01) To verify that the proposed method work as expected.
(G02) To ensure that adding behavioral features can improve the clustering result.

### Notes:

<!-- Slide number: 13 -->
# Running the Experiment (2)
Scenarios:
Dry run test 🡪 G01
Scenario based with synthetic data 🡪 G01
Comparison between HCSumm vs Proposed method without f(v) vs Proposed method with f(v) 🡪 G02 🡪 pendekatan yg ada arahnya vs tidak ada arahnya
Using real-world case*

### Notes:

<!-- Slide number: 14 -->
# Dry Run Test
Step-by-step mathematical verification

Graph @ t0
A
B
C
D
Edges: A→B, A→C, C→D

Graph @ t1
A
B
D
C
E
Edges: A→B, A→C, C→D, C→E

### Notes:

<!-- Slide number: 15 -->
# Assumptions

Important note: f(v) is computed exactly from the directed call graph, while e(v) uses a proxy node2vec-style embedding so the dry run can be performed manually.
Rules: graph is directed; execution path is simple; path must end at an exit node; trivial path is not allowed; path length is counted in number of edges.

### Notes:

<!-- Slide number: 16 -->
# t0 - Graph and valid execution paths

Directed call graph t0: A→B, A→C, C→D
Exit nodes: B and D
Valid execution paths:
P1 = A→B (length 1)
P2 = A→C→D (length 2)
P3 = C→D (length 1)
Maximum path length L = 2

### Notes:

<!-- Slide number: 17 -->
# t0 - Raw path feature and normalization

Raw feature definition and normalized feature:

![eq_fdef.png](GoogleShape228p17.jpg)

![eq_fnorm.png](GoogleShape229p17.jpg)

![t0_raw_text.png](GoogleShape230p17.jpg)

![t0_norm_text.png](GoogleShape231p17.jpg)

### Notes:

<!-- Slide number: 18 -->
# t0 - Proxy node2vec embedding and normalization

Proxy embedding used for dry run:
e(A)=[1.0, 0.0]
e(B)=[0.8, 0.2]
e(C)=[0.2, 0.8]
e(D)=[0.0, 1.0]
normalized embeddings:

![t0_enorm_text.png](GoogleShape239p18.jpg)

![eq_enorm.png](GoogleShape238p18.jpg)

### Notes:

<!-- Slide number: 19 -->
t0 - L2 normalization of e(v)
Normalization rule:
e~(v) = e(v) / ||e(v)||

For A:
e(A) = [1, 0]
||e(A)|| = sqrt(1^2 + 0^2) = sqrt(1) = 1
e~(A) = [1/1, 0/1] = [1, 0]

For B:
e(B) = [0.8, 0.2]
||e(B)|| = sqrt(0.8^2 + 0.2^2)
        = sqrt(0.64 + 0.04)
        = sqrt(0.68)
        ≈ 0.825
e~(B) = [0.8/0.825, 0.2/0.825]
      ≈ [0.970, 0.243]

For C:
e(C) = [0.2, 0.8]
||e(C)|| = sqrt(0.2^2 + 0.8^2)
        = sqrt(0.04 + 0.64)
        = sqrt(0.68)
        ≈ 0.825
e~(C) = [0.2/0.825, 0.8/0.825]
      ≈ [0.243, 0.970]

For D:
e(D) = [0, 1]
||e(D)|| = sqrt(0^2 + 1^2) = 1
e~(D) = [0, 1]

### Notes:

<!-- Slide number: 20 -->
# t0 - Fusion x(v)

Fusion with α = 1 and β = 1

![eq_fusion.png](GoogleShape252p20.jpg)

![t0_fusion_text.png](GoogleShape253p20.jpg)

### Notes:

<!-- Slide number: 21 -->
# t0 - Euclidean distances

Distance equation and full matrix:

![eq_dist.png](GoogleShape260p21.jpg)

![t0_distmat.png](GoogleShape261p21.jpg)

![t0_distmat.png](GoogleShape262p21.jpg)

### Notes:

<!-- Slide number: 22 -->
#

t0 - Full step-by-step distance calculations
d(A,B)=sqrt((1-0.970)^2 + (0-0.243)^2 + (0.5-1)^2 + (0.5-0)^2)=sqrt(0.5599)≈0.748
d(A,C)=sqrt((1-0.243)^2 + (0-0.970)^2)=sqrt(1.514)≈1.230
d(A,D)=sqrt((1-0)^2 + (0-1)^2)=sqrt(2)≈1.414
d(B,C)=sqrt((0.727)^2 + (-0.727)^2 + (0.5)^2 + (-0.5)^2)=sqrt(1.556)≈1.247
d(B,D)=sqrt((0.970)^2 + (-0.757)^2 + (0.5)^2 + (-0.5)^2)=sqrt(2.014)≈1.419
d(C,D)=sqrt((0.243)^2 + (-0.030)^2)=sqrt(0.0599)≈0.245

### Notes:

<!-- Slide number: 23 -->
# t0 - Ward linkage

Smallest pairwise distance is C-D, so that merge happens first.
Then A-B merges.
Finally {A,B} and {C,D} are merged at the highest Ward cost.

### Notes:

<!-- Slide number: 24 -->
# t0 - Summary graph

Cut at 2 clusters:
Cluster 1 = {A,B}
Cluster 2 = {C,D}
Summary graph: {A,B} → {C,D}

![t0_dendrogram.png](GoogleShape281p24.jpg)

### Notes:

<!-- Slide number: 25 -->
# t1 - Graph and valid execution paths

Directed call graph t1: A→B, A→C, C→D, C→E
Exit nodes: B, D, E
Valid execution paths:
P1 = A→B (1)
P2 = A→C→D (2)
P3 = A→C→E (2)
P4 = C→D (1)
P5 = C→E (1)
Maximum path length L = 2

### Notes:

<!-- Slide number: 26 -->
# t1 - Raw path feature and normalization

Raw feature definition and normalized feature:

![eq_fdef.png](GoogleShape294p26.jpg)

![eq_fnorm.png](GoogleShape296p26.jpg)

![t1_raw_text.png](GoogleShape295p26.jpg)

![t1_norm_text.png](GoogleShape297p26.jpg)

### Notes:

<!-- Slide number: 27 -->
# t1 - Proxy node2vec-style embedding and normalization

Proxy embedding used for dry run:
e(A)=[1.0, 0.0]
e(B)=[0.8, 0.2]
e(C)=[0.2, 0.8]
e(D)=[0.0, 1.0]
e(E)=[0.0, 1.0]
normalized embeddings:

![t1_enorm_text.png](GoogleShape304p27.jpg)

![eq_enorm.png](GoogleShape305p27.jpg)

### Notes:

<!-- Slide number: 28 -->
t1 - L2 normalization of e(v)
Normalization rule:
e~(v) = e(v) / ||e(v)||

For A:
e~(A) = [1, 0]

For B:
||e(B)|| = sqrt(0.8^2 + 0.2^2)
        = sqrt(0.64 + 0.04)
        = sqrt(0.68)
        ≈ 0.825
e~(B) = [0.8/0.825, 0.2/0.825]
      ≈ [0.970, 0.243]

For C:
||e(C)|| = sqrt(0.2^2 + 0.8^2)
        = sqrt(0.68)
        ≈ 0.825
e~(C) = [0.2/0.825, 0.8/0.825]
      ≈ [0.243, 0.970]

For D:
e~(D) = [0, 1]

For E:
e~(E) = [0, 1]

### Notes:

<!-- Slide number: 29 -->
# t1 - Fusion x(v)

Fusion with α = 1 and β = 1

![eq_fusion.png](GoogleShape318p29.jpg)

![t1_fusion_text.png](GoogleShape319p29.jpg)

### Notes:

<!-- Slide number: 30 -->
# t1 - Euclidean distances

Distance equation and full matrix:

![eq_dist.png](GoogleShape326p30.jpg)

![t1_distmat.png](GoogleShape328p30.jpg)

![t1_distmat.png](GoogleShape327p30.jpg)

### Notes:

<!-- Slide number: 31 -->
# t1 - Full step-by-step distance calculations
d(A,B)=sqrt((1-0.970)^2 + (0-0.243)^2 + (0.333-1)^2 + (0.667-0)^2)=sqrt(0.9497)≈0.975
d(A,C)=sqrt((0.757)^2 + (-0.970)^2 + (-0.167)^2 + (0.167)^2)=sqrt(1.570)≈1.253
d(A,D)=sqrt(1 + 1 + 0.028 + 0.028)=sqrt(2.056)≈1.434
d(A,E)=d(A,D)=1.434
d(B,C)=sqrt((0.727)^2 + (-0.727)^2 + 0.5^2 + (-0.5)^2)=sqrt(1.556)≈1.247
d(B,D)=sqrt((0.970)^2 + (-0.757)^2 + 0.5^2 + (-0.5)^2)=sqrt(2.014)≈1.419
d(B,E)=d(B,D)=1.419
d(C,D)=sqrt((0.243)^2 + (-0.030)^2)=sqrt(0.0599)≈0.245
d(C,E)=d(C,D)=0.245
d(D,E)=0

### Notes:

<!-- Slide number: 32 -->
# t1 - Ward linkage

Smallest pairwise distance is D-E = 0, so that merge happens first.
Then C merges into {D,E}.
Then A-B merge.
Finally {A,B} and {C,D,E} are merged at the highest Ward cost.

### Notes:

<!-- Slide number: 33 -->
# t1 - Summary graph

Cut at 2 clusters:
Cluster 1 = {A,B}
Cluster 2 = {C,D,E}
Summary graph: {A,B} → {C,D,E}

![t1_dendrogram.png](GoogleShape347p33.jpg)

### Notes: