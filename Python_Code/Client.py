




def validation_handler(unused_addr, args, msg):
    print("[{0}] ~ {1}".format(args[0], msg))
    print(unused_addr)
    return

def load_handler(unused_addr, args, msg):
    print("[{0}] ~ {1}".format(args[0], msg))
    print(unused_addr)
    return

if __name__ == "__main__":
    mi_app = Aplicacion()
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/songid", load_handler, "Save")
    dispatcher.map("/validation", validation_handler, "Ready")

    server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 5006), dispatcher)
    print("ServerOSC-FRONT in Client Ready on {}".format(server.server_address))
    server.serve_forever()

