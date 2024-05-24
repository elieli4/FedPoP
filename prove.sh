#!/bin/bash

gnome-terminal -- bash -c "python3 verifier.py; sleep 10; exit"

gnome-terminal -- bash -c "python3 prover.py; sleep 10; exit"
