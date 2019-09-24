import simpy


from Simulator.findNeighbors import *
from Simulator.packetHandling import *
from Simulator.simulationConstants import *
from Simulator.graphGenerator import *

#Every node is a class with some variables like node ID and neighbor set.
class Node(object):

    def __init__(self,env,ID):

        self.env = env
        #Create buffer memory (of capacity recBufferCapacity) for each node
        self.recBuf = simpy.Store(env,capacity = recBufferCapacity)
        self.ID = ID
        #Set of indegree and out-degree neighbors
        self.ind,self.out = self.neighbors()
        #print "I am node %d. My in-neighbors are %s and out-neighbors are %s" % (self.ID,str(self.ind),str(self.out))

        #If out-degree of a node > 0, initiate send process.
        if len(self.out) > 0:
            self.env.process(self.send())

        # If in-degree of a node > 0, initiate receive process.
        if len(self.ind) > 0:
            self.env.process(self.recv())


    def neighbors(self):

        return findN(G,self.ID)

    def packetTransfer(self):

        global Sent,drpcnt,globCount,Received

        iterate = min(transmissionRate, len(self.recBuf.items))
        for i in range(iterate):

            packet = yield self.recBuf.get()

            for k in self.out:

                globCount += 1.0
                Sent = Sent + 1.0

                if len(entities[k].recBuf.items) >= recBufferCapacity:
                    # print ("Dropping Packet:", packet, self.env.now)
                    drpcnt += 1.0

                # print "Sending Packet:",packet
                else:
                    entities[k].recBuf.put(packet)
                    Received += 1

    def send(self):

        #Keep track of total packet transmission
        global drpcnt,globCount,Sent

        while(True):

            # (i) Flush old Packets and (ii) update existing packet information
            self.recBuf.items = pHandling(self.recBuf.items, storeInterval, self.env.now, self.ID)

            # Create New Packets
            self.recBuf.items,globCount = packetC(self.recBuf.items,self.recBuf.capacity,generationRate,self.ID,self.env.now,globCount)

            #Perform routing (applies flooding at present)
            self.env.process(self.packetTransfer())

            #Wait certain time before next data generation
            yield self.env.timeout((nextGenerationDelay))


    def recv(self):

        # Keep track of total packet reception
        global Received,sink,Lat,sReceived

        while(True):

            #print "I am node %d. My buffer is %s" % (self.ID,str(self.recBuf.items))

            #Retrieve data from own memory buffer and calculate latency
            for i in range(min(retrievalRate,len(self.recBuf.items))):

                item = yield self.recBuf.get()

                if self.ID in sink:
                    # print ("Received Packet:",item)
                    #Received = Received + 1.0
                    hops = float(len(item)) - 1.0

                    #Current Average Latency
                    Lat = (Lat[0] + hops,Lat[1] + 1)

                    sReceived += 1.0
                #print "I am node %d. I received %s at time T = %d." % (self.ID,str(item),env.now)

            # Wait certain time before next data reception
            yield self.env.timeout(nextReceiptDelay)


GlobalTime = 0

#Generate network graph G
G,N,sink,p = generateG()

#Energy matrix
#E = [0.0 for i in range(len(G))]

#Create simpy environment and assign nodes to it.
env = simpy.Environment()
entities = [Node(env,i) for i in range(N)]
env.run(until = simulationTime)

# ---------------- This takes the control to line no. 9 ----------------


# ---------------- Results and Evaluations --------------------------

#update Sink Receive Count
for i in sink:
    sReceived += len(entities[i].recBuf.items)

print (Sent,Received,drpcnt)
PDR = Received / Sent * 100.0
print ("\nMy Data Delivery Rate is: %f" % (PDR), "%")
print ("\nMy Average Packet Latency is: %f seconds" % (float(Lat[0])/(float(Lat[1]))))
print ("Globcount:",globCount)

#for i in range(len(G.nodes())):
    #print (len(entities[i].recBuf.items))

print (len(entities[i].recBuf.items) + Received + drpcnt)
