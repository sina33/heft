total_cores = 4
low_perf_multiplier = 2


dag={1:(2,3,4,5,6,7),
     2:(19,),
     3:(7,8),
     4:(9,),
     5:(10,),
     6:(11,),
     7:(8,9,10,11,12),
     8:(19,),
     9:(12,13),
     10:(14,),
     11:(15,),
     12:(13,14,15,16),
     13:(19,),
     14:(16,17),
     15:(18,),
     16:(17,18),
     17:(19,),
     18:(19,),
     19:()}


def compcost(job, agent):
    if(job==0):
        return 0
    if(job==1):
        if agent == 'a' or agent == 'b':
            return 80 * low_perf_multiplier
        else:
            return 80
    if(job==2):
        if agent == 'a' or agent == 'b':
            return 40 * low_perf_multiplier
        else:
            return 40
    if(job==3):
        if agent == 'a' or agent == 'b':
            return 40 * low_perf_multiplier
        else:
            return 40
    if(job==4):
        if agent == 'a' or agent == 'b':
            return 40 * low_perf_multiplier
        else:
            return 40
    if(job==5):
        if agent == 'a' or agent == 'b':
            return 40 * low_perf_multiplier
        else:
            return 40
    if(job==6):
        if agent == 'a' or agent == 'b':
            return 40 * low_perf_multiplier
        else:
            return 40
    if(job==7):
        if agent == 'a' or agent == 'b':
            return 60 * low_perf_multiplier
        else:
            return 60
    if(job==8):
        if agent == 'a' or agent == 'b':
            return 30 * low_perf_multiplier
        else:
            return 30
    if(job==9):
        if agent == 'a' or agent == 'b':
            return 30 * low_perf_multiplier
        else:
            return 30
    if(job==10):
        if agent == 'a' or agent == 'b':
            return 30 * low_perf_multiplier
        else:
            return 30
    if(job==11):
        if agent == 'a' or agent == 'b':
            return 30 * low_perf_multiplier
        else:
            return 30
    if(job==12):
        if agent == 'a' or agent == 'b':
            return 40 * low_perf_multiplier
        else:
            return 40
    if(job==13):
        if agent == 'a' or agent == 'b':
            return 20 * low_perf_multiplier
        else:
            return 20
    if(job==14):
        if agent == 'a' or agent == 'b':
            return 20 * low_perf_multiplier
        else:
            return 20
    if(job==15):
        if agent == 'a' or agent == 'b':
            return 20 * low_perf_multiplier
        else:
            return 20
    if(job==16):
        if agent == 'a' or agent == 'b':
            return 20 * low_perf_multiplier
        else:
            return 20
    if(job==17):
        if agent == 'a' or agent == 'b':
            return 10 * low_perf_multiplier
        else:
            return 10
    if(job==18):
        if agent == 'a' or agent == 'b':
            return 10 * low_perf_multiplier
        else:
            return 10
    if(job==19):
            return 0





def commcost(ni, nj, A, B):
    return 0
    if(A==B):
        return 0
    else:
        if(ni==1 and nj==2):
            return 60
        if(ni==1 and nj==3):
            return 60
        if(ni==1 and nj==4):
            return 60
        if(ni==1 and nj==5):
            return 60
        if(ni==1 and nj==6):
            return 60
        if(ni==1 and nj==7):
            return 60

        if(ni==3 and nj==7):
            return 40
        if(ni==3 and nj==8):
            return 40
        if(ni==4 and nj==9):
            return 40
        if(ni==5 and nj==10):
            return 40
        if(ni==6 and nj==11):
            return 40

        if(ni==7 and nj==8):
            return 60
        if(ni==7 and nj==9):
            return 60
        if(ni==7 and nj==10):
            return 60
        if(ni==7 and nj==11):
            return 60
        if(ni==7 and nj==12):
            return 60

        if(ni==9 and nj==12):
            return 40
        if(ni==9 and nj==13):
            return 40
        if(ni==10 and nj==14):
            return 40
        if(ni==11 and nj==15):
            return 40

        if(ni==12 and nj==13):
            return 60
        if(ni==12 and nj==14):
            return 60
        if(ni==12 and nj==15):
            return 60
        if(ni==12 and nj==16):
            return 60

        if(ni==14 and nj==16):
            return 40
        if(ni==14 and nj==17):
            return 40
        if(ni==15 and nj==18):
            return 40
        if(ni==16 and nj==17):
            return 60
        if(ni==16 and nj==18):
            return 60
        else:
            return 0