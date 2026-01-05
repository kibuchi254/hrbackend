#!/bin/bash

# HR & Payroll SaaS API - Startup Script
# This script starts the FastAPI backend server

# Get the directory where this script is located
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  HR & Payroll SaaS API${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "$BACKEND_DIR/venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run: python3 -m venv venv${NC}"
    exit 1
fi

# Check if database exists
if [ ! -f "$BACKEND_DIR/hr_payroll.db" ]; then
    echo -e "${YELLOW}Database not found. Initializing...${NC}"
    "$BACKEND_DIR/venv/bin/python3" "$BACKEND_DIR/init_db.py"
    echo ""
fi

# Kill any existing server processes
echo -e "${YELLOW}Stopping any existing servers...${NC}"
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 2

# Start the server
echo -e "${GREEN}Starting FastAPI server...${NC}"
echo -e "${YELLOW}Server will run on: http://localhost:8000${NC}"
echo -e "${YELLOW}API Documentation: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start server in background with logging
cd "$BACKEND_DIR"
nohup "$BACKEND_DIR/venv/bin/python3" -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    > /tmp/hr-api.log 2>&1 &

# Save PID for later cleanup
echo $! > /tmp/hr-api.pid

# Wait a moment for server to start
sleep 3

# Check if server started successfully
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully!${NC}"
    echo -e "${GREEN}✓ Health check: http://localhost:8000/health${NC}"
    echo -e "${GREEN}✓ API Docs: http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${YELLOW}View logs: tail -f /tmp/hr-api.log${NC}"
    echo -e "${YELLOW}Stop server: kill \$(cat /tmp/hr-api.pid)${NC}"
    echo ""
    tail -f /tmp/hr-api.log
else
    echo -e "${RED}✗ Failed to start server${NC}"
    echo -e "${YELLOW}Check logs: cat /tmp/hr-api.log${NC}"
    exit 1
fi
