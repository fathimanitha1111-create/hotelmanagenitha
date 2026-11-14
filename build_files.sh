#!/bin/bash
echo '=== Installing dependencies ==='
python3 -m pip install -r requirements.txt

echo '=== Collecting static files ==='
python3 manage.py collectstatic --noinput --clear

echo '=== Ensuring static mirror for Vercel ==='
mkdir -p staticfiles/static
cp -r staticfiles/hotel_app staticfiles/static/ 2>/dev/null || true
cp -r staticfiles/admin staticfiles/static/ 2>/dev/null || true

echo '=== Build Complete ==='
