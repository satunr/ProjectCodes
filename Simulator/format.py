

#Define format of each packet as -- <sequence no, (node 1,time 1),(node 2,time 2), ... ,(node n, time n)>
class NewPacket(object):

    def form(self,src,T,exist):

        seq = str(src)
        if len(exist) == 0:
            exist.append(seq)

        exist.append((src,T))
        return exist


#p = NewPacket()
#print p.form(1,2,[])


