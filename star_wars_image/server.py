import threading
import time
import SocketServer
import json
import pygame

started = False
playing = False
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global started
        global playing
        self.data = self.request.recv(1024).strip()
        print "%s wrote: " % self.client_address[0]
        print self.data
        reading = json.loads(self.data)

        if "sensor" in reading and "value" in reading:
            if reading["sensor"] == "GroveButton" and reading["value"] == 1 and not playing:
                if not started:
                    pygame.mixer.music.play("/src/starwars.wav")
                    started = True
                else:
                    pygame.mixer.music.unpause()
                playing = True
            elif reading["sensor"] == "GroveButton" and reading["value"] == 0 and playing:
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
