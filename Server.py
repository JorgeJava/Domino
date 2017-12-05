from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep

class ClientChannel(Channel):
    def Network(self,data):
        print(data)
        
        
    def Network_testeChamadaJorge(self,data):
        nome = data['name']
        print "ClientChannel = ",str(ClientChannel)
        print "nome = ",nome
        
        self._server.testeServerReceberInfo(nome)
        
        
class GameServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        
        Server.__init__(self,*args, **kwargs)
        self.playerChannels = []
        
        
    def Connected(self, channel, addr):
        print('new connection: ',channel)
        
        
    def testeServerReceberInfo(self,data):
        retorno = "RETORNO SERVER"    
        for channel in self.channels:
            channel.Send({"action":"testeRetornoServidorJorge","name":retorno})
        
        
print ("STARTING SERVER ON LOCALHOST")
gameServe = GameServer()

run = 1
while run:
    gameServe.Pump()
    sleep(0.01)