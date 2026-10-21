# Dynamic Freight Fuel Surcharge (FSC) DOE Indexer Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

EIA/DOE weekly diesel fuel price indexing, dynamic LTL/FTL linehaul fuel surcharge (FSC) calculation, and carrier overbill audit. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_baseline_fsc_percentage`: Compute contract fuel surcharge percentage from weekly DOE On-Highway Diesel price index.
- `audit_carrier_invoice_fsc_overcharge`: Audit billed freight invoice FSC against official index date to flag carrier margin padding.

## 🚀 Installation & Usage
```bash
python -m genpark_agentic_commerce_real_time_dynamic_freight_fuel_surcharge_index_skill.server --test
```
