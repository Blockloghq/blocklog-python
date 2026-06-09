# Blocklog Python SDK

**Infrastructure for AI Decision-Making.**

Record every decision your AI agents make.

[![PyPI version](https://img.shields.io/pypi/v/blocklog.svg)](https://pypi.org/project/blocklog/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## Installation

```bash
pip install blocklog
```

---

## Quick Start: Time to First Trace

The Blocklog SDK is designed around a simple, powerful workflow: **Initialize, Trace, Tool, and Decide.**

### 1. Initialize

Configure the SDK once at startup.

```python
import blocklog

blocklog.init(api_key="blk_...")
```

### 2. Tool

Record every tool call automatically.

```python
@blocklog.tool
def fetch_price(ticker: str) -> float:
    # Tool inputs and outputs will be captured automatically
    return 412.50
```

### 3. Agent

Trace your agent's full execution lifecycle.

```python
@blocklog.agent(name="stock-trader")
def run_agent():
    price = fetch_price("TSLA")
    
    # Next step: record the decision
```

### 4. Decision

Record the AI decision with its inputs and outputs. This is the core of Blocklog.

```python
    with blocklog.decision(type="BUY", asset="TSLA") as d:
        d.record_input(price=price)
        
        # ... logic to place order ...
        
        d.record_output(order_id="ord_123")
```

---

## Next Steps

Once you've recorded your first decision, explore the advanced governance and investigation features of Blocklog:

- [Governance & Investigation Docs](https://docs.blocklog.dev) — Learn how to set up Human-in-the-Loop approvals and run Forensic Replays.
- [Advanced Features](https://docs.blocklog.dev/advanced) — Learn about incident management, compliance reports, and cryptographic verification.

### Examples

Check out the `examples/` directory in the repository for full, runnable code:

1. `01_quickstart.py`
2. `02_stock_trading_agent.py`
3. `03_multi_agent_workflow.py`
4. `advanced/` — Advanced use-cases like incidents, compliance, and replays.

---

## License

[See LICENSE](../LICENSE)
