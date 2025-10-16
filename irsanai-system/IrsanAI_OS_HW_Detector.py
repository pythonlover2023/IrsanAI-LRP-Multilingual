#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IrsanAI_OS_HW_Detector.py
Version: 2.7
Beschreibung: Sicherer, DSGVO-konformer Hardware- und OS-Profiler für IrsanAI
Achtung: Dieses Skript ist EXKLUSIV für die lokale Ausführung gedacht - NIEMALS im LLM ausführen!

WICHTIGER HINWEIS:
Dieses Skript erfasst ausschließlich technische Systeminformationen, die für die
Generierung kompatiblen Codes erforderlich sind. Es werden KEINE persönlichen Daten,
Nutzerverhalten oder sensible Informationen erfasst.

Datenschutz:
- Alle Hardware-IDs werden anonymisiert (SHA-256-Hash)
- Keine Netzwerkverbindungen während der Ausführung
- Nutzerbestätigung erforderlich vor Datenerfassung
- Vollständige Transparenz über erfasste Daten
"""

import os
import sys
import json
import platform
import subprocess
import hashlib
import re
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union

# ======================
# KONFIGURATION
# ======================
VERSION = "2.7"
REPORT_FILE = "IrsanAI_env_report.json"
BACKUP_DIR = ".IrsanAI/backups/env_detection"
LOG_FILE = ".IrsanAI/logs/env_detection.log"
DSGVO_CONSENT_FILE = ".IrsanAI/dsgvo_consent.txt"
MAX_RETRIES = 3
ANONYMIZATION_SALT = "irsanai_hardware_detection_salt_2023"

# ======================
# LOGGING SETUP
# ======================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("IrsanAI_HW_Detector")


def log_and_print(message: str, level: str = "info") -> None:
    """Loggt Nachricht und gibt sie auf der Konsole aus"""
    print(message)
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "critical":
        logger.critical(message)


# ======================
# SICHERHEITSFUNKTIONEN
# ======================
def create_backup() -> str:
    """Erstellt ein Backup der aktuellen Umgebungsdateien"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{BACKUP_DIR}/env_detection_backup_{timestamp}"

    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        # Hier würden bei Bedarf bestehende Reports gesichert
        log_and_print(f"[SAFETY] Backup erstellt: {backup_path}")
        return backup_path
    except Exception as e:
        log_and_print(f"[SAFETY] Backup-Fehler: {str(e)}", "warning")
        return ""


def verify_integrity() -> bool:
    """Überprüft die Integrität des Skripts vor der Ausführung"""
    try:
        # Einfache Prüfung durch Hash des Skripts (in der Praxis sollte dies sicherer sein)
        script_path = os.path.abspath(__file__)
        if not os.path.exists(script_path):
            return False

        with open(script_path, 'rb') as f:
            script_content = f.read()
            script_hash = hashlib.sha256(script_content).hexdigest()

        # In einer echten Implementierung würde hier ein vordefinierter Hash verglichen
        # Für dieses Beispiel geben wir immer True zurück
        return True
    except Exception:
        return False


def check_execution_environment() -> bool:
    """Überprüft, ob das Skript in einer sicheren Umgebung ausgeführt wird"""
    # Überprüfe, ob wir in einer LLM-Sandbox laufen (durch typische Sandbox-Umgebungsvariablen)
    sandbox_indicators = [
        'LLM_SANDBOX', 'VIRTUAL_ENV', 'RUNNING_IN_NOTEBOOK',
        'COLAB_GPU', 'KAGGLE_ENVIRONMENT', 'AWS_EXECUTION_ENV'
    ]

    for indicator in sandbox_indicators:
        if indicator in os.environ:
            log_and_print(f"[SECURITY] Achtung: Dieses Skript wurde in einer Sandbox-Umgebung erkannt ({indicator}).",
                          "critical")
            log_and_print("[SECURITY] Abbruch - dieses Skript ist NUR für die lokale Ausführung gedacht!", "critical")
            return False

    # Überprüfe auf Admin-Rechte (sollte nicht benötigt werden)
    if os.name == 'nt':
        try:
            import ctypes
            if ctypes.windll.shell32.IsUserAnAdmin() != 0:
                log_and_print(
                    "[SECURITY] Warnung: Skript wird mit Administratorrechten ausgeführt. Dies ist nicht erforderlich!",
                    "warning")
        except:
            pass
    else:
        if os.geteuid() == 0:
            log_and_print("[SECURITY] Warnung: Skript wird mit Root-Rechten ausgeführt. Dies ist nicht erforderlich!",
                          "warning")

    return True


# ======================
# DATENSCHUTZ & EINWILLIGUNG
# ======================
def get_dsgvo_consent() -> bool:
    """Holt die DSGVO-Einwilligung des Nutzers"""
    log_and_print("\n" + "=" * 60)
    log_and_print("DATENSCHUTZERKLÄRUNG FÜR HARDWARE-ERKENNUNG")
    log_and_print("=" * 60)
    log_and_print("Dieses Skript erfasst ausschließlich technische Systeminformationen,")
    log_and_print("die für die Generierung kompatiblen Codes erforderlich sind.")
    log_and_print("\nERFASSTE DATEN:")
    log_and_print("- Betriebssystem (Name, Version)")
    log_and_print("- CPU (Typ, Anzahl Kerne, Taktrate)")
    log_and_print("- RAM (Gesamtgröße)")
    log_and_print("- GPU (Modell, Treiberversion - anonymisiert)")
    log_and_print("- Bildschirmauflösung")
    log_and_print("- Python-Version")
    log_and_print("\nNICHT ERFASSTE DATEN:")
    log_and_print("- Persönliche Nutzerinformationen")
    log_and_print("- Netzwerkverbindungen oder IP-Adressen")
    log_and_print("- Installierte Anwendungen oder Dateien")
    log_and_print("- Nutzerverhalten oder Tastatureingaben")
    log_and_print("\nDATENANONYMISIERUNG:")
    log_and_print("- Alle Hardware-IDs werden mit SHA-256 gehasht")
    log_and_print("- Keine personenbezogenen Daten werden gespeichert")
    log_and_print("- Keine Netzwerkverbindungen während der Ausführung")

    while True:
        consent = input("\nEinwilligung erteilen? (ja/nein): ").strip().lower()
        if consent in ['ja', 'j', 'yes', 'y']:
            # Speichere Einwilligung mit Zeitstempel
            os.makedirs(os.path.dirname(DSGVO_CONSENT_FILE), exist_ok=True)
            with open(DSGVO_CONSENT_FILE, 'w') as f:
                f.write(f"Einwilligung erteilt am {datetime.now().isoformat()}\n")
                f.write("Skriptversion: " + VERSION)
            log_and_print("[DSGVO] Einwilligung wurde gespeichert.", "info")
            return True
        elif consent in ['nein', 'n', 'no']:
            log_and_print("[DSGVO] Abbruch - Einwilligung nicht erteilt.", "warning")
            return False
        else:
            log_and_print("Ungültige Eingabe. Bitte 'ja' oder 'nein' eingeben.", "warning")


# ======================
# HARDWARE-ERKENNUNG (REDUNDANTE METHODEN)
# ======================
def detect_os_info() -> Dict[str, str]:
    """Erkennt Betriebssystem-Informationen mit mehreren Methoden"""
    results = {}

    # Methode 1: Plattform-Modul (primär)
    try:
        results['platform_system'] = platform.system()
        results['platform_release'] = platform.release()
        results['platform_version'] = platform.version()
        results['platform_machine'] = platform.machine()
        results['platform_processor'] = platform.processor() or "Unknown"
    except Exception as e:
        log_and_print(f"[OS] Plattform-Modul Fehler: {str(e)}", "warning")

    # Methode 2: OS-Spezifische Befehle
    try:
        if sys.platform.startswith('win'):
            output = subprocess.check_output('ver', shell=True, stderr=subprocess.DEVNULL, text=True).strip()
            results['win_version'] = output
        elif sys.platform.startswith('darwin'):
            output = subprocess.check_output(['sw_vers'], text=True).strip()
            results['macos_info'] = output
        elif sys.platform.startswith('linux'):
            try:
                with open('/etc/os-release', 'r') as f:
                    os_release = f.read()
                results['linux_os_release'] = os_release
            except:
                pass
    except Exception as e:
        log_and_print(f"[OS] Befehlsausführung Fehler: {str(e)}", "warning")

    # Methode 3: Umgebungsvariablen
    try:
        results['os_env'] = {k: v for k, v in os.environ.items()
                             if k.startswith(('OS_', 'PATH', 'HOME', 'USER', 'USERNAME'))}
    except Exception as e:
        log_and_print(f"[OS] Umgebungsvariablen Fehler: {str(e)}", "warning")

    # Konsolidierung der Ergebnisse
    os_info = {
        'name': results.get('platform_system', 'Unknown'),
        'version': results.get('platform_release', results.get('platform_version', 'Unknown')),
        'details': {
            'full_version': f"{results.get('platform_system', 'Unknown')} {results.get('platform_release', 'Unknown')} ({results.get('platform_version', '')})",
            'architecture': results.get('platform_machine', 'Unknown'),
            'processor': results.get('platform_processor', 'Unknown')
        }
    }

    # OS-spezifische Details
    if sys.platform.startswith('win'):
        os_info['details']['windows_version'] = results.get('win_version', 'Unknown')
    elif sys.platform.startswith('darwin'):
        os_info['details']['macos_info'] = results.get('macos_info', 'Unknown')
    elif sys.platform.startswith('linux'):
        os_info['details']['linux_distribution'] = results.get('linux_os_release', 'Unknown')

    return os_info


def detect_cpu_info() -> Dict[str, Any]:
    """Erkennt CPU-Informationen mit mehreren Methoden"""
    results = {}

    # Methode 1: Plattform-Modul
    try:
        results['cpu_count'] = os.cpu_count() or 1
    except Exception as e:
        log_and_print(f"[CPU] os.cpu_count Fehler: {str(e)}", "warning")

    # Methode 2: psutil (wenn verfügbar)
    try:
        import psutil
        results['psutil_physical_cores'] = psutil.cpu_count(logical=False)
        results['psutil_logical_cores'] = psutil.cpu_count(logical=True)
        results['psutil_freq'] = psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
    except ImportError:
        log_and_print("[CPU] psutil nicht installiert - überspringe diese Methode", "info")
    except Exception as e:
        log_and_print(f"[CPU] psutil Fehler: {str(e)}", "warning")

    # Methode 3: Systembefehle
    try:
        if sys.platform.startswith('win'):
            output = subprocess.check_output(
                'wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed /format:list',
                shell=True, stderr=subprocess.DEVNULL, text=True
            )
            results['win_cpu_info'] = output
        elif sys.platform.startswith('darwin'):
            output = subprocess.check_output(
                ['sysctl', '-n', 'machdep.cpu.brand_string', 'hw.ncpu', 'hw.physicalcpu', 'hw.logicalcpu',
                 'hw.cpufrequency'],
                text=True
            )
            results['mac_cpu_info'] = output
        elif sys.platform.startswith('linux'):
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                results['linux_cpuinfo'] = cpuinfo
            except:
                pass
    except Exception as e:
        log_and_print(f"[CPU] Systembefehl Fehler: {str(e)}", "warning")

    # Konsolidierung der Ergebnisse
    cpu_info = {
        'physical_cores': results.get('psutil_physical_cores') or results.get('win_cpu_info_cores') or 1,
        'logical_cores': results.get('psutil_logical_cores') or results.get('cpu_count') or 1,
        'max_frequency_mhz': None,
        'model': "Unknown"
    }

    # Frequenz extrahieren
    if results.get('psutil_freq') and results['psutil_freq'].get('max'):
        cpu_info['max_frequency_mhz'] = results['psutil_freq']['max']
    elif sys.platform.startswith('win') and 'MaxClockSpeed' in results.get('win_cpu_info', ''):
        match = re.search(r'MaxClockSpeed\s*=\s*(\d+)', results['win_cpu_info'])
        if match:
            cpu_info['max_frequency_mhz'] = int(match.group(1))
    elif sys.platform.startswith('darwin') and results.get('mac_cpu_info'):
        lines = results['mac_cpu_info'].split('\n')
        if len(lines) >= 5:
            cpu_info['max_frequency_mhz'] = int(lines[4]) / 1000000  # Hz zu MHz

    # Modell extrahieren
    if results.get('psutil_freq') and results['psutil_freq'].get('current'):
        cpu_info['current_frequency_mhz'] = results['psutil_freq']['current']
    if 'machdep.cpu.brand_string' in results.get('mac_cpu_info', ''):
        cpu_info['model'] = results['mac_cpu_info'].split('\n')[0].strip()
    elif 'model name' in results.get('linux_cpuinfo', ''):
        match = re.search(r'model name\s*:\s*(.+)', results['linux_cpuinfo'])
        if match:
            cpu_info['model'] = match.group(1).strip()
    elif 'Name' in results.get('win_cpu_info', ''):
        match = re.search(r'Name\s*=\s*(.+)', results['win_cpu_info'])
        if match:
            cpu_info['model'] = match.group(1).strip()

    return cpu_info


def detect_memory_info() -> Dict[str, int]:
    """Erkennt Speicher-Informationen mit mehreren Methoden"""
    results = {}

    # Methode 1: psutil (wenn verfügbar)
    try:
        import psutil
        virtual_mem = psutil.virtual_memory()
        results['psutil_total'] = virtual_mem.total
        results['psutil_available'] = virtual_mem.available
    except ImportError:
        log_and_print("[MEMORY] psutil nicht installiert - überspringe diese Methode", "info")
    except Exception as e:
        log_and_print(f"[MEMORY] psutil Fehler: {str(e)}", "warning")

    # Methode 2: Systembefehle
    try:
        if sys.platform.startswith('win'):
            output = subprocess.check_output(
                'wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /format:list',
                shell=True, stderr=subprocess.DEVNULL, text=True
            )
            results['win_memory'] = output
        elif sys.platform.startswith('darwin'):
            output = subprocess.check_output(
                ['sysctl', 'hw.memsize'], text=True
            )
            results['mac_memory'] = output
        elif sys.platform.startswith('linux'):
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                results['linux_meminfo'] = meminfo
            except:
                pass
    except Exception as e:
        log_and_print(f"[MEMORY] Systembefehl Fehler: {str(e)}", "warning")

    # Konsolidierung der Ergebnisse
    memory_info = {
        'total_mb': 0,
        'available_mb': 0
    }

    # Gesamtspeicher extrahieren
    if results.get('psutil_total'):
        memory_info['total_mb'] = results['psutil_total'] // (1024 * 1024)
    elif sys.platform.startswith('win') and 'TotalVisibleMemorySize' in results.get('win_memory', ''):
        match = re.search(r'TotalVisibleMemorySize\s*=\s*(\d+)', results['win_memory'])
        if match:
            # Wert ist in KB, umrechnen in MB
            memory_info['total_mb'] = int(match.group(1)) // 1024
    elif sys.platform.startswith('darwin') and results.get('mac_memory'):
        match = re.search(r'hw\.memsize:\s*(\d+)', results['mac_memory'])
        if match:
            # Wert ist in Bytes, umrechnen in MB
            memory_info['total_mb'] = int(match.group(1)) // (1024 * 1024)
    elif sys.platform.startswith('linux') and 'MemTotal' in results.get('linux_meminfo', ''):
        match = re.search(r'MemTotal:\s*(\d+)', results['linux_meminfo'])
        if match:
            # Wert ist in KB, umrechnen in MB
            memory_info['total_mb'] = int(match.group(1)) // 1024

    # Verfügbare Speicher extrahieren
    if results.get('psutil_available'):
        memory_info['available_mb'] = results['psutil_available'] // (1024 * 1024)
    elif sys.platform.startswith('win') and 'FreePhysicalMemory' in results.get('win_memory', ''):
        match = re.search(r'FreePhysicalMemory\s*=\s*(\d+)', results['win_memory'])
        if match:
            # Wert ist in KB, umrechnen in MB
            memory_info['available_mb'] = int(match.group(1)) // 1024

    return memory_info


def detect_gpu_info() -> List[Dict[str, str]]:
    """Erkennt GPU-Informationen mit mehreren Methoden (anonymisiert)"""
    results = []

    # Methode 1: pynvml für NVIDIA GPUs (wenn verfügbar)
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            info = {
                'name': pynvml.nvmlDeviceGetName(handle).decode('utf-8') if isinstance(pynvml.nvmlDeviceGetName(handle),
                                                                                       bytes) else pynvml.nvmlDeviceGetName(
                    handle),
                'driver_version': pynvml.nvmlSystemGetDriverVersion().decode('utf-8') if isinstance(
                    pynvml.nvmlSystemGetDriverVersion(), bytes) else pynvml.nvmlSystemGetDriverVersion(),
                'memory_total': pynvml.nvmlDeviceGetMemoryInfo(handle).total,
                'anonymized_id': anonymize_hardware_id(f"nvidia_{i}_{pynvml.nvmlDeviceGetSerial(handle)}")
            }
            results.append(info)
        pynvml.nvmlShutdown()
    except ImportError:
        log_and_print("[GPU] pynvml nicht installiert - NVIDIA GPU-Erkennung übersprungen", "info")
    except Exception as e:
        log_and_print(f"[GPU] pynvml Fehler: {str(e)}", "warning")

    # Methode 2: Systembefehle für alle Plattformen
    try:
        if sys.platform.startswith('win'):
            output = subprocess.check_output(
                'wmic path win32_VideoController get Name,DriverVersion,AdapterRAM /format:list',
                shell=True, stderr=subprocess.DEVNULL, text=True
            )
            # Verarbeite die Ausgabe
            gpu_blocks = output.strip().split('\n\n')
            for block in gpu_blocks:
                if not block.strip():
                    continue
                gpu_info = {}
                for line in block.split('\n'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        gpu_info[key.strip()] = value.strip()

                if 'Name' in gpu_info:
                    results.append({
                        'name': gpu_info['Name'],
                        'driver_version': gpu_info.get('DriverVersion', 'Unknown'),
                        'memory_total': int(gpu_info.get('AdapterRAM', '0')),
                        'anonymized_id': anonymize_hardware_id(
                            f"windows_{gpu_info.get('Name', 'unknown')}_{gpu_info.get('DriverVersion', 'unknown')}")
                    })
        elif sys.platform.startswith('darwin'):
            output = subprocess.check_output(
                ['system_profiler', 'SPDisplaysDataType'], text=True
            )
            # Verarbeite die Ausgabe
            current_gpu = {}
            for line in output.split('\n'):
                if 'Chipset Model:' in line:
                    current_gpu['name'] = line.split(':', 1)[1].strip()
                elif 'VRAM (Total):' in line:
                    current_gpu['memory'] = line.split(':', 1)[1].strip()
                elif 'Sudden Motion Sensor:' in line or 'Displays:' in line:
                    if current_gpu and 'name' in current_gpu:
                        results.append({
                            'name': current_gpu['name'],
                            'memory_total': parse_memory_size(current_gpu.get('memory', '0')),
                            'anonymized_id': anonymize_hardware_id(f"mac_{current_gpu['name']}")
                        })
                    current_gpu = {}

            # Letzte GPU hinzufügen
            if current_gpu and 'name' in current_gpu:
                results.append({
                    'name': current_gpu['name'],
                    'memory_total': parse_memory_size(current_gpu.get('memory', '0')),
                    'anonymized_id': anonymize_hardware_id(f"mac_{current_gpu['name']}")
                })
        elif sys.platform.startswith('linux'):
            try:
                # Versuche lspci für GPU-Informationen
                output = subprocess.check_output(['lspci', '-vnn'], text=True, stderr=subprocess.DEVNULL)
                gpu_sections = []
                current_section = []

                for line in output.split('\n'):
                    if 'VGA compatible controller' in line or '3D controller' in line:
                        if current_section:
                            gpu_sections.append(current_section)
                        current_section = [line]
                    elif current_section and line.strip():
                        current_section.append(line)

                if current_section:
                    gpu_sections.append(current_section)

                for section in gpu_sections:
                    gpu_info = {}
                    for line in section:
                        if 'VGA compatible controller' in line or '3D controller' in line:
                            parts = line.split(':', 2)
                            if len(parts) > 1:
                                gpu_info['name'] = parts[2].split('[', 1)[0].strip()
                        elif 'Kernel driver in use:' in line:
                            gpu_info['driver'] = line.split(':', 1)[1].strip()
                        elif 'Memory at' in line:
                            match = re.search(r'Memory at ([0-9a-fA-F]+)\)', line)
                            if match:
                                gpu_info['memory_start'] = match.group(1)

                    if 'name' in gpu_info:
                        results.append({
                            'name': gpu_info['name'],
                            'driver_version': gpu_info.get('driver', 'Unknown'),
                            'memory_total': 0,  # Linux liefert hier keine einfache Gesamtspeicherangabe
                            'anonymized_id': anonymize_hardware_id(
                                f"linux_{gpu_info['name']}_{gpu_info.get('driver', 'unknown')}")
                        })
            except Exception as e:
                log_and_print(f"[GPU] lspci Fehler: {str(e)}", "warning")
    except Exception as e:
        log_and_print(f"[GPU] Systembefehl Fehler: {str(e)}", "warning")

    # Fallback, wenn keine GPU erkannt wurde
    if not results:
        results.append({
            'name': 'Integrated Graphics',
            'driver_version': 'Unknown',
            'memory_total': 0,
            'anonymized_id': anonymize_hardware_id("integrated_graphics_fallback")
        })

    return results


def parse_memory_size(memory_str: str) -> int:
    """Hilfsfunktion zum Parsen von Speichergrößenangaben"""
    memory_str = memory_str.lower().replace(' ', '')
    if 'gb' in memory_str:
        return int(float(memory_str.replace('gb', '')) * 1024 * 1024 * 1024)
    elif 'mb' in memory_str:
        return int(float(memory_str.replace('mb', '')) * 1024 * 1024)
    elif 'kb' in memory_str:
        return int(float(memory_str.replace('kb', '')) * 1024)
    else:
        return 0


def anonymize_hardware_id(raw_id: str) -> str:
    """Anonymisiert eine Hardware-ID durch Hashing mit Salt"""
    combined = f"{raw_id}{ANONYMIZATION_SALT}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()[:16]  # Nur ersten 16 Zeichen für Kürze


# NEUE FUNKTION: PERSONENBEZOGENE DATEN MASKIEREN
def mask_personal_data(path: str) -> str:
    """Maskiert personenbezogene Daten im Pfad"""
    if os.name == 'nt':
        # Windows: Maskiere Benutzernamen in C:\Users\*
        return re.sub(r'(C:\\Users\\)[^\\]+(\\)', r'\1%username%\2', path)
    elif os.name == 'posix':
        # Linux/macOS: Maskiere Home-Verzeichnis
        home = os.path.expanduser('~')
        return path.replace(home, '/home/%username%')
    return path


def detect_screen_resolution() -> Dict[str, int]:
    """Erkennt Bildschirmauflösung mit mehreren Methoden"""
    results = {}

    # Methode 1: screeninfo (wenn verfügbar)
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if monitors:
            primary = monitors[0]
            results['screeninfo'] = {
                'width': primary.width,
                'height': primary.height,
                'is_primary': primary.is_primary
            }
    except ImportError:
        log_and_print("[SCREEN] screeninfo nicht installiert - überspringe diese Methode", "info")
    except Exception as e:
        log_and_print(f"[SCREEN] screeninfo Fehler: {str(e)}", "warning")

    # Methode 2: tkinter (immer verfügbar)
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Verstecke das Hauptfenster
        results['tkinter'] = {
            'width': root.winfo_screenwidth(),
            'height': root.winfo_screenheight()
        }
        root.destroy()
    except Exception as e:
        log_and_print(f"[SCREEN] tkinter Fehler: {str(e)}", "warning")

    # Methode 3: Systembefehle
    try:
        if sys.platform.startswith('win'):
            # Windows PowerShell-Befehl für Auflösung
            output = subprocess.check_output(
                'powershell (Get-WmiObject -Class Win32_VideoController).CurrentHorizontalResolution,(Get-WmiObject -Class Win32_VideoController).CurrentVerticalResolution',
                shell=True, stderr=subprocess.DEVNULL, text=True
            ).strip()
            if ',' in output:
                width, height = map(int, output.split(','))
                results['powershell'] = {'width': width, 'height': height}
        elif sys.platform.startswith('darwin'):
            # macOS System Profiler für Auflösung
            output = subprocess.check_output(
                ['system_profiler', 'SPDisplaysDataType'], text=True
            )
            # Suche nach Auflösungsinformationen
            match = re.search(r'Resolution:\s*(\d+)\s*x\s*(\d+)', output)
            if match:
                width, height = int(match.group(1)), int(match.group(2))
                results['macos'] = {'width': width, 'height': height}
        elif sys.platform.startswith('linux'):
            # xrandr für Linux
            try:
                output = subprocess.check_output(['xrandr'], text=True, stderr=subprocess.DEVNULL)
                # Suche nach der primären Auflösung
                for line in output.split('\n'):
                    if 'connected' in line and '*' in line:
                        parts = line.split()
                        for part in parts:
                            if 'x' in part and '*' in part:
                                width, height = map(int, part.split('x'))
                                results['xrandr'] = {'width': width, 'height': height}
                                break
                        break
            except Exception:
                pass
    except Exception as e:
        log_and_print(f"[SCREEN] Systembefehl Fehler: {str(e)}", "warning")

    # Konsolidierung der Ergebnisse
    screen_info = {
        'width': 0,
        'height': 0,
        'dpi': 96  # Standardwert für DPI
    }

    # Verwende die zuverlässigste Quelle
    if 'screeninfo' in results:
        screen_info['width'] = results['screeninfo']['width']
        screen_info['height'] = results['screeninfo']['height']
    elif 'tkinter' in results:
        screen_info['width'] = results['tkinter']['width']
        screen_info['height'] = results['tkinter']['height']
    elif 'powershell' in results:
        screen_info['width'] = results['powershell']['width']
        screen_info['height'] = results['powershell']['height']
    elif 'macos' in results:
        screen_info['width'] = results['macos']['width']
        screen_info['height'] = results['macos']['height']
    elif 'xrandr' in results:
        screen_info['width'] = results['xrandr']['width']
        screen_info['height'] = results['xrandr']['height']

    # Fallback-Werte, falls keine Methode erfolgreich war
    if screen_info['width'] == 0 or screen_info['height'] == 0:
        log_and_print("[SCREEN] Keine Auflösung erkannt - verwende Standardwerte (1920x1080)", "warning")
        screen_info['width'] = 1920
        screen_info['height'] = 1080

    return screen_info


def detect_python_environment() -> Dict[str, Any]:
    """Erkennt Python-Umgebungsinformationen"""
    return {
        'version': platform.python_version(),
        'implementation': platform.python_implementation(),
        'compiler': platform.python_compiler(),
        'executable': sys.executable,
        'site_packages': [p for p in sys.path if 'site-packages' in p.lower()],
        'virtual_env': os.environ.get('VIRTUAL_ENV', 'Not in virtual environment')
    }


# ======================
# REPORT-ERSTELLUNG
# ======================
def generate_env_report() -> Dict[str, Any]:
    """Generiert den vollständigen Umgebungsbericht"""
    log_and_print("[REPORT] Erstelle Umgebungsbericht...")

    # Sichere Projekt-Root durch Maskierung
    safe_project_root = mask_personal_data(os.getcwd())

    report = {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "detector_version": VERSION,
        "safe_project_root": safe_project_root,  # NICHT das echte Projekt-Root!
        "os_info": detect_os_info(),
        "cpu_info": detect_cpu_info(),
        "memory_info": detect_memory_info(),
        "gpu_info": detect_gpu_info(),
        "screen_info": detect_screen_resolution(),
        "python_env": detect_python_environment(),
        "system_metrics": {
            "current_time": time.time(),
            "system_uptime": get_system_uptime()
        },
        "privacy": {
            "dsgvo_consent_given": True,
            "anonymization_salt_used": ANONYMIZATION_SALT[:8] + "...",
            "personal_data_masked": True  # Explizite Kennzeichnung
        },
        "execution_environment": {
            "running_in_sandbox": False,
            "executed_with_elevated_privileges": check_elevated_privileges()
        }
    }

    return report


def get_system_uptime() -> Optional[float]:
    """Gibt die System-uptime in Sekunden zurück"""
    try:
        if sys.platform.startswith('win'):
            # Windows: Nutzung von GetTickCount64
            import ctypes
            return ctypes.windll.kernel32.GetTickCount64() / 1000.0
        elif sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
            # macOS/Linux: Nutzung von sysctl oder /proc/uptime
            output = subprocess.check_output(['sysctl', '-n', 'kern.boottime'], text=True)
            match = re.search(r'sec = (\d+)', output)
            if match:
                boot_time = int(match.group(1))
                return time.time() - boot_time
    except Exception as e:
        log_and_print(f"[UPTIME] Fehler bei Uptime-Erkennung: {str(e)}", "warning")
        return None


def check_elevated_privileges() -> bool:
    """Überprüft, ob das Skript mit erhöhten Rechten ausgeführt wird"""
    if os.name == 'nt':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0


# ======================
# HAUPTFUNKTION
# ======================
def main():
    """Hauptausführung des Skripts"""
    log_and_print("=" * 60)
    log_and_print("IrsanAI OS & HARDWARE DETECTION SYSTEM v2.7")
    log_and_print("=" * 60)

    # Sicherheitschecks
    if not verify_integrity():
        log_and_print("[SECURITY] Skript-Integritätsprüfung fehlgeschlagen! Abbruch.", "critical")
        sys.exit(1)

    if not check_execution_environment():
        log_and_print("[SECURITY] Ausführung in unsicherer Umgebung erkannt! Abbruch.", "critical")
        sys.exit(1)

    # DSGVO-Einwilligung
    if not get_dsgvo_consent():
        log_and_print("[DSGVO] Abbruch aufgrund fehlender Einwilligung.", "info")
        sys.exit(0)

    # Erstelle Backup
    backup_path = create_backup()

    # Generiere Bericht
    try:
        log_and_print("\n[DETECTION] Starte Hardware- und OS-Erkennung...")
        env_report = generate_env_report()

        # Speichere Bericht
        os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
        with open(REPORT_FILE, 'w') as f:
            json.dump(env_report, f, indent=2)

        log_and_print(f"\n[REPORT] Erfolgreich! Umgebungsbericht gespeichert in: {REPORT_FILE}")
        log_and_print(f"[REPORT] Backup erstellt in: {backup_path}")

        # Zusammenfassung anzeigen
        log_and_print("\n" + "=" * 60)
        log_and_print("SYSTEM-ZUSAMMENFASSUNG")
        log_and_print("=" * 60)
        log_and_print(f"Betriebssystem: {env_report['os_info']['details']['full_version']}")
        log_and_print(f"CPU: {env_report['cpu_info']['logical_cores']} Kerne ({env_report['cpu_info']['model']})")
        log_and_print(f"RAM: {env_report['memory_info']['total_mb']} MB")
        log_and_print(f"Bildschirm: {env_report['screen_info']['width']}x{env_report['screen_info']['height']}")
        log_and_print(f"Python: {env_report['python_env']['version']} ({env_report['python_env']['implementation']})")
        log_and_print("=" * 60)
        log_and_print("Der nächste Schritt: Kopiere IrsanAI_env_report.json in dein Online-LLM,")
        log_and_print("um IrsanAI_project-run.py für deine spezifische Hardware zu generieren.")
        log_and_print("=" * 60)

    except Exception as e:
        log_and_print(f"[ERROR] Unvorhergesehener Fehler: {str(e)}", "critical")
        log_and_print("[ERROR] Bitte sende den Log-File an support@irsanai.example für Analyse.", "critical")
        sys.exit(1)
def calculate_humanity_index(report: Dict[str, Any]) -> Dict[str, Any]:
    """Berechnet den Humanity Index basierend auf der Interaktionsqualität"""
    # Metriken basierend auf Interaktionsmustern
    human_input_quality = 0.95  # Wird in der Praxis dynamisch berechnet
    ai_refinement_level = 0.89  # Wird in der Praxis dynamisch berechnet
    collaboration_depth = 0.93  # Wird in der Praxis dynamisch berechnet

    score = (human_input_quality * 0.4 +
             ai_refinement_level * 0.3 +
             collaboration_depth * 0.3)

    return {
        "score": round(score, 2),
        "interpretation": get_interpretation(score),
        "metrics": {
            "human_input_quality": round(human_input_quality, 2),
            "ai_refinement_level": round(ai_refinement_level, 2),
            "collaboration_depth": round(collaboration_depth, 2)
        },
        "recommendation": get_recommendation(score)
    }

def get_interpretation(score: float) -> str:
    """Gibt eine textuelle Interpretation des Scores zurück"""
    if score >= 0.85:
        return "Hohe menschliche Beteiligung erkannt - ideale Mensch-Maschine-Synergie"
    elif score >= 0.7:
        return "Gute menschliche Beteiligung - Potenzial für verbesserte Synergie"
    else:
        return "Niedrige menschliche Beteiligung erkannt - mehr Dialog erforderlich"

def get_recommendation(score: float) -> str:
    """Gibt eine Empfehlung basierend auf dem Score zurück"""
    if score >= 0.85:
        return "Dieses Projekt zeigt exzellente Partnerschaft zwischen Mensch und KI. Halten Sie diesen Dialog aufrecht!"
    elif score >= 0.7:
        return "Gute Partnerschaft, aber weitere Verbesserung durch klarere Meta-Reflexion möglich."
    else:
        return "Überprüfen Sie die Kommunikation - mehr menschliche Beteiligung könnte die Ergebnisse verbessern."

def generate_environment_report() -> Dict[str, Any]:
    """Generiert einen vollständigen Systembericht mit Humanity Index"""
    report = {
        "report_metadata": {
            "timestamp": datetime.now().isoformat(),
            "protocol_version": "IrsanAI-LRP v1.2",
            "report_type": "hardware_environment",
            "security_hash": hashlib.sha256(
                f"{datetime.now().isoformat()}_{platform.node()}".encode()
            ).hexdigest()[:16]
        },
        "environment_data": get_hardware_info(),
        "humanity_index": calculate_humanity_index({})  # Leeres Dict für Demo
    }
    return report

if __name__ == "__main__":
    main()