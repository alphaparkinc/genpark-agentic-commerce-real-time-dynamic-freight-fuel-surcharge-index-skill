# -*- coding: utf-8 -*-
"""MCP Server for Dynamic Freight Fuel Surcharge (FSC) DOE Indexer Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import FreightFuelSurchargeIndexer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_baseline_fsc_percentage",
        "description": "Compute contract fuel surcharge percentage from weekly DOE On-Highway Diesel price index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_doe_diesel_price_per_gal": {
                    "type": "number"
                },
                "baseline_diesel_peg": {
                    "type": "number"
                },
                "fsc_step_cents": {
                    "type": "number"
                },
                "fsc_step_pct": {
                    "type": "number"
                }
            },
            "required": [
                "current_doe_diesel_price_per_gal"
            ]
        }
    },
    {
        "name": "audit_carrier_invoice_fsc_overcharge",
        "description": "Audit billed freight invoice FSC against official index date to flag carrier margin padding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "billed_fsc_usd": {
                    "type": "number"
                },
                "linehaul_charge_usd": {
                    "type": "number"
                },
                "expected_fsc_pct": {
                    "type": "number"
                }
            },
            "required": [
                "billed_fsc_usd",
                "linehaul_charge_usd",
                "expected_fsc_pct"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-real-time-dynamic-freight-fuel-surcharge-index-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(FreightFuelSurchargeIndexer, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-real-time-dynamic-freight-fuel-surcharge-index-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
