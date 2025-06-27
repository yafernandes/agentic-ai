#!/usr/bin/env python3
"""
Demo script to run the weather agent interactively.
"""
import asyncio

import main_agent

if __name__ == "__main__":
    print("Agentic AI Client")
    print("=" * 20)
    asyncio.run(main_agent.main())