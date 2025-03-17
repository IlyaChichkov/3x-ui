#!/bin/bash

AUTOSTART_FILE="/app/x-ui/autostart"

if [[ -f "$AUTOSTART_FILE" && $(cat "$AUTOSTART_FILE") == "1" ]]; then
    echo "Autostart is enabled. Starting /app/x-ui/x-ui..."
    /app/x-ui/x-ui
else
    echo "Autostart is disabled. Skipping /app/x-ui/x-ui startup."
fi