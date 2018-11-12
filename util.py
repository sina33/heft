import itertools


def reverse_dict(d):
    """ Reverses direction of dependence dict

    >>> d = {'a': (1, 2), 'b': (2, 3), 'c':()}
    >>> reverse_dict(d)
    {1: ('a',), 2: ('a', 'b'), 3: ('b',)}
    """
    result = {}
    for key in d:
        result[key] = result.get(key, tuple())
        for val in d[key]:
            result[val] = result.get(val, tuple()) + (key, )
    return result

def find_job_event(job_name, orders_dict):
    for event in itertools.chain.from_iterable(orders_dict.values()):
        if event.job == job_name:
            return event


def stg_to_dag(filename = 'sparse'):
    import numpy as np
    no_tasks = 334
    with open(filename, 'r') as f:
        line = f.readline() # no_tasks
        no_tasks = int(line)
    dag = dict()
    _compcost = np.zeros(no_tasks+1, dtype=int)
    _commcost = np.zeros((no_tasks, no_tasks), dtype=int)


    with open(filename, 'r') as f:
        _ = f.readline() # no_tasks
        cnt = 0
        line = f.readline()
        # while line:
        while cnt < no_tasks:
            task, exec_time, deps_size, *deps = map(int, line.split())
            _compcost[task] = exec_time
            dag[task] = dag.get(task, ())
            if len(deps) != deps_size and task != 0:
                raise ValueError("Number of dependencies doesn't match with len(deps)! {} - {} {}".format(task, deps_size, deps))
            for d in deps:
                dag[d] = dag.get(d, ()) + (task,)
            line = f.readline()
            cnt+=1 
    return dag, _compcost


def dag_to_stg(dag, compcost, filename='tmp.stg'):
    N = len(dag)
    rdag = reverse_dict(dag)
    print('reversed dag : %s' % rdag)
    print('reversed dag sorted: %s' % sorted(rdag.items(), key=lambda x: x[0]))
    # print()
    with open(filename, 'w+') as f:
        f.write("%d \n" % N)
        f.write("0 0 0 \n")
        for k, v in sorted(rdag.items(), key=lambda x: x[0]):
            f.write("%d %d " % (k, compcost(k, 'a')))
            if v:
                f.write("%d " % len(v))
                for d in v:
                    f.write("%d " % d)
            else:
                f.write('0 ')
            f.write("\n")
        
