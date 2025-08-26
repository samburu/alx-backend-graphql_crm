#!/bin/bash

# Navigate to the Django project root (adjust path if needed)
PROJECT_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"

# Run Django shell command to delete inactive customers
DELETED_COUNT=$(python3 $PROJECT_ROOT/manage.py shell -c "
import datetime
from crm.models import Customer

one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=one_year_ago)
count = qs.count()
qs.delete()
print(count)
")

# Log the result with timestamp
echo \"$(date '+%Y-%m-%d %H:%M:%S') - Deleted customers: $DELETED_COUNT\" >> /tmp/customer_cleanup_log.txt
