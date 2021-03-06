# from stg.fft import dag, commcost, compcost
from util import stg_to_dag
import statistics as stats
from decimal import Decimal, ROUND_DOWN
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


### Configs
alg = 'heft-t' # 'heft-t' (ranku) or 'heft-b' (rankd)
task_graph = 'rand0002-100.stg' # 'sparse' or 'fpppp' or 'robot' or uncomment a line from below
stg_flag = True
# from stg.fft import dag, commcost, compcost
# from stg.laplace import dag, commcost, compcost
# from stg.gaussian_elimination import dag, commcost, compcost
log_to_file = False
log_level = logging.INFO
###


if log_to_file:
    log_filename = 'logs/' + alg + '/' + task_graph + '.log'
    logging.basicConfig(level=log_level, filename=log_filename) # filename='sparse.log'
else:
    logging.basicConfig(level=log_level)

# Set the computation costs of tasks and communication costs of edges with mean values.
# Compute rank_u for all tasks by traversing graph upward, starting from the exit task.
# Sort the tasks in a scheduling list by nonincreasing order of rank_u values.

global compcost
global commcost
global dag
stgs = ['sparse', 'robot', 'fpppp']
rankuDict = {}
rankdDict = {}
stgs.append(task_graph)

# for running stg task graphs
if stg_flag:
    low_perf_multiplier = 2
    dag, _compcost = stg_to_dag('stg/' + task_graph)

    def comm(a, b, A, B):
        return 0

    def comp(job, agent):
        if agent == 'a' or agent == 'b':
            return _compcost[job] * low_perf_multiplier
        else: 
            return _compcost[job]

    compcost = comp
    commcost = comm
else:
    pass



class Task:
    def __init__(self, num):
        self.id = num
        self.processor = None
        self.ast = None     # Actual Start Time
        self.aft = None     # Actual Finish Time
        self.est = []       # Earliest execution Start Time
        self.eft = []       # Earliest execution Finish Time
        self.ranku = None
        self.rankd = None
        self.comp_cost = []
        self.avg_comp_cost = None
        self.successors = []
        self.predecessors = []

    def __str__(self):
        return str(" TASK id: {}, succ: {}, pred: {}, avg_comp_cost: {}, ranku: {}, rankd: {}".format(
            self.id, self.successors, self.predecessors, self.avg_comp_cost, self.ranku, self.rankd
        ))


class Processor:
    def __init__(self, num):
        self.id = num
        self.tasks = []
        self.avail = 0      # processor ready time in a non-insertion based scheduling policy
    



def ranku(i, tasks):
    """Calculate Upward Rank of a task
    
    Arguments:
        i {int} -- task id
        tasks {list} -- list of Tasks
    """ 
    global rankuDict
    if i in rankuDict:
        return rankuDict[i]

    seq = [commcost(i, j,'a', 'b') + ranku(j, tasks) for j in tasks[i].successors]
    logging.debug('ranku[%s] - seq: %s', i, seq)
    if i==0:    # Entry Task
        rankuDict[0] = 9999
        return 9999
    if seq == []:
        rankuDict[i] = tasks[i].avg_comp_cost 
        return tasks[i].avg_comp_cost
    rankuDict[i] = tasks[i].avg_comp_cost + max(seq)
    return tasks[i].avg_comp_cost + max(seq)


def rankd(i, tasks):
    """Calculate Downward Rank of a task
    
    Arguments:
        i {int} -- task id
        tasks {list} -- list of Tasks
    """
    global rankdDict
    if i in rankdDict:
        return rankdDict[i]
    if i==0:        # entry task
        rankdDict[0] = 0
        return 0
    logging.debug('rankd(%s)', i)
    seq = [(rankd(j, tasks) + tasks[j].avg_comp_cost + commcost(j, i, 'a', 'b')) for j in tasks[i].predecessors]
    rankdDict[i] = max(seq)
    return max(seq)


def est(i, p, tasks, processors):
    """Calculate Earliest execution Start Time Task i on Processor p
    
    Arguments:
        i {int} -- task id
        p {int} -- processor id
        tasks {list} -- list of Tasks
        processors {list} -- list of Processors
    """
    if i==0:        # entry task
        return 0
    for m in tasks[i].predecessors:
        if tasks[m].aft is None:
            schedule(tasks[m], tasks, processors)
            # print('tasks[%s].aft: %s' % (m, tasks[m].aft))
    seq = [tasks[m].aft + commcost(m, i, tasks[m].processor, p) for m in tasks[i].predecessors]
    logging.debug('est ready_times for task %s on different cores: %s', i, seq)
    ready_time = max(seq)
    logging.debug('est(%s, %s): %s', i, p, max([ready_time, processors[p].avail]))
    return max([ready_time, processors[p].avail])


def eft(i, p, tasks, processors):
    """Calculate Earliest execution Finish Time for task i on processor p
    
    Arguments:
        i {int} -- task id
        p {int} -- processor id
        tasks {list} -- list of Tasks
        processors {list} -- list of Processors
    """
    logging.debug('eft: %s, %s = %s', i, p, compcost(i, chr(97+p)))
    return compcost(i, chr(97+p)) + est(i, p, tasks, processors)


def makespan(tasks):
    seq = [t.aft for t in tasks]
    logging.debug('aft: %s', seq)
    return max(seq)


def assign(i, p, tasks, processors):
    """Assign task to processor
    
    Arguments:
        i {int} -- task id
        p {int} -- processor id
        tasks {list} -- list of tasks
        processors {list} -- list of processors
    """
    processors[p].tasks.append(tasks[i])
    tasks[i].processor = p
    tasks[i].ast = est(tasks[i].id, p, tasks, processors)
    tasks[i].aft = eft(tasks[i].id, p, tasks, processors)
    processors[p].avail = tasks[i].aft


def schedule(task, tasks, processors):
    seq = [eft(task.id, p.id, tasks, processors) for p in processors]
    p = seq.index(min(seq))
    if task.processor is None:
        assign(task.id, p, tasks, processors)



if __name__ == "__main__":
    # Create Processors
    P = 4
    processors = [Processor(i) for i in range(P)]
    # Create Tasks
    N = len(dag) - 1 if stg_flag else len(dag) - 1
    tasks = [Task(i) for i in range(N+1)] # N+1 for non-stg
    for t, succ in dag.items():
        tasks[t].successors = [x for x in succ]
        agents = ''.join([chr(97+i) for i in range(P)]) # e.g., 'abc'
        tasks[t].comp_cost = [compcost(t, p) for p in agents]
        tasks[t].avg_comp_cost = stats.mean(tasks[t].comp_cost)   
        for x in succ:
            tasks[x].predecessors.append(t)
        # setup entry task (id=0)
        tasks[0].avg_comp_cost = 0
        # if task_graph not in stgs:
        #     tasks[0].successors = [1]
        #     tasks[1].predecessors = [0]
        

    logging.info('-'*7 + ' Tasks ' + '-'*7 )
    for task in tasks:
        logging.info(task)
    logging.info('-'*20)

    # Calculate ranku by traversing task graph upward
    for task in reversed(tasks):
        task.ranku = round(ranku(task.id, tasks), 3)
    
    # Calculate Rankd by traversing task graph upward
    for task in tasks:
        task.rankd = round(rankd(task.id, tasks), 3)
    
    # return a new sorted list, use the sorted() built-in function
    priority_list = list()
    if alg == 'heft-t':
        priority_list = sorted(tasks, key=lambda x: x.ranku, reverse=True)
    elif alg == 'heft-b':
        priority_list = sorted(tasks, key=lambda x: x.rankd, reverse=True)


    logging.info('-'*7 + ' Tasks ' + '-'*7 )
    for task in tasks:
        logging.info(task)
    logging.info('-'*20)
    logging.info('task scheduling order: %s', [t.id for t in priority_list])

    tasks[0].ast = 0
    tasks[0].aft = 0
    for task in priority_list:
        schedule(task, tasks, processors)
        


    for p in processors:
        logging.info('tasks on processor %s: %s', p.id, {t.id: (t.ast, t.aft) for t in p.tasks})

    logging.info('makespan: %s', makespan(tasks))