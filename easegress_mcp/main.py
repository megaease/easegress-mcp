import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easegress_mcp import server

if __name__ == "__main__":
    server.run()
