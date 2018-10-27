from example import dag, commcost, compcost
import statistics as stats
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.DEBUG)


class Task:
    def __init__(self, num):
        self.id = num
        self.processor = None
        self.ast = None     # Actual Start Time
        self.aft = None     # Actual Finish Time
        self.rank = None
        self.comp_cost = []
        self.avg_comp = None
        self.successors = []
        self.predecessor = None

    def __str__(self):
        return str(" TASK id: {}, succ: {}, pred: {}, avg_comp: {}, rank: {}".format(
            self.id, self.successors, self.predecessor, self.avg_comp, self.rank
        ))


class Processor:
    def __init__(self, num):
        self.id = num
        self.tasks = []


def ranku(i, tasks):
    seq = [commcost(i, j,'a', 'b') + ranku(j, tasks) for j in tasks[i].successors]
    logging.debug('%s - seq: %s', i, seq)
    if i==0:
        return 9999
    if seq == []:
        return tasks[i].avg_comp
    return tasks[i].avg_comp + max(seq)


if __name__ == "__main__":
    # Create Tasks
    N = 10
    tasks = [Task(i) for i in range(N+1)]
    for t, succ in dag.items():
        tasks[t].successors = [x for x in succ]
        tasks[t].comp_cost = [compcost(t, p) for p in 'ab']
        tasks[t].avg_comp = stats.mean(tasks[t].comp_cost)        
        for x in succ:
            tasks[x].predecessor = t
        # setup entry task (id=0)
        tasks[0].avg_comp = 0
        
    for task in tasks:
        logging.info(task)

    # Calculate Ranks
    for task in reversed(tasks):
        task.rank = ranku(task.id, tasks)
            
    # To return a new list, use the sorted() built-in function...
    newlist = sorted(tasks, key=lambda x: x.rank)

    for task in newlist:
        logging.info(task)