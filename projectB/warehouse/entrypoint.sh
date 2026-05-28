#!/bin/bash

set -e

echo "Starting Warehouse"

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput

# Restore from dump if requested (after migrations)
if [ "$RESTORE_DUMP" = "true" ] || [ "$RESTORE_DUMP" = "1" ]; then

    if [ -f "$DUMP_FILE" ]; then
        echo "Found dump file: $DUMP_FILE"
        echo "Restoring data from dump..."

        python manage.py loaddata "$DUMP_FILE"

        echo "Dump successfully loaded"
    else
        echo "RESTORE_DUMP=true but no dump found at: $DUMP_FILE"
    fi
else
    echo "Restore dump skipped"
fi

echo "Creating groups..."

python manage.py create_groups || true

echo "Warehouse ready!"

exec "$@"
