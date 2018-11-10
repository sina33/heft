"""
This is a simple script to use the HEFT function provided based on the example given in the original HEFT paper.
You have to define the DAG, compcost function and commcost funtion.

Each task/job is numbered 1 to 10
Each processor/agent is named 'a', 'b' and 'c'

Output expected:
Ranking:
[10, 8, 7, 9, 6, 5, 2, 4, 3, 1]
Schedule:
('a', [Event(job=2, start=27, end=40), Event(job=8, start=57, end=62)])
('b', [Event(job=4, start=18, end=26), Event(job=6, start=26, end=42), Event(job=9, start=56, end=68), Event(job=10, start=73, end=80)])
('c', [Event(job=1, start=0, end=9), Event(job=3, start=9, end=28), Event(job=5, start=28, end=38), Event(job=7, start=38, end=49)])
{1: 'c', 2: 'a', 3: 'c', 4: 'b', 5: 'c', 6: 'b', 7: 'c', 8: 'a', 9: 'b', 10: 'b'}
"""


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
            return 80
    if(job==2):
            return 40
    if(job==3):
            return 40
    if(job==4):
            return 40
    if(job==5):
            return 40
    if(job==6):
            return 40
    if(job==7):
            return 60
    if(job==8):
            return 30
    if(job==9):
            return 30
    if(job==10):
            return 30
    if(job==11):
            return 30
    if(job==12):
            return 40
    if(job==13):
            return 20
    if(job==14):
            return 20
    if(job==15):
            return 20
    if(job==16):
            return 20
    if(job==17):
            return 10
    if(job==18):
            return 10
    if(job==19):
            return 0





def commcost(ni, nj, A, B):

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