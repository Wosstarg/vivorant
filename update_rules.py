import sqlite3
from pathlib import Path

# ================= НАСТРОЙКИ =================
DB_PATH = r"C:\ProgramData\Locktime\NetLimiter\5\Stats\nlstats.db"  # ← измени, если путь другой
OUTPUT_DIR = Path(r"C:\Users\Wosstarg\Documents\GitHub\vivorant\rule-sets")
# ============================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

domains = set()
ips = set()

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

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_DIR / "vivox_valorant.txt", "w", encoding="utf-8") as f:
    f.write("# Valorant + Vivox rules from Netlimiter\n\n")
    for d in sorted(domains):
        f.write(f"domain:{d}\n")
    for ip in sorted(ips):
        f.write(f"ipcidr:{ip}/32\n")

print(f"Файл успешно сохранён в:\n{OUTPUT_DIR / 'vivox_valorant.txt'}")