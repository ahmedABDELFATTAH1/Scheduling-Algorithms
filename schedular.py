import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
def readInputFile():
    #read from input file
    myfile=open("input.txt", "r")
    #contents will be array of lines from the file
    contents=myfile.readlines()
    # a directory to store key:value pairs
    process_info={}    
    process_info['PNUMBER']=int(contents[0])
    process_info['ARR_MEAN']=float(contents[1].split()[0])
    process_info['ARR_SD']=float(contents[1].split()[1])
    process_info['RUN_MEAN']=float(contents[2].split()[0])
    process_info['RUN_SD']=float(contents[2].split()[1])
    process_info['LAMDA']=float(contents[3])
    return process_info
    

def generateProecesses(process_info):
    gen_process_info={}
    #generate array of arrival times generated from normal distribution and rounded to 1 decimal places
    gen_process_info['arrivaltime']=np.round(np.random.normal(process_info['ARR_MEAN'], process_info['ARR_SD'],process_info['PNUMBER']),1)
    for i in range(len(gen_process_info['arrivaltime'])):
        if(gen_process_info['arrivaltime'][i]<0):
            gen_process_info['arrivaltime'][i]=0
    #generate array of run time generated from normal distribution and rounded to 1 decimal places
    gen_process_info['runtime']=np.round(np.random.normal(process_info['RUN_MEAN'], process_info['RUN_SD'], process_info['PNUMBER']),1)
    for i in range(len(gen_process_info['runtime'])):
        if(gen_process_info['runtime'][i]<0):
            gen_process_info['runtime'][i]=0
    #generate array of priority generated from poission distribution 
    gen_process_info['priority']=np.random.poisson(process_info['LAMDA'], process_info['PNUMBER'])
    return gen_process_info

def writeOutputFile(gen_process_info,process_number):   
    f=open("out1.txt", "a+") 
    f.write(str(process_number)+'\n')
    for i in range(process_number):
        f.write(str(i+1)+" "+str(gen_process_info['arrivaltime'][i])+" "+str(gen_process_info['runtime'][i])+" "+str(gen_process_info['priority'][i])+'\n')


            
        
def writeProcessesInfo(processesInfo):  
    f=open("info.txt", "a+")
    Average_Turnaround=0
    Average_Weighted_turnaround=0
    for i in range(len(processesInfo)):
        f.write("for process "+str(processesInfo[i][0])+'\n')
        f.write("waiting time  = "+str(processesInfo[i][1])+'\n')  
        f.write("turnaround time  = "+str(processesInfo[i][2])+'\n')  
        f.write("weighted turnaround time  = "+str(processesInfo[i][3])+'\n')  
    Average_Turnaround = processesInfo[i][2]/len(processesInfo)
    Average_Weighted_turnaround = processesInfo[i][3]/len(processesInfo)
    f.write("############################################ \n")  
    f.write("Average Turnaround time of theschedule = "+str(Average_Turnaround)+'\n')  
    f.write("Average Weighted turnaround time of theschedule  = "+str(Average_Weighted_turnaround)+'\n')  
    
            
def computematrix(out_put,processarray):  
    f=open("info.txt", "a+")
    Average_Turnaround=0
    Average_Weighted_turnaround=0
    for i in range(len(processarray)):
        f.write("for proecess "+str(i+1)+'\n')
        starttime=processarray[i][1]
        endtime=0       
        for k in range(len(out_put)-1,-1,-1):
            if(int(out_put[k])==(i+1)):
                endtime=k
                break
        turnaroundtime=((endtime/10)-starttime)
        Average_Turnaround+=turnaroundtime
        bursttime=np.round(processarray[i][2],1)
        waitingtime=max(np.round(turnaroundtime-bursttime,1),0)
        waightedturntime=np.round(turnaroundtime/bursttime,1)
        Average_Weighted_turnaround+=waightedturntime
        f.write("waiting time  = "+str(waitingtime)+'\n')  
        f.write("turnaround time  = "+str(np.round(turnaroundtime,1))+'\n')  
        f.write("weighted turnaround time  = "+str(waightedturntime)+'\n')  
    Average_Turnaround/=len(processarray)
    Average_Weighted_turnaround/=len(processarray)
    f.write("############################################ \n")  
    f.write("Average Turnaround time of theschedule = "+str(Average_Turnaround)+'\n')  
    f.write("Average Weighted turnaround time of theschedule  = "+str(Average_Weighted_turnaround)+'\n')  
    
def preemptiveShortestRemainingTimeNext(processarray:np.float16,c_s): 
    #first sort the processes by arrival time then compy them into new array       
    processarraynew=np.copy(processarray[processarray[:,1].argsort(kind='stable')])
    
    processesturn=0   #index to current process     
    scheduling_queue=[]   #thsi will act exactly like the scheduling_queue
    timing=processarraynew[0][1] # the clock (increasing by .1 at every time)
    out_put=[] #will hold the current running process number at every time stamp .1
    
    #untill any process arrives
    for i in range(0,int(timing*10)):
        out_put.append(-1)  # 0 indecates context switching or no running       
    c_process_number=-1   
    context_switching_value=int(c_s*10)
    while True:
        if (processesturn>=len(processarraynew)) and (len(scheduling_queue)==0):
            #if scheduling queue is empty and there is no processes will enter it
            #finish 
            x=np.arange(0,len(out_put)/10,.1)
            plt.scatter(x, out_put,alpha=1,linewidths=.1,s=2)            
            plt.title('Preemptive Shortest Remaining Time Next')
            plt.xlabel('time')
            plt.ylabel('process number')
            computematrix(out_put,processarray)
            plt.savefig("graph")
            plt.show()              
            break
        #while there are new process to enter at this time          
        while processesturn<len(processarraynew):            
            if processarraynew[processesturn][1]<= timing:
                scheduling_queue.append(processarraynew[processesturn])
                #first sort by process number then by remaining time
                scheduling_queue= sorted(scheduling_queue, key=lambda reminingtime: (reminingtime[2],reminingtime[1]))
                processesturn+=1
            else:
                break        
        #if the scheduling queue is empty
        if len(scheduling_queue)==0:
            out_put.append(-1)
            timing+=.1
            continue
        #if a new processs running go and do context switching
        if c_process_number != -1 and c_process_number!=scheduling_queue[0][0]:
            #this means do context switching
            while(context_switching_value!=0):
                timing+=.1
                context_switching_value-=1
                out_put.append(0)
            c_process_number=scheduling_queue[0][0]
            context_switching_value  =int(c_s*10)
            continue
        #the current running process is the first on in the queue
        c_process_number=scheduling_queue[0][0]
        #reseve this time slot to this running proecess
        out_put.append(c_process_number)
        timing+=.1
        scheduling_queue[0][2]-=.1
        #if the remaining time in the runnig proecess is 0 -> pop it from the queue
        if(np.round(scheduling_queue[0][2],1)==0):
            scheduling_queue.pop(0)
        timing=np.round(timing,1)   
        
        
   #FCFS    
   ############################################################################################
def FCFS(processArray:np.float16,c_s):
    #sorting processes according to arrival time
    sortedProcesses=np.copy(processarray[processArray[:,1].argsort(kind='stable')])  
    ProcessesInfo = np.zeros([len(processArray),4])
    t=0   #timer
    hPlotXFrom = []
    hPlotXTo = []
    hPlotY = []

    vPlotYFrom = []
    vPlotYTo = []
    vPlotX = []

    for i in range (len(sortedProcesses)): #iterating on each process
        y = sortedProcesses[i][0]
        xFrom = 0
        xTo = 0
        if(sortedProcesses[i][1] >= t): #if the arrival time of the current process is bigger than or equal time
            xFrom = sortedProcesses[i][1] + c_s  #make graph from process arrival time + context switch
            t = xTo = xFrom + sortedProcesses[i][2] #perform process and change timer to the time at which process ends
           
        else:  #if the arrival time of the current process is less that timer
            xFrom = t + c_s       #leave time for context switch and start process
            t = xTo = xFrom + sortedProcesses[i][2] #perform process and change timer to the time at which process ends
            y = sortedProcesses[i][0]  

        ProcessesInfo[i][0] = sortedProcesses[i][0] #process number  
        ProcessesInfo[i][1] = t - sortedProcesses[i][2] - sortedProcesses[i][1] #wait time  
        ProcessesInfo[i][2] = t-sortedProcesses[i][1] #turn around time
        ProcessesInfo[i][3] = ProcessesInfo[i][2]/sortedProcesses[i][2]  # weighted turn around time
        
        #add graph  data
        ######################
        
        #horizontal lines data

        hPlotXFrom.append(t - sortedProcesses[i][2] - c_s) # context switch start
        hPlotXTo.append(t - sortedProcesses[i][2]) #context switch end
        hPlotY.append(0) # at height 0

        hPlotXFrom.append(xFrom)
        hPlotXTo.append(xTo)
        hPlotY.append(y) 

        #vertical lines data
        vPlotYFrom.append(0)
        vPlotYFrom.append(0)
        vPlotYTo.append(y)
        vPlotYTo.append(y)
        vPlotX.append(xFrom)
        vPlotX.append(xTo)

        ###################### 

    #showing graph
    #################################################
    plt.hlines(hPlotY,hPlotXFrom,hPlotXTo) #drawing horizontal lines
    plt.vlines(vPlotX,vPlotYFrom,vPlotYTo) #drawing vertical lines
    plt.ylabel('Processes Number')
    plt.title('X')

    
    plt.show()
    ###################################################     
    writeProcessesInfo(ProcessesInfo)  
############################################################################################
   
#Highest priority first    
############################################################################################
def HPF(processArray:np.float16,c_s):
    #sorting processes according to priority
    sortedProcesses = np.array(sorted(processArray, key= lambda x: -x[3])) 
    
    ProcessesInfo = np.zeros([len(processArray),4])
    t=0   #timer
    hPlotXFrom = []
    hPlotXTo = []
    hPlotY = []

    vPlotYFrom = []
    vPlotYTo = []
    vPlotX = []
    
    for i in range (len(sortedProcesses)): #iterating on each process
        y = sortedProcesses[i][0] 
        if(sortedProcesses[i][1] >= t): #if the arrival time of the current process is bigger than or equal time
            xFrom = sortedProcesses[i][1] + c_s  #make graph from process arrival time + context switch
            t = xTo = xFrom + sortedProcesses[i][2] #perform process and change timer to the time at which process ends
           
        else:  #if the arrival time of the current process is less that timer
            xFrom = t + c_s       #leave time for context switch and start process
            t = xTo = xFrom + sortedProcesses[i][2] #perform process and change timer to the time at which process ends

        ProcessesInfo[i][0] = sortedProcesses[i][0] #process number  
        ProcessesInfo[i][1] = t - sortedProcesses[i][2] - sortedProcesses[i][1] #wait time  
        ProcessesInfo[i][2] = t-sortedProcesses[i][1] #turn around time
        ProcessesInfo[i][3] = ProcessesInfo[i][2]/sortedProcesses[i][2]  # weighted turn around time
        
        #adding graph data   
        ############################
        #horizontal lines data
        hPlotXFrom.append(t - sortedProcesses[i][2] - c_s) # context switch start
        hPlotXTo.append(t - sortedProcesses[i][2]) #context switch end
        hPlotY.append(0) # at height 0

        hPlotXFrom.append(xFrom)
        hPlotXTo.append(xTo)
        hPlotY.append(y) 

        #vertical lines data
        vPlotYFrom.append(0)
        vPlotYFrom.append(0)
        vPlotYTo.append(y)
        vPlotYTo.append(y)
        vPlotX.append(xFrom)
        vPlotX.append(xTo)
        ######################  
                 
     #showing graph
    #################################################
    plt.hlines(hPlotY,hPlotXFrom,hPlotXTo) #drawing horizontal lines
    plt.vlines(vPlotX,vPlotYFrom,vPlotYTo) #drawing vertical lines
    plt.ylabel('Processes Number')
    plt.title('X')

    plt.show()
    ###################################################    
    writeProcessesInfo(process_info)
############################################################################################


#Round Robin 
############################################################################################
def RoundRobin(processArray:np.float16,c_s,quantum):
    #sorting processes according to Arrival time
    sortedProcesses=np.copy(processArray[processArray[:,1].argsort(kind='stable')]) 

    #saving Burst time
    totalTime = np.zeros(int(np.max(processArray[:,0]))+1)
    for i in range (len(processArray)):
        totalTime[int(processArray[i][0])] = processArray[i][2]

    #will save processes info(TAT,FT) here
    ProcessesInfo = np.ones([int(np.max(processArray[:,0])) + 1,4])  
    ProcessesInfo = np.negative(ProcessesInfo)

    readyQueue = []  #processes ready to be scheduled
    t = 0     #timer

    #graph data
    hPlotXFrom = []
    hPlotXTo = []
    hPlotY = []
    vPlotYFrom = []
    vPlotYTo = []
    vPlotX = []
    reAddedProcess = None
    while  len(readyQueue) != 0 or len(sortedProcesses) != 0 or  reAddedProcess is not None:
        if len(readyQueue) == 0 and  reAddedProcess is None and t < sortedProcesses[0][1]: #if the ready queue is empty move timer to the arrival time of the first process
            t = sortedProcesses[0][1]
        
        #adding ready elements in ready queue
        #############################################################
        for i in range (len(sortedProcesses)):
            if(sortedProcesses[0][1] <= t): #it should be in ready queue
                readyQueue.append(sortedProcesses[0]) #put ready process in ready queue
                sortedProcesses = np.delete(sortedProcesses, 0,0) #deleting ready process from the array
            else:
                break
        if reAddedProcess is not None:
            readyQueue.append(reAddedProcess)   
            reAddedProcess = None
        ###############################################################

        
        #scheduling ready process
        ##########################################################  
        scheduledProcess = readyQueue.pop(0)  #getting process to be scheduled 
        sameProcess = False #checking if te previous and current processes are the same to decide to add context switch or no
        if len(hPlotY) != 0 and hPlotY[-1] == scheduledProcess[0]:
            sameProcess = True
        else :
            sameProcess = False
            t = t + c_s #adding the context switch
            y = scheduledProcess[0]
        xFrom = t
        xTo = xFrom
        if(scheduledProcess[2] > quantum): #subtract quantum from process and re add it in ready queue
            t = xTo = xTo + quantum
            scheduledProcess[2] = scheduledProcess[2] - quantum 
            reAddedProcess = scheduledProcess
        else: #dont add it again in the queue it's done
            t = xTo = xTo + scheduledProcess[2]
            ProcessesInfo[int(scheduledProcess[0])][0] = scheduledProcess[0] #process number  
            ProcessesInfo[int(scheduledProcess[0])][2] = t-scheduledProcess[1] #turn around time
            ProcessesInfo[int(scheduledProcess[0])][3] = ProcessesInfo[int(scheduledProcess[0])][2]/totalTime[int(scheduledProcess[0])] # weighted turn around time
            ProcessesInfo[int(scheduledProcess[0])][1] = ProcessesInfo[int(scheduledProcess[0])][2] - totalTime[int(scheduledProcess[0])]   #wait time
           #turn around time
          
              ##########################################################

        #adding graph data   
        ############################
        #horizontal lines data
        if(not sameProcess): #if the process changed we neeed context switch
            hPlotXFrom.append(xFrom - c_s) # context switch start
            hPlotXTo.append(xFrom) #context switch end
            hPlotY.append(0) # at height 0

        hPlotXFrom.append(xFrom)
        hPlotXTo.append(xTo)
        hPlotY.append(y) 
        
        #vertical lines data
        vPlotYFrom.append(0)
        vPlotYFrom.append(0)
        vPlotYTo.append(y)
        vPlotYTo.append(y)
        vPlotX.append(xFrom)
        vPlotX.append(xTo)
        ######################  
     #showing graph
    #################################################
    plt.hlines(hPlotY,hPlotXFrom,hPlotXTo) #drawing horizontal lines
    plt.vlines(vPlotX,vPlotYFrom,vPlotYTo) #drawing vertical lines
    plt.ylabel('Processes Number')
    plt.title('X')
    plt.show()
    ###################################################
    delRows = []  
    for i in range(len(ProcessesInfo)):
        if ProcessesInfo[i][0] == -1:
            delRows.append(i)
    ProcessesInfo = np.delete(ProcessesInfo,delRows,0)  
    writeProcessesInfo(ProcessesInfo)
############################################################################################
                
        

    

   
#process_info=readInputFile()
#gen_process_info=generateProecesses(process_info)
processarray=np.zeros((4,4))
#processarray[:,0]=np.arange(1,process_info['PNUMBER']+1,1)
#processarray[:,1]=gen_process_info['arrivaltime']
#processarray[:,2]=gen_process_info['runtime']
#processarray[:,3]=gen_process_info['priority']
#processarray[:,0]=[1,2,3]
#processarray[:,1]=[1,2,3]
#processarray[:,2]=[1,1,1]
#processarray[:,3]=[1,1,1]
processarray[0,:] = [1,1,5,1] 
processarray[1,:] = [2,1,1,2] 
processarray[2,:] = [3,1,1,3] 
processarray[3,:] = [4,1,1,4] 
preemptiveShortestRemainingTimeNext(processarray,1)
#RoundRobin(processarray,1,1)
#HPF(processarray,1)
#FCFS(processarray,1)
#writeOutputFile(gen_process_info,process_info['PNUMBER'])