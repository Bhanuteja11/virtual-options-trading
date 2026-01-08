# Virtual Options Trading Platform (Paper Trading)

## Overview
A backend system that simulates options trading on NIFTY using
delayed index data and virtual capital.

## Features
- FastAPI-based REST APIs
- Virtual wallet with risk checks
- Options trade execution (paper trades)
- Market data abstraction
- P&L-ready architecture

## Tech Stack
- Python 3.11
- FastAPI
- Pydantic
- Uvicorn

## Key Design Decisions
- Delayed index data used due to exchange licensing constraints
- Option premiums simulated using pricing logic
- In-memory storage for speed and clarity

## Disclaimer
This project is for educational and demonstration purposes only.
No real trading is performed.
