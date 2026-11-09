"""Download the TSPLIB (Problem 1) and OR-Library (Problem 2) datasets.

Run from the repository root:  python scripts/download_data.py
"""
import gzip
import urllib.request
from pathlib import Path
import ssl

ROOT = Path(__file__).resolve().parent.parent
TSP_DIR = ROOT / "problem1" / "data" / "tsplib"
PORT_DIR = ROOT / "problem2" / "data" / "orlib"

###TSP_URL = "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/{}.tsp.gz"
TSP_URL = "https://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/{}.tsp.gz"
PORT_URL = "https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{}.txt"
UNVERIFIED_HOSTS = ("comopt.ifi.uni-heidelberg.de",)

# instance name -> number of cities / assets stated in the assignment
TSP_INSTANCES = {"eil51": 51, "berlin52": 52, "st70": 70, "eil76": 76, "kroA100": 100, "ch150": 150}
PORT_FILES = {"port1": 31, "port2": 85, "port3": 89, "port4": 98, "port5": 225}


def fetch(url):
    context = None
    if any(host in url for host in UNVERIFIED_HOSTS):
        context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, timeout=60, context=context) as response:
        return response.read()


def main():
    TSP_DIR.mkdir(parents=True, exist_ok=True)
    PORT_DIR.mkdir(parents=True, exist_ok=True)

    for name, n in TSP_INSTANCES.items():
        data = gzip.decompress(fetch(TSP_URL.format(name)))
        lines = data.decode().splitlines()
        header = {k.strip(): v.strip() for k, v in (l.split(":", 1) for l in lines if ":" in l)}
        assert header["TYPE"] == "TSP", name
        assert header["EDGE_WEIGHT_TYPE"] == "EUC_2D", name
        assert int(header["DIMENSION"]) == n, name
        (TSP_DIR / f"{name}.tsp").write_bytes(data)
        print(f"OK  {name}.tsp  ({n} cities)")

    for name, n in PORT_FILES.items():
        data = fetch(PORT_URL.format(name))
        lines = [l for l in data.decode().splitlines() if l.strip()]
        assert int(lines[0]) == n, name
        assert len(lines) == 1 + n + n * (n + 1) // 2, name  # header + assets + correlation records
        (PORT_DIR / f"{name}.txt").write_bytes(data)
        print(f"OK  {name}.txt  ({n} assets)")


if __name__ == "__main__":
    main()