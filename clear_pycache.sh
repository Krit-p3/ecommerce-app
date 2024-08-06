#!/bin/bash 

find src -type d -name '__pycache__' -print -exec rm -rf {} +


echo "Cleared all __pycache__ success."
