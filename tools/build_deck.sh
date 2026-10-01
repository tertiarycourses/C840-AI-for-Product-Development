#!/bin/sh
# Rebuild the C840 deck from the WSQ source: convert_deck.py, then fix_deck.py.
set -e
cd "$(dirname "$0")/.."
OUT="courseware/AI for Product Development (C840)-v1.0.pptx"
python3 ~/.claude/skills/wsq-to-non-wsq/scripts/convert_deck.py \
  --src "source-wsq/courseware/PPT-Agentic AI for Product Development-v7.0.pptx" --out "$OUT" \
  --old-title "Agentic AI for Product Development" --new-title "AI for Product Development" \
  --old-code TGS-2024045799 --new-code C840 \
  --old-version v7.0 --new-version v1.0 \
  --old-duration "2 days / 16 hours" --new-duration "2 days / 15 hours" \
  --sub "https://github.com/tertiarycourses/TGS-2024045799-Agentic-AI-for-Product-Development=>https://github.com/tertiarycourses/C840-AI-for-Product-Development" \
  --sub "Duration: 2 days / 16 training hours=>Duration: 2 days / 15 instructional hours" \
  --sub "Version: v7.0 / 11 September 2026=>Version: v1.0 / 1 October 2026" \
  --sub "v7.0  •  11 September 2026=>v1.0  •  1 October 2026" \
  --wsq-slides 1,9,10,11,12,14,202,203
python3 tools/fix_deck.py
