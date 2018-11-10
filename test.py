from util import dag_to_stg, stg_to_dag, reverse_dict
from stg.fft import dag, compcost

print(dag)
dag_to_stg(dag, compcost)
stg_to_dag(filename='tmp.stg')