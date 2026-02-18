# Distributed Async-Await Testbed (Resonate Multi-Server)

## Quick Start

```bash
docker-compose up
python worker1.py &
python worker2.py &
python client.py
```

## Test Scenarios

### Baseline (no faults)
- All components healthy
- Measure: end-to-end latency, throughput
- Expected: jobs complete in ~20s

### Fault injection
- Server crash / recovery
- Network partition
- Worker restart during execution

## Metrics

Access Grafana at `http://localhost:3000` to visualize:
- Task completion times per server
- Durable promise state transitions
- Worker polling frequency

