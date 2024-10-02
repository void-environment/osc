"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client
import yaml

def load_config(file_path = "config.yaml"):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
  config = load_config()

  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=config["Port"],
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)

  for x in range(10):
    client.send_message("/health", random.random())
    time.sleep(1)