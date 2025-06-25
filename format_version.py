# Script para formatear el archivo VERSION a YY.MM.DD.N
import re

with open('VERSION', 'r') as f:
    version = f.read().strip()

m = re.match(r"(\d{4})(\d{2})(\d{2})\.(\d+)", version)
if m:
    formatted = f"{m.group(1)[2:]}.{m.group(2)}.{m.group(3)}.{m.group(4)}"
    with open('VERSION', 'w') as f:
        f.write(formatted + '\n')
