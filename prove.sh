#!/bin/bash

gnome-terminal -- bash -c "python3 verifier.py; sleep 1; exit"

gnome-terminal -- bash -c "python3 prover.py; sleep 1; exit"
