'''
Created on 18 de nov de 2017

@author: jorge.rocha
'''

from PodSixNet.Connection import  ConnectionListener, connection
import pygame
from pygame.locals import QUIT, Rect
from pygame.constants import  MOUSEBUTTONDOWN
import random
import json

class Utils:
    listaIdImagens = []
    listaPedrasJogadorUm = []
    listaPedrasJogadorDois = []
    listaPedrasJogadorTres = []
    listaPedrasJogadorQuatro = []
    dominoRect = ''
    img = ''
    listaTodasPedrasEJogadores = []
    listaPedrasInseridasNaMesa = []
    ladosPedraMesa =[]
    esquerdaAcrescenta = 1
    direitaAcrescenta = 1
    rodaEsquerdaAcrescenta = False
    rodaDireitaAcrescenta = False
    dominoJogador = []
    proximoJogador = 1


class Games(ConnectionListener):

    def __init__(self):
        
        pygame.init()
        self.screen = pygame.display.set_mode( (800, 600), 0, 32 )
        
        #definicao de cor de fundo para o jogo 
        white = (0, 100, 0)
        self.screen.fill((white))
        
        #chamando de forma randomica as pedras de domino
#         posicaoImagemPedra = random.sample(xrange(0,5),1)
        self.fImage = open("detalheImagemDomino.json", "r")
        self.fimg = json.load( self.fImage )
        self.fImage.close()
        
        self.popularMaoJogadoresPedras()
        print "Utils.listaIdImagens = ",Utils.listaIdImagens
        print "Utils.listaPedrasJogadorUm = ",Utils.listaPedrasJogadorUm
        print "Utils.listaPedrasJogadorDois = ",Utils.listaPedrasJogadorDois
        print "Utils.listaPedrasJogadorTres = ",Utils.listaPedrasJogadorTres
        print "Utils.listaPedrasJogadorQuatro = ",Utils.listaPedrasJogadorQuatro
        
        Utils.listaPedrasJogadorUm = self.converterIdParaDadoCompletoPedra(Utils.listaPedrasJogadorUm,1)
        Utils.listaPedrasJogadorDois = self.converterIdParaDadoCompletoPedra(Utils.listaPedrasJogadorDois,2)
        Utils.listaPedrasJogadorTres = self.converterIdParaDadoCompletoPedra(Utils.listaPedrasJogadorTres,3)
        Utils.listaPedrasJogadorQuatro = self.converterIdParaDadoCompletoPedra(Utils.listaPedrasJogadorQuatro,4)
    
        print "Utils.listaIdImagens DEPOIS = ",Utils.listaIdImagens
        print "Utils.listaPedrasJogadorUm DEPOIS = ",Utils.listaPedrasJogadorUm
        print "Utils.listaPedrasJogadorDois DEPOIS = ",Utils.listaPedrasJogadorDois
        print "Utils.listaPedrasJogadorTres DEPOIS = ",Utils.listaPedrasJogadorTres
        print "Utils.listaPedrasJogadorQuatro DEPOIS = ",Utils.listaPedrasJogadorQuatro
        
        self.Connect()


    def popularMaoJogadoresPedras(self):
        for i in range(4):
            while not(len(self.fimg) == len(Utils.listaIdImagens)):
                #chamando de forma randomica as pedras de domino
                posicaoImagemPedra2 = random.sample(xrange(0,len(self.fimg)),1)
                if posicaoImagemPedra2[0] not in Utils.listaIdImagens:
                    
                    if len(Utils.listaPedrasJogadorUm) < 7:
                        Utils.listaIdImagens.append(posicaoImagemPedra2[0])
                        Utils.listaPedrasJogadorUm.append(posicaoImagemPedra2[0])
                        
                    elif len(Utils.listaPedrasJogadorDois) < 7:
                        Utils.listaIdImagens.append(posicaoImagemPedra2[0])
                        Utils.listaPedrasJogadorDois.append(posicaoImagemPedra2[0])
                        
                    elif len(Utils.listaPedrasJogadorTres) < 7:
                        Utils.listaIdImagens.append(posicaoImagemPedra2[0])
                        Utils.listaPedrasJogadorTres.append(posicaoImagemPedra2[0])
                        
                    elif len(Utils.listaPedrasJogadorQuatro) < 7:
                        Utils.listaIdImagens.append(posicaoImagemPedra2[0])
                        Utils.listaPedrasJogadorQuatro.append(posicaoImagemPedra2[0])

        
    def definirPosicaoPedrasJogadores(self,jogador,indice):
        posRetorno = {
                        "pos":[0,0],
                        "rotate":{"verify":False,
                                  "grau":''}}
        if jogador == 1 :
            posRetorno["pos"] = [(180/4)*(indice+4),500]
            # SE FOR JOGADOR DOIS ELE DEVERA RECEBER O ROTATE POIS AS PEDRAS IRAM FICAR DO LADO DIREITO DA TELA
        elif jogador == 2 :
            posRetorno["pos"] = [700,(170/4)*(indice+2)]
            posRetorno["rotate"]["verify"] = True
            posRetorno["rotate"]["grau"] = 90
            
        elif jogador == 3 :
            posRetorno["pos"] = [(180/4)*(indice+4),30]
            # SE FOR JOGADOR QUATRO ELE DEVERA RECEBER O ROTATE POIS AS PEDRAS IRAM FICAR DO LADO ESQUERDO DA TELA
        elif jogador == 4 :
            posRetorno["pos"] = [50,(170/4)*(indice+2)]
            posRetorno["rotate"]["verify"] = True
            posRetorno["rotate"]["grau"] = 180
        return posRetorno


    def converterIdParaDadoCompletoPedra(self,listaEntrada,jogador):
        listaRetorno = []
        
        for i in range(len(listaEntrada)):
            for j in range(len(self.fimg)):
                if listaEntrada[i] == self.fimg[j]['id']:
                    self.fimg[j]['jogador'] = jogador
                    posicao = self.definirPosicaoPedrasJogadores(jogador,i+1)
                    self.fimg[j]['pos'] = posicao['pos']
                    self.fimg[j]['rotate'] = posicao['rotate']  
                    listaRetorno.append(self.fimg[j])
                        
        return listaRetorno
    


    def chamadaImagensDomino(self,listaEntrada,jogador):
        
        
        for i in range(len(listaEntrada)):
            Utils.img = pygame.image.load(listaEntrada[i]['url'])
            Utils.img = pygame.transform.scale(Utils.img, (listaEntrada[i]['size']))
            
            if jogador == 1:
                Utils.listaPedrasJogadorUm[i]['rect'] = Rect( listaEntrada[i]['pos'], (listaEntrada[i]['size']))
                Utils.listaTodasPedrasEJogadores.append(Utils.listaPedrasJogadorUm[i])
                
            # SE FOR JOGADOR DOIS ELE DEVERA RECEBER O ROTATE POIS AS PEDRAS IRAM FICAR DO LADO DIREITO DA TELA
            elif jogador == 2:
                Utils.listaPedrasJogadorDois[i]['rect'] = Rect( listaEntrada[i]['pos'], (listaEntrada[i]['size'][1],listaEntrada[i]['size'][0]))
                Utils.img = pygame.transform.rotate(Utils.img, Utils.listaPedrasJogadorDois[i]["rotate"]["grau"])
                Utils.listaTodasPedrasEJogadores.append(Utils.listaPedrasJogadorDois[i])
            elif jogador == 3:
                Utils.listaPedrasJogadorTres[i]['rect'] = Rect( listaEntrada[i]['pos'], (listaEntrada[i]['size']))
                Utils.listaTodasPedrasEJogadores.append(Utils.listaPedrasJogadorTres[i])
            
            # SE FOR JOGADOR QUATRO ELE DEVERA RECEBER O ROTATE POIS AS PEDRAS IRAM FICAR DO LADO ESQUERDO DA TELA
            elif jogador == 4:
                Utils.listaPedrasJogadorQuatro[i]['rect'] = Rect( listaEntrada[i]['pos'], (listaEntrada[i]['size'][1],listaEntrada[i]['size'][0]))
                Utils.img = pygame.transform.rotate(Utils.img, Utils.listaPedrasJogadorDois[i]["rotate"]["grau"])
                Utils.listaTodasPedrasEJogadores.append(Utils.listaPedrasJogadorQuatro[i])
            
            self.screen.blit( Utils.img, listaEntrada[i]['pos'] )


    def chamadaEventoAoClicar(self,listaEntrada):
        for e in pygame.event.get():
            for i in range(len(listaEntrada)):
                if e.type == MOUSEBUTTONDOWN:
    #                 print "Pos : ", e.pos, "  Botao : ", e.button  
                    if listaEntrada[i]['rect'].collidepoint(e.pos[0], e.pos[1]):
                            print "Clicou no Domino = ",listaEntrada[i]['nomePedra']
    #                         Utils.listaTodasPedrasEJogadores.remove(listaEntrada[i])
    
                            if listaEntrada[i]['jogador'] == 1:
                                Utils.listaPedrasJogadorUm = self.atualizarListaDePedrasSelecionadas(
                                    Utils.listaPedrasJogadorUm,listaEntrada[i])
                                
                            elif listaEntrada[i]['jogador'] == 2:
                                Utils.listaPedrasJogadorDois = self.atualizarListaDePedrasSelecionadas(
                                    Utils.listaPedrasJogadorDois,listaEntrada[i])    
                                
                            elif listaEntrada[i]['jogador'] == 3:
                                Utils.listaPedrasJogadorTres = self.atualizarListaDePedrasSelecionadas(
                                    Utils.listaPedrasJogadorTres,listaEntrada[i])
                                
                            elif listaEntrada[i]['jogador'] == 4:
                                Utils.listaPedrasJogadorQuatro = self.atualizarListaDePedrasSelecionadas(
                                    Utils.listaPedrasJogadorQuatro,listaEntrada[i])
                            
                                    
                            break



    def atualizarListaDePedrasSelecionadas(self,listaDominosJogador,dominoEntrada):
        
        for j in range(len(listaDominosJogador)):
                            Utils.dominoJogador = []
                                
                            if listaDominosJogador[j]['id'] == dominoEntrada['id'] and dominoEntrada['nomePedra'] != 'VAZIO':
                                dominoJogadorTemp = {
                                    "url": listaDominosJogador[j]["url"], 
                                    "id": listaDominosJogador[j]["id"],
                                    "nomePedra":listaDominosJogador[j]["nomePedra"],
                                    "ladosPedra":listaDominosJogador[j]["ladosPedra"],
                                    "size":listaDominosJogador[j]["size"],
                                    "pos":listaDominosJogador[j]["pos"],
                                    "rotate":listaDominosJogador[j]["rotate"],
                                    "rect":listaDominosJogador[j]["rect"],
                                     "rectLadosPedra":listaDominosJogador[j]["rectLadosPedra"],
                                    "jogador":listaDominosJogador[j]["jogador"]
                                  }
                                Utils.dominoJogador.append(dominoJogadorTemp)
                                
                                if len(Utils.listaPedrasInseridasNaMesa) != 0:   
    #                                 for i in range(len(Utils.listaPedrasInseridasNaMesa)):
                                        if (Utils.ladosPedraMesa[0] in dominoEntrada['ladosPedra']) or (Utils.ladosPedraMesa[1] in dominoEntrada['ladosPedra']):
                                                
                                                print "Utils.dominoJogador = ",Utils.dominoJogador
                                                Utils.listaPedrasInseridasNaMesa.append(Utils.dominoJogador[0])
                
                                                print "Utils.listaPedrasInseridasNaMesa = ",Utils.listaPedrasInseridasNaMesa 
                                                listaDominosJogador[j]['url'] = "img/pedras_domino\\vazio.png"
                                                listaDominosJogador[j]['nomePedra'] = "VAZIO"
                                                self.montarDominosCentroDaMesa()
                                else:
                                                print "Utils.dominoJogador = ",Utils.dominoJogador
                                                Utils.listaPedrasInseridasNaMesa.append(Utils.dominoJogador[0])
                
                                                print "Utils.listaPedrasInseridasNaMesa = ",Utils.listaPedrasInseridasNaMesa 
                                                listaDominosJogador[j]['url'] = "img/pedras_domino\\vazio.png"
                                                listaDominosJogador[j]['nomePedra'] = "VAZIO"
                                                self.montarDominosCentroDaMesa()
                                
                                
                            pygame.display.update()
                                    
        print "Utils.listaPedrasInseridasNaMesa = ",Utils.listaPedrasInseridasNaMesa                           
    
        return listaDominosJogador


    def montarDominosCentroDaMesa(self):
    #     if(len(Utils.listaPedrasInseridasNaMesa) > 0):
    #         for i in range(len(Utils.listaPedrasInseridasNaMesa)):
                self.definirPosicaoPedrasCentroMesa(len(Utils.listaPedrasInseridasNaMesa)-1)
                self.chamadaImagensDominoCentroMesa()




    def definirPosicaoPedrasCentroMesa(self,indice):
    
        if indice == 0:
            Utils.listaPedrasInseridasNaMesa[indice]['pos'] = [410,270]
            # IRA HABILITAR A OPCAO PARA RODAR A PEDRA
    #         if Utils.listaPedrasInseridasNaMesa[indice]["nomePedra"] not in ["branca","pio","duque","terno","quadra","quina","sena"]:
            Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["verify"] = True
            Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["grau"] = 90
       
            Utils.ladosPedraMesa = Utils.listaPedrasInseridasNaMesa[indice]["ladosPedra"] 
        else:
            ladosPedraIndiceAtual = Utils.listaPedrasInseridasNaMesa[indice]["ladosPedra"] 
            
            if Utils.ladosPedraMesa[0] == ladosPedraIndiceAtual[0]:
                Utils.listaPedrasInseridasNaMesa[indice]['pos'] = [(410-81*Utils.esquerdaAcrescenta),270]
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["verify"] = True
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["grau"] = 270
                    
                Utils.ladosPedraMesa = [ladosPedraIndiceAtual[1],Utils.ladosPedraMesa[1]]
                Utils.esquerdaAcrescenta += 1
                
            elif Utils.ladosPedraMesa[0] == ladosPedraIndiceAtual[1]:
                Utils.listaPedrasInseridasNaMesa[indice]['pos'] = [(410-81*Utils.esquerdaAcrescenta),270]
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["verify"] = True
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["grau"] = 90
                    
                Utils.ladosPedraMesa = [ladosPedraIndiceAtual[0],Utils.ladosPedraMesa[1]]
                Utils.esquerdaAcrescenta += 1
                
            elif Utils.ladosPedraMesa[1] == ladosPedraIndiceAtual[0]:
                Utils.listaPedrasInseridasNaMesa[indice]['pos'] = [(410+81*Utils.direitaAcrescenta),270]
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["verify"] = True
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["grau"] = 90
                    
                Utils.ladosPedraMesa = [Utils.ladosPedraMesa[0],ladosPedraIndiceAtual[1]]
                Utils.direitaAcrescenta += 1
                
            elif Utils.ladosPedraMesa[1] == ladosPedraIndiceAtual[1]:
                Utils.listaPedrasInseridasNaMesa[indice]['pos'] = [(410+81*Utils.direitaAcrescenta),270]
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["verify"] = True
                Utils.listaPedrasInseridasNaMesa[indice]["rotate"]["grau"] = 270
                    
                Utils.ladosPedraMesa = [Utils.ladosPedraMesa[0],ladosPedraIndiceAtual[0]]
                Utils.direitaAcrescenta += 1
            

    def chamadaImagensDominoCentroMesa(self):
        
        for i in range(len(Utils.listaPedrasInseridasNaMesa)):
            Utils.img = pygame.image.load(Utils.listaPedrasInseridasNaMesa[i]['url'])
            size = Utils.listaPedrasInseridasNaMesa[i]['size']
            pos = Utils.listaPedrasInseridasNaMesa[i]['pos']
            Utils.img = pygame.transform.scale(Utils.img, (size))
    
            if Utils.listaPedrasInseridasNaMesa[i]["rotate"]["verify"] == True:
                
                Utils.img = pygame.transform.rotate(Utils.img, Utils.listaPedrasInseridasNaMesa[i]["rotate"]["grau"])
    
                Utils.listaPedrasInseridasNaMesa[i]["rectLadosPedra"]["rectEsquerda"] = Rect( (pos[0],(pos[1]+2)), ((size[0]-6),(size[1]/2))) 

                print "POS = ",pos
                print "SIZE = ",size
                
                Utils.listaPedrasInseridasNaMesa[i]["rectLadosPedra"]["rectDireita"] =Rect( ((pos[0]+40),pos[1]+2), ((size[0]-7),(size[1]/2)))
            
            else:
                Utils.listaPedrasInseridasNaMesa[i]['rect'] = Rect( Utils.listaPedrasInseridasNaMesa[i]['pos'], (Utils.listaPedrasInseridasNaMesa[i]['size']))
            self.screen.blit( Utils.img, Utils.listaPedrasInseridasNaMesa[i]['pos'] )
            pygame.display.update()
        
        
    def chamadaEventoAoClicarDominoMesa(self):
        for e in pygame.event.get():
            for i in range(len(Utils.listaPedrasInseridasNaMesa)):
                if e.type == MOUSEBUTTONDOWN:
    #                 print "Pos : ", e.pos, "  Botao : ", e.button
    
                    if Utils.listaPedrasInseridasNaMesa[i]["rectLadosPedra"]["rectEsquerda"] != {} and Utils.listaPedrasInseridasNaMesa[i]["rectLadosPedra"]["rectDireita"] != {}: 
                        if Utils.listaPedrasInseridasNaMesa[i]["rectLadosPedra"]["rectEsquerda"].collidepoint(e.pos[0], e.pos[1]):
                                print "Clicou no Domino LADO ESQUERDO"
                                print "VALOR DO LADO ESQUERDO = ",Utils.listaPedrasInseridasNaMesa[i]["ladosPedra"][0]
                        
                        if Utils.listaPedrasInseridasNaMesa[i]["rectLadosPedra"]["rectDireita"].collidepoint(e.pos[0], e.pos[1]):
                                print "Clicou no Domino LADO DIREITO"
                                print "VALOR DO LADO DIREITO = ",Utils.listaPedrasInseridasNaMesa[i]["ladosPedra"][1]        
     
     
    def Network_testeRetornoServidorJorge(self,data):
        print "TUDO OK"
        print "data = ", data      
    
    def run(self):
        #CHAMADA EM REDE
        self.name = "JORGE"
        #BUSCA O NOME DA FUNCAO E PASSA O PARAMETRO NO CASO O MEU NOME
        self.Send({"action":"testeChamadaJorge","name":self.name})
        #CHAMADA EM REDE
        
        run = 1
        while run:
            
            #CONEXAO REDE
            connection.Pump()
            self.Pump()
        
            self.chamadaEventoAoClicar(Utils.listaTodasPedrasEJogadores)
            self.chamadaEventoAoClicarDominoMesa()
            
            self.chamadaImagensDomino(Utils.listaPedrasJogadorUm,1)
        
            self.chamadaImagensDomino(Utils.listaPedrasJogadorDois,2)
        
            self.chamadaImagensDomino(Utils.listaPedrasJogadorTres,3)
        
            self.chamadaImagensDomino(Utils.listaPedrasJogadorQuatro,4)
                
            pygame.display.update()
            

jogo = Games()
jogo.run()

