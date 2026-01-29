#!/bin/bash
cd /Users/arthelper/services/podcast-pipeline
export DEEPGRAM_API_KEY="e774124fe5e10632834c3406eae7a5921a25e782"
export OPENAI_API_KEY="sk-proj-6gH7n3Q6Yc6K1aL8m2N0w5b7G4d3F2h9J5k1L8m2N0w5b7G4d3F2h9J5k"
python3 ingest.py --source lennys-podcast --limit 1
