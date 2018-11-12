# Create STG from dag

from util import dag_to_stg, stg_to_dag, reverse_dict
from stg.fft import dag, compcost


# print(dag)
dag_to_stg(dag, compcost, filename='fft.stg')
d, c = stg_to_dag(filename='fft.stg')
# print(d)

from stg.laplace import dag, compcost

# print(dag)
dag_to_stg(dag, compcost, filename='laplace.stg')
d, c = stg_to_dag(filename='laplace.stg')
# print(d)

from stg.gaussian_elimination import dag, compcost

# print(dag)
dag_to_stg(dag, compcost, filename='gaussian_elimination.stg')
d, c = stg_to_dag(filename='gaussian_elimination.stg')
# print(d)