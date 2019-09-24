from Simulator.format import *


# (i) Flush old Packets and (ii) update existing packet information
def pHandling(recBuf,storeInterval,t,ID):

    p = NewPacket()
    pos = 0
    # print (recBuf)

    for packet in recBuf:
        # Packet generation time: startTime[1]
        startTime = packet[1]
        if t - startTime[1] > storeInterval:
            recBuf.remove(packet)

            # print "Flushing Packet:",packet,self.env.now

        else:

            lastEntry = packet[-1]
            if ID != lastEntry[0] and len(packet) > 0:
                recBuf[pos] = p.form(ID,t,packet)
                #print self.recBuf.items

        #print "Difference in time = %d " % self.env.now - tup[1]
        pos = pos + 1

    return recBuf


#Create New Packets
def packetC(recBuf, capacity, generationRate, ID, t,globCount):

    p = NewPacket()
    remaining = capacity - len(recBuf)
    # print "Remaining space in my buffer:",remaining

    iterate = min(remaining, generationRate)
    for i in range(iterate):

        #globCount += 1
        packet = p.form(ID, t, [])
        recBuf.append(packet)

    return recBuf,globCount

    # print "I am node %d. My buffer now: %s" % (self.ID,str(self.recBuf.items))
