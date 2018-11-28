from stg.laplace import dag, commcost, compcost
from util import stg_to_dag
import statistics as stats
from queue import PriorityQueue
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


### Configs
task_graph = 'fpppp' # 'sparse' or 'fpppp' or 'robot' or uncomment a line from below
# from stg.fft import dag, commcost, compcost
# from stg.laplace import dag, commcost, compcost
# from stg.gaussian_elimination import dag, commcost, compcost
log_to_file = True
log_level = logging.INFO
###


if log_to_file:
    log_filename = 'logs/cpop/' + task_graph + '.log'
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

# for running stg task graphs
if task_graph in stgs:
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
        self.priority = None
        self.comp_cost = []
        self.avg_comp_cost = None
        self.successors = []
        self.predecessors = []

    def __str__(self):
        return str(" TASK id: {}, succ: {}, pred: {}, ranku: {}, rankd: {}, processor: {}".format(
            self.id, self.successors, self.predecessors, self.ranku, self.rankd, self.processor
        ))

    ### turns Task to unhashable type
    # def __eq__(self, other):
    #     if other.priority == self.priority:
    #         return True
    #     else:
    #         return False

    def __lt__(self, other):
        return self.priority < other.priority



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
    seq = [commcost(i, j,'a', 'b') + ranku(j, tasks) for j in tasks[i].successors]
    logging.debug('%s - seq: %s', i, seq)
    if i==0:
        return 9999
    if seq == []:
        return tasks[i].avg_comp_cost
    return tasks[i].avg_comp_cost + max(seq)


def rankd(i, tasks):
    """Calculate Downward Rank of a task
    
    Arguments:
        i {int} -- task id
        tasks {list} -- list of Tasks
    """
    if i==0:        # entry task
        return 0
    seq = [(rankd(j, tasks) + tasks[j].avg_comp_cost + commcost(j, i, 'a', 'b')) for j in tasks[i].predecessors]
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
    seq = [tasks[m].aft + commcost(m, i, tasks[m].processor, p) + commcost(i, m, tasks[m].processor, p) for m in tasks[i].predecessors]
    # logging.debug('est() ready_times for task %s on processor %s : %s', i, p, seq)
    ready_time = max(seq)
    res = max([ready_time, processors[p].avail])
    # logging.debug('est(%s, %s): %s', i, p, res)
    return res

def eft(i, p, tasks, processors):
    """Calculate Earliest execution Finish Time for task i on processor p
    
    Arguments:
        i {int} -- task id
        p {int} -- processor id
        tasks {list} -- list of Tasks
        processors {list} -- list of Processors
    """
    res = compcost(i, chr(97+p)) + est(i, p, tasks, processors)
    # logging.debug('eft(%s, %s) = %s', i, p, res)
    return res


def makespan(tasks):
    seq = [t.aft for t in tasks]
    # logging.debug(seq)
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




if __name__ == "__main__":
    # Create Processors
    P = 4
    processors = [Processor(i) for i in range(P)]
    # Create Tasks
    N = len(dag) if task_graph in stgs else len(dag) + 1
    tasks = [Task(i) for i in range(N)]
    for t, succ in dag.items():
        tasks[t].successors = [x for x in succ]
        agents = ''.join([chr(97+i) for i in range(P)]) # e.g., 'abc'
        tasks[t].comp_cost = [compcost(t, p) for p in agents]
        tasks[t].avg_comp_cost = stats.mean(tasks[t].comp_cost)   
        for x in succ:
            tasks[x].predecessors.append(t)
        # setup entry task (id=0)
        tasks[0].avg_comp_cost = 0
        if task_graph not in stgs:
            tasks[0].successors = [1]
            tasks[1].predecessors = [0]

    # Calculate ranku by traversing task graph upward
    for task in reversed(tasks):
        task.ranku = round(ranku(task.id, tasks), 3)
    
    # Calculate Rankd by traversing task graph upward
    for task in tasks:
        task.rankd = round(rankd(task.id, tasks), 3)
        
    
    # Calculate Priority
    for task in tasks:
        task.priority = task.rankd + task.ranku

    _cp_ = tasks[1].priority
    CP = {tasks[1],}
    # Construct Critical-Path (CP)
    selected = tasks[1]
    while selected.id != N-1:
        pr = [tasks[t].priority for t in selected.successors]
        i = pr.index(max(pr))
        CP.add(tasks[selected.successors[i]])
        selected = tasks[selected.successors[i]]
        logging.info('CP: %s', [t.id for t in CP])
    
    # Select the CP-Processor
    pcp = [0] * P
    for t in CP:
        for p in range(P):
            pcp[p] += compcost(t.id, chr(97+p))
    cp_processor = pcp.index(min(pcp))
    logging.info('CP-Processor is %s', cp_processor)

    # Initialize Priority Queue
    tasks[0].ast = 0
    tasks[0].aft = 0
    q = PriorityQueue()
    q.put((-tasks[0].priority, tasks[0]))
    order = []
    while not q.empty():
        task = q.get()[1]
        order.append(task.id)
        logging.debug('task from q: %s', task)
        if task in CP:
            # Assign the task to the CP-Processor
            assign(task.id, cp_processor, tasks, processors)
        else:
            seq = [eft(task.id, p, tasks, processors) for p in range(P)]
            p = seq.index(min(seq))
            assign(task.id, p, tasks, processors)
        # Update the Priority Queue with successors of task if they become ready tasks
        for s in task.successors:
            if None not in [(tasks[p].processor) for p in tasks[s].predecessors]:
                q.put((-tasks[s].priority, tasks[s]))

    logging.info('task scheduling order: %s', order)
    logging.info('-'*7 + ' Tasks ' + '-'*7 )
    for task in tasks:
        logging.info(task)
    logging.info('-'*20)


    for p in processors:
        logging.info('tasks on processor %s: %s', p.id, {t.id: (t.ast, t.aft) for t in p.tasks})

    logging.info('makespan: %s', makespan(tasks))