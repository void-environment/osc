import webview
import os
import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
import socket
import yaml
import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("Python.Runtime")

global_window = None

def load_config(file_path="config.yaml"):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def send_to_js(point, args=None, ip=None):
    if ip:
        global_window.evaluate_js(f"getIP('{ip}')")
    
    global_window.evaluate_js(f"point('{point}')")
    global_window.evaluate_js(f"args(\"{args}\")")

    if point == '/button':
        global_window.evaluate_js(f"{args}()")
    elif point == '/start':
        global_window.evaluate_js(f"rfid('{args}')")
    elif point == '/stop':
        global_window.evaluate_js(f"rfid('{args}')")

def js_api_close_app():
    print("Close App")
    os._exit(0)

def handle_any_request(address, *args):
    clean_args = ' '.join(map(str, args))
    print(f"request at: {address} args: {clean_args}")
    send_to_js(address, clean_args)

def handle_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print("HostName:", s.getsockname()[0])
    send_to_js("", "", s.getsockname()[0])

def start_osc_server():
    config = load_config()
    dispatcher = Dispatcher()
    dispatcher.map("*", handle_any_request)

    server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", config['Port']), dispatcher)
    print(f"Serving on {server.server_address}")
    handle_ip()
    server.serve_forever()

def start_webview():
    global global_window
    global_window = webview.create_window(
        'Test App',
        'template/index.html',
        js_api={"closeApp": js_api_close_app},
        on_top=True,
        # fullscreen=True,
        confirm_close=False
    )
    webview.start()

if __name__ == '__main__':
    osc_thread = threading.Thread(target=start_osc_server)
    osc_thread.daemon = True
    osc_thread.start()
    start_webview()
