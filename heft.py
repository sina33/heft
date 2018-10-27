from example import dag, commcost, compcost
import statistics as stats
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.DEBUG)


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
        self.rank = None
        self.comp_cost = []
        self.avg_comp = None
        self.successors = []
        self.predecessors = []

    def __str__(self):
        return str(" TASK id: {}, succ: {}, pred: {}, avg_comp: {}, rank: {}".format(
            self.id, self.successors, self.predecessors, self.avg_comp, self.rank
        ))


class Processor:
    def __init__(self, num):
        self.id = num
        self.tasks = []
        self.avail = 0      # processor ready time in a non-insertion based scheduling policy



def ranku(i, tasks):
    """Calculate Upward Rank of a node
    
    Arguments:
        i {int} -- task id
        tasks {list} -- list of Tasks
    """
    
    seq = [commcost(i, j,'a', 'b') + ranku(j, tasks) for j in tasks[i].successors]
    logging.debug('%s - seq: %s', i, seq)
    if i==0:
        return 9999
    if seq == []:
        return tasks[i].avg_comp
    return tasks[i].avg_comp + max(seq)


def est(i, p, tasks, processors):
    """Calculate Earliest execution Start Time Task i on Processor p
    
    Arguments:
        i {int} -- task id
        p {int} -- processor id
        tasks {list} -- list of Tasks
"""
    if i==0:        # entry task
        return 0
    seq = [tasks[m].aft + commcost(m, i, 'a', 'b') for m in tasks[i].predecessors]
    ready_time = max(seq)
    next((x for x in processors if x.id == p), None)
    logging.debug('est: %s', max([ready_time, processors[p].avail]))
    return max([ready_time, processors[p].avail])


def eft(i, p, tasks, processors):
    logging.debug('eft: %s, %s = %s', i, p, compcost(i, chr(97+p)))
    return compcost(i, chr(97+p)) + est(i, p, tasks, processors)


def makespan(tasks):
    seq = [t.aft for t in tasks]
    return max(seq)


if __name__ == "__main__":
    # Create Processors
    P = 3
    processors = [Processor(i) for i in range(P)]
    # Create Tasks
    N = 10
    tasks = [Task(i) for i in range(N+1)]
    for t, succ in dag.items():
        tasks[t].successors = [x for x in succ]
        tasks[t].comp_cost = [compcost(t, p) for p in 'ab']
        tasks[t].avg_comp = stats.mean(tasks[t].comp_cost)        
        for x in succ:
            tasks[x].predecessors.append(t)
        # setup entry task (id=0)
        tasks[0].avg_comp = 0
        tasks[0].successors = [1]
        tasks[1].predecessors = [0]

    # Calculate Ranks by traversing task graph upward
    for task in reversed(tasks):
        task.rank = ranku(task.id, tasks)
            
    # return a new sorted list, use the sorted() built-in function
    priority_list = sorted(tasks, key=lambda x: x.rank, reverse=True)

    for task in priority_list:
        logging.info(task)

    tasks[0].ast = 0
    tasks[0].aft = 0
    for task in priority_list:
        seq = [eft(task.id, p.id, tasks, processors) for p in processors]
        p = seq.index(min(seq))
        processors[p].tasks.append(task)
        task.ast = est(task.id, p, tasks, processors)
        task.aft = eft(task.id, p, tasks, processors)

    for p in processors:
        logging.info('task on processor %s: %s', p.id, [t.id for t in p.tasks])

    logging.info('makespan: %s', makespan(tasks))