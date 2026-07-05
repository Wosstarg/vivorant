import sqlite3
from pathlib import Path

# ================= НАСТРОЙКИ =================
DB_PATH = r"C:\ProgramData\Locktime\NetLimiter\5\Stats\nlstats.db"  # ← проверь путь!
OUTPUT_DIR = Path("rule-sets")
FILENAME = "vivox_valorant.mrs"
# ============================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

ips = set()
domains = set()

print("Извлекаем данные Valorant...")

cursor.execute("""
    SELECT DISTINCT i.DomName, i.Ip
    FROM Cnns c
    JOIN IpsV4 i ON c.RemoteIpId = i.Ip
    JOIN Apps a ON c.AppId = a.Id
    WHERE a.Path LIKE '%VALORANT-Win64-Shipping.exe%'
""")

for dom, ip_int in cursor.fetchall():
    if dom and dom != "None":
        domains.add(dom)
    if ip_int:
        ip = f"{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}"
        ips.add(ip)

conn.close()

print(f"Доменов: {len(domains)} | IP: {len(ips)}")

OUTPUT_DIR.mkdir(exist_ok=True)

# Создаём .mrs файл
with open(OUTPUT_DIR / FILENAME, "w", encoding="utf-8") as f:
    f.write("payload:\n")
    
    # Сначала IP (как ты показал)
    for ip in sorted(ips):
        f.write(f"  - '{ip}/32'\n")
    
    # Потом домены (для domain behavior)
    for d in sorted(domains):
        f.write(f"  - 'domain:{d}'\n")

print(f"Файл создан: {OUTPUT_DIR / FILENAME}")