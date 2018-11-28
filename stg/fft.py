total_cores = 4
low_perf_multiplier = 2


dag={1:(2,3,4,5),
     2:(6,9),
     3:(6,7),
     4:(7,8),
     5:(8,9),
     6:(10,),
     7:(11,),
     8:(12,),
     9:(13,),
     10:(14,),
     11:(14,),
     12:(14,),
     13:(14,),
     14:()}


def compcost(job, agent):
    if(job==0):
        return 0 
    if(job==1):
        if agent == 'a' or agent == 'b':
            return 1 * low_perf_multiplier
        else:
            return 1
    if(job==2):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==3):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==4):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==5):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==6):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==7):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==8):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==9):
        if agent == 'a' or agent == 'b':
            return 5 * low_perf_multiplier
        else:
            return 5
    if(job==10):
        if agent == 'a' or agent == 'b':
            return 14 * low_perf_multiplier
        else:
            return 14
    if(job==11):
        if agent == 'a' or agent == 'b':
            return 14 * low_perf_multiplier
        else:
            return 14
    if(job==12):
        if agent == 'a' or agent == 'b':
            return 14 * low_perf_multiplier
        else:
            return 14
    if(job==13):
        if agent == 'a' or agent == 'b':
            return 14 * low_perf_multiplier
        else:
            return 14
    if(job==14):
        if agent == 'a' or agent == 'b':
            return 1 * low_perf_multiplier
        else:
            return 1




def commcost(ni, nj, A, B):
    return 0
    if(A==B):
        return 0
    else:
        if(ni==1 and nj==2):
            return 24
        if(ni==1 and nj==3):
            return 24
        if(ni==1 and nj==4):
            return 24
        if(ni==1 and nj==5):
            return 24
        if(ni==2 and nj==6):
            return 16
        if(ni==2 and nj==9):
            return 16
        if(ni==3 and nj==6):
            return 16
        if(ni==3 and nj==7):
            return 16
        if(ni==4 and nj==7):
            return 16
        if(ni==4 and nj==8):
            return 16
        if(ni==5 and nj==8):
            return 16
        if(ni==5 and nj==9):
            return 16
        if(ni==6 and nj==10):
            return 16
        if(ni==7 and nj==11):
            return 16
        if(ni==8 and nj==12):
            return 16
        if(ni==9 and nj==13):
            return 16
        if(ni==10 and nj==14):
            return 16
        if(ni==11 and nj==14):
            return 16
        if(ni==12 and nj==14):
            return 16
        if(ni==13 and nj==14):
            return 16
        else:
            return 0