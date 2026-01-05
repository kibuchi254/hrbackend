#!/bin/bash

# HR & Payroll SaaS API - Stop Script

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping HR & Payroll API server...${NC}"

# Kill any existing server processes
pkill -f "uvicorn app.main:app"

# Wait for process to stop
sleep 2

# Verify server is stopped
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "\033[0;31m✗ Failed to stop server\033[0m"
    exit 1
else
    echo -e "${GREEN}✓ Server stopped successfully!${NC}"
fi

# Clean up PID file
rm -f /tmp/hr-api.pid
