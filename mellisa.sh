#!/bin/bash

SCRIPT_DIR="$(dirname "$(realpath "$0")")"
PYTHON_SCRIPT="$SCRIPT_DIR/mellisa/mellisa.py"
FLAG_FILE="$SCRIPT_DIR/.first_run_flag"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

if [ ! -f "$FLAG_FILE" ]; then
    touch "$FLAG_FILE"
    python3 -c "from mellisa.ascii.description_ascii import mellisa_ascii; print(mellisa_ascii)"
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

# Run the Python script
python "$PYTHON_SCRIPT" "$@"

exit 0
