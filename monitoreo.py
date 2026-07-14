import json
import platform
import subprocess
import urllib.request
import psutil

# 🟢 PON TU URL AQUÍ (DENTRO DE LAS COMILLAS)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1523763026250174596/IXOPrPa7puGg_sec6UmBLWpFelzcpb1WpoywGHocmCYeaB4404wFpQWI4JLwRxiHU7zN"


def enviar_alerta_discord(mensaje):
    """Envía un texto al canal de Discord usando el Webhook configurado."""
    datos = {"content": mensaje}
    payload = json.dumps(datos).encode("utf-8")
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    try:
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL, data=payload, headers=headers
        )
        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("📢 ¡Alerta enviada con éxito a Discord!")
    except Exception as e:
        print(f"❌ Falló el envío a Discord: {e}")


def verificar_ping(ip):
    """Hace un ping a una IP con un tiempo límite."""
    if platform.system().lower() == "windows":
        comando = ["ping", "-n", "1", "-w", "1500", ip]
    else:
        comando = ["ping", "-c", "1", "-W", "2", ip]
    try:
        resultado = subprocess.run(
            comando, capture_output=True, text=True, timeout=3
        )
        return "TTL=" in resultado.stdout.upper()
    except Exception:
        return False


def obtener_salud_sistema():
    """Recupera el uso actual de CPU y memoria RAM."""
    try:
        uso_cpu = psutil.cpu_percent(interval=0.5)
        memoria = psutil.virtual_memory()
        uso_ram = memoria.percent
        return uso_cpu, uso_ram
    except Exception:
        return 0, 0


if __name__ == "__main__":
    dispositivos = ["8.8.8.8", "1.1.1.1", "10.0.0.99"]

    reporte_discord = "📊 **REPORTE AUTOMÁTICO DE INFRAESTRUCTURA** 📊\n\n"
    reporte_discord += "🖥️ **Estado de Red:**\n"

    print("=== INICIANDO MONITOREO ===")

    for ip in dispositivos:
        print(f"Verificando {ip}...")
        if verificar_ping(ip):
            reporte_discord += f"• `{ip}` -> 🟢 ONLINE\n"
        else:
            reporte_discord += f"• `{ip}` -> 🔴 OFFLINE / INACCESIBLE\n"

    cpu, ram = obtener_salud_sistema()
    reporte_discord += f"\n⚙️ **Estado del Servidor Local:**\n"
    reporte_discord += f"• Uso de CPU: `{cpu}%`\n"
    reporte_discord += f"• Uso de RAM: `{ram}%`\n"

    if cpu > 80 or ram > 85:
        reporte_discord += "\n🚨 **¡ALERTAS DE SISTEMA CRÍTICAS!** 🚨\n"
        if cpu > 80:
            reporte_discord += "⚠️ `CPU` superó el umbral del 80%\n"
        if ram > 85:
            reporte_discord += "⚠️ `RAM` superó el umbral del 85%\n"

    print("Enviando reporte consolidado...")
    enviar_alerta_discord(reporte_discord)
    print("==========================")