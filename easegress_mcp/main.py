import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import server

if __name__ == "__main__":
    server.run()
