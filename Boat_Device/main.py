from mqtt.client import Client


def main():
    broker = "mqtt.yourbroker.com"
    
    client = Client()
    client.connect(broker)

    # client.instance.stop_loop()
    


if __name__ == "__main__":
    main()
