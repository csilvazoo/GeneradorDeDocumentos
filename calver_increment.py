import datetime
import re

def get_next_calver_increment():
    today = datetime.date.today().strftime('%Y.%m.%d')
    try:
        with open('VERSION', 'r') as f:
            version = f.read().strip()
        match = re.match(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
        if match:
            last_date, last_inc = match.groups()
            if last_date == today:
                return f"{today}-{int(last_inc)+1}"
        # Si la fecha cambió o no hay match
        return f"{today}-1"
    except Exception:
        return f"{today}-1"

def update_version_file():
    next_version = get_next_calver_increment()
    with open('VERSION', 'w') as f:
        f.write(next_version + '\n')
    return next_version

if __name__ == "__main__":
    v = update_version_file()
    print(f"Nueva versión: {v}")
