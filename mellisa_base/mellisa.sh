#!/bin/bash

SCRIPT_PATH="$(readlink -f "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

PROJECT_ROOT="$(realpath "$SCRIPT_DIR/..")"  
PYTHON_SCRIPT="$PROJECT_ROOT/mellisa_base/mellisa.py"
FLAG_FILE="$SCRIPT_DIR/.first_run_flag"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

if [ ! -f "$FLAG_FILE" ]; then
    touch "$FLAG_FILE"
    python3 -c "import ascii.description_ascii; print(ascii.description_ascii.mellisa_ascii)"
fi

(
    TERM_PID=$(ps -o ppid= -p $$)
    
    exec </dev/null >/dev/null 2>&1
    
    while ps -p $TERM_PID > /dev/null 2>&1; do
        sleep 1
    done
    
    rm -f "$FLAG_FILE"
) &

MONITOR_PID=$!
disown $MONITOR_PID

export PYTHONPATH="$PROJECT_ROOT"

# Run the Python script
python "$PYTHON_SCRIPT" "@"

exit 0