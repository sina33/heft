from example import dag, commcost, compcost
import statistics as stats
from decimal import Decimal, ROUND_DOWN
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO)


# Set the computation costs of tasks and communication costs of edges with mean values.
# Compute rank_u for all tasks by traversing graph upward, starting from the exit task.
# Sort the tasks in a scheduling list by nonincreasing order of rank_u values.


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
    assign(task.id, p, tasks, processors)



if __name__ == "__main__":
    # Create Processors
    P = 3
    processors = [Processor(i) for i in range(P)]
    # Create Tasks
    N = len(dag)
    tasks = [Task(i) for i in range(N+1)]
    for t, succ in dag.items():
        tasks[t].successors = [x for x in succ]
        agents = ''.join([chr(97+i) for i in range(P)]) # e.g., 'abc'
        tasks[t].comp_cost = [compcost(t, p) for p in agents]
        tasks[t].avg_comp_cost = stats.mean(tasks[t].comp_cost)   
        for x in succ:
            tasks[x].predecessors.append(t)
        # setup entry task (id=0)
        tasks[0].avg_comp_cost = 0
        tasks[0].successors = [1]
        tasks[1].predecessors = [0]

    # Calculate ranku by traversing task graph upward
    for task in reversed(tasks):
        task.ranku = round(ranku(task.id, tasks), 3)
    
    # Calculate Rankd by traversing task graph upward
    for task in tasks:
        task.rankd = round(rankd(task.id, tasks), 3)
    
    # return a new sorted list, use the sorted() built-in function
    priority_list = sorted(tasks, key=lambda x: x.ranku, reverse=True)
    # priority_list = sorted(tasks, key=lambda x: x.rankd)

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
        logging.info('tasks on processor %s: %s', p.id, [{t.id: (t.ast, t.aft)} for t in p.tasks])

    logging.info('makespan: %s', makespan(tasks))