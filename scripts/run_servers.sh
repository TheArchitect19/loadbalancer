
---

### `scripts/run_servers.sh`
This script runs multiple backend servers on different ports in the background.

```bash
#!/bin/bash

# Run backend servers on different ports
python3 backend_server.py 8000 &
python3 backend_server.py 8001 &
python3 backend_server.py 8002 &

echo "Backend servers are running on ports 8000, 8001, and 8002."
