import argparse
import signal
import sys
from acars2sbs.main import Main
from acars2sbs.console import Console

MAIN = None

def sig_handler(sig, frame):
    MAIN.shutdown()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Converte mensagens ACARS em SBS.")
    parser.add_argument("input", help="[ip:]porta (UDP) onde receber as mensagens ACARS (inclua o IP caso queira receber somente em um IP específico do host local)")
    parser.add_argument("output", help="host:porta (TCP) para onde enviar as mensagens convertidas")
    parser.add_argument("-f", "--forward", metavar="HOST:PORT", help="host:porta (UDP) para onde enviar uma cópia das mensagens ACARS")
    args = parser.parse_args()

    parts = args.input.split(":")
    if len(parts) == 1:
        (srchost, srcport) = ("", int(parts[0]))
    else:
        (srchost, srcport) = (parts[0], int(parts[1]))

    parts = args.output.split(":")
    (dsthost, dstport) = (parts[0], int(parts[1]))

    if args.forward:
        parts = args.forward.split(":")
        (fwhost, fwport) = (parts[0], int(parts[1]))
    else:
        fwhost = fwport = None

    return (srchost, srcport, dsthost, dstport, fwhost, fwport)

def main():
    (srchost, srcport, dsthost, dstport, fwhost, fwport) = parse_args()
    console = Console()
    global MAIN
    MAIN = Main(console, srchost, srcport, dsthost, dstport, fwhost, fwport)
    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    MAIN.start()
    MAIN.join()

if __name__ == "__main__":
    main()
