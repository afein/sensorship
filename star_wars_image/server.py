import threading
import time
import SocketServer
import json
import pygame

started = False
playing = False
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("/src/starwars.wav")

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global started
        global playing
        self.data = self.request.recv(1024).strip()
        print "%s wrote: " % self.client_address[0]
        print self.data

        if "GroveButton" in self.data:
            print "GroveButton found"
            if '"value": 1' in self.data and not playing:
                print "button pressed"
                if not started:
                    pygame.mixer.play()
                    print "started music"
                    started = True
                else:
                    print "unpaused music"
                    pygame.mixer.music.unpause()
                playing = True
                time.sleep(5)
            elif '"value": 0' in self.data and playing:
                print "paused music"
                pygame.mixer.music.pause()
                playing = False

        self.request.send(self.data.upper())

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":

    HOST = ''
    PORT_A = 1234
    PORT_B = 1235

    server_A = ThreadedTCPServer((HOST, PORT_A), ThreadedTCPRequestHandler)
    server_B = ThreadedTCPServer((HOST, PORT_B), ThreadedTCPRequestHandler)

    server_A_thread = threading.Thread(target=server_A.serve_forever)
    server_B_thread = threading.Thread(target=server_B.serve_forever)

    server_A_thread.setDaemon(True)
    server_B_thread.setDaemon(True)

    server_A_thread.start()
    server_B_thread.start()

    while 1:
        time.sleep(1)
