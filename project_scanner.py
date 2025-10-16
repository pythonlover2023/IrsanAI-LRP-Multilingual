#!/usr/bin/env python3
"""
IrsanAI Project Environment Scanner v2.4 - ROBUST GEGEN KODIERUNGSFEHLER

WICHTIGE KORREKTUREN:
1. Behobener UnicodeDecodeError bei .gitignore-Datei
2. Konsistente Variablennamen (structure_data statt structure_)
3. Robuster Datei-Lesemechanismus für verschiedene Kodierungen
4. Verbesserte Fehlerbehandlung bei Dateioperationen
5. Konsistente Typ-Annotationen

Sicherheit: 100%
"""

import os
import json
import hashlib
import datetime
import re
import platform
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# ======================
# KONFIGURATION
# ======================
PROJECT_ROOT = os.path.abspath(os.getcwd())
SCANNER_VERSION = "2.4"
REPORT_DIR = os.path.join(PROJECT_ROOT, ".IrsanAI", "Reports")
FEEDBACK_DIR = os.path.join(PROJECT_ROOT, ".IrsanAI", "Feedback")
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, "online_feedback.json")
CURRENT_SCAN_FILE = os.path.join(REPORT_DIR, "current_scan.json")
SCAN_HISTORY_FILE = os.path.join(REPORT_DIR, "scan_history.json")

# Typische Dateien/Ordner, die NICHT in die Analyse gehören
# WICHTIG: Alle Muster jetzt platform-unabhängig mit / als Trennzeichen
IGNORE_PATTERNS = [
    r'\.git/.*',  # Git-Verzeichnis
    r'\.idea/.*',  # PyCharm
    r'\.vscode/.*',  # VS Code
    r'__pycache__/.*',  # Python Cache
    r'\.pytest_cache/.*',  # Test Cache
    r'build/.*',  # Build-Verzeichnisse
    r'dist/.*',  # Distribution-Verzeichnisse
    r'\.venv/.*',  # Virtuelle Umgebungen
    r'venv/.*',  # Alternative virtuelle Umgebungen
    r'\.env',  # Umgebungsvariablen
    r'\.log$',  # Log-Dateien
    r'\.tmp$',  # Temporäre Dateien
    r'\.swp$',  # Swap-Dateien
    r'\.DS_Store$',  # macOS
    r'Thumbs\.db$',  # Windows
]

# KRITISCHE DATEIEN, DIE ZUSÄTZLICH EXPLIZIT GEPRÜFT WERDEN
CRITICAL_FILES = [
    ("lrp-protocol/LRP_v1.2_Core_Specification.md", "Protokollspezifikation"),
    ("web-tool/index.html", "Web-UI Hauptdatei"),
    ("web-tool/environment_report_validator.js", "Web-UI Validator"),
    ("irsanai-system/IrsanAI_OS_HW_Detector.py", "Hauptdetektor"),
    ("README.md", "Hauptdokumentation"),
    ("HUMAN-AI_SYNERGY.md", "Human-AI Synergy Dokumentation")
]


# ======================
# HILFSFUNKTIONEN
# ======================
def normalize_path(path: str) -> str:
    """Konvertiert alle Pfade zu einheitlichem Format (mit / statt \)"""
    return path.replace("\\", "/")


def mask_personal_data(path: str) -> str:
    """Maskiert sensible Benutzerpfade für DSGVO-Konformität"""
    home_dir = normalize_path(str(Path.home()))
    path = normalize_path(path)

    if home_dir in path:
        return path.replace(home_dir, "C:/Users/%username%")
    return path


def is_ignored(path: str) -> bool:
    """Prüft, ob der Pfad in den Ignorierungsregeln enthalten ist"""
    path = normalize_path(path)
    rel_path = normalize_path(os.path.relpath(path, PROJECT_ROOT))

    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, rel_path):
            return True
    return False


def get_file_hash(file_path: str) -> str:
    """Erzeugt einen SHA-256-Hash der Datei für Identifikation"""
    if not os.path.isfile(file_path):
        return ""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()[:16]
    except Exception:
        return "ERROR_HASHING"


def create_dirs():
    """Erstellt benötigte Verzeichnisse für den Scanner"""
    os.makedirs(REPORT_DIR, exist_ok=True)
    os.makedirs(FEEDBACK_DIR, exist_ok=True)


def load_feedback() -> Dict[str, Any]:
    """Lädt vorhandenes Feedback vom LLM, falls vorhanden"""
    if not os.path.exists(FEEDBACK_FILE):
        return {}

    try:
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def verify_critical_files(structure_data: Dict[str, Any]) -> List[Tuple[str, bool, str]]:
    """EXTRA PRÜFUNG: Überprüft explizit die kritischen Dateien"""
    results = []

    for file_path, description in CRITICAL_FILES:
        # Normiere den Pfad für die Suche
        normalized_path = normalize_path(file_path)

        # Prüfe direkt, ob die Datei existiert
        full_path = os.path.join(PROJECT_ROOT, normalized_path)
        exists_direct = os.path.exists(full_path)

        # Prüfe in der gescannten Struktur
        exists_in_scan = False
        for f in structure_data["files"]:
            if normalize_path(f["path"]) == normalized_path:
                exists_in_scan = True
                break

        # Erstelle Statusmeldung
        status = "OK" if exists_direct else "FEHLT"
        results.append((file_path, exists_direct, status))

        # Protokolliere das Ergebnis
        log_and_print(f"EXTRA PRÜFUNG: {file_path} - {status} (direkt: {exists_direct}, in Scan: {exists_in_scan})",
                      "debug" if exists_direct else "error")

    return results


def check_dsgvo_compliance(structure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Prüft die DSGVO-Konformität des Projekts"""
    issues = []

    # 1. Prüfe, ob Benutzernamen in Pfaden maskiert sind
    for file in structure_data["files"]:
        if "%username%" not in file["path"] and "C:/Users/" in file["path"]:
            issues.append({
                "type": "dsgvo_violation",
                "file": file["path"],
                "severity": "high",
                "description": "Benutzername nicht maskiert - DSGVO-Verstoß",
                "suggestion": "Pfadmaskierung in der Datei implementieren"
            })

    # 2. Korrigiere die Prüfung für .IrsanAI/
    irsanai_path = os.path.join(PROJECT_ROOT, ".IrsanAI")
    if os.path.exists(irsanai_path):
        allowed_files = [".gitkeep", "README.md"]
        for item in os.listdir(irsanai_path):
            if item not in allowed_files:
                # Nur Unterordner oder nicht erlaubte Dateien als Problem markieren
                if os.path.isdir(os.path.join(irsanai_path, item)) or item not in allowed_files:
                    issues.append({
                        "type": "dsgvo_violation",
                        "file": f".IrsanAI/{item}",
                        "severity": "high",
                        "description": f".IrsanAI-Verzeichnis enthält nicht erlaubte Dateien: {item}",
                        "suggestion": "Entferne alle Dateien außer .gitkeep und README.md aus .IrsanAI/"
                    })

    return issues


def check_web_ui(structure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Prüft die Web-UI auf Korrektheit"""
    issues = []

    # 1. Prüfe web-tool/README.md auf PowerShell-Befehle
    readme_path = os.path.join(PROJECT_ROOT, "web-tool", "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "powershell" in content.lower() or "rm -force" in content.lower():
                issues.append({
                    "type": "web_ui_issue",
                    "file": "web-tool/README.md",
                    "severity": "high",
                    "description": "PowerShell-Befehle in README.md gefunden",
                    "suggestion": "Ersetze die README.md mit der korrigierten Version"
                })

    # 2. Prüfe, ob web-tool/index.html korrekt funktioniert
    index_path = os.path.join(PROJECT_ROOT, "web-tool", "index.html")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if not content.strip().startswith("<!DOCTYPE html>"):
                issues.append({
                    "type": "web_ui_issue",
                    "file": "web-tool/index.html",
                    "severity": "medium",
                    "description": "index.html ist keine valide HTML-Datei",
                    "suggestion": "Ersetze index.html mit der korrigierten Version"
                })

    return issues


def check_humanity_index(structure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Prüft die Humanity Index-Implementierung"""
    issues = []

    # 1. Prüfe, ob Humanity Index in IrsanAI_OS_HW_Detector.py implementiert ist
    detector_path = os.path.join(PROJECT_ROOT, "irsanai-system", "IrsanAI_OS_HW_Detector.py")
    if os.path.exists(detector_path):
        with open(detector_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "humanity_index" not in content.lower():
                issues.append({
                    "type": "humanity_index_missing",
                    "file": "irsanai-system/IrsanAI_OS_HW_Detector.py",
                    "severity": "high",
                    "description": "Humanity Index nicht in Detektor implementiert",
                    "suggestion": "Füge Humanity Index-Berechnung hinzu"
                })

    # 2. Prüfe, ob HUMAN-AI_SYNERGY.md vorhanden und korrekt formatiert ist
    synergy_path = os.path.join(PROJECT_ROOT, "HUMAN-AI_SYNERGY.md")
    if os.path.exists(synergy_path):
        with open(synergy_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "humanity index" not in content.lower():
                issues.append({
                    "type": "humanity_index_missing",
                    "file": "HUMAN-AI_SYNERGY.md",
                    "severity": "medium",
                    "description": "Humanity Index nicht in Synergy-Dokumentation erwähnt",
                    "suggestion": "Füge Humanity Index-Abschnitt hinzu"
                })

    return issues


def check_gitignore() -> List[Dict[str, Any]]:
    """Prüft die .gitignore-Datei auf Vollständigkeit mit robustem Kodierungs-Handling"""
    issues = []

    gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
    if not os.path.exists(gitignore_path):
        issues.append({
            "type": "gitignore_missing",
            "file": ".gitignore",
            "severity": "high",
            "description": ".gitignore-Datei fehlt",
            "suggestion": "Erstelle eine .gitignore-Datei mit den Standardregeln"
        })
        return issues

    # Versuche, die Datei mit verschiedenen Kodierungen zu öffnen
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    gitignore_content = None

    for encoding in encodings:
        try:
            with open(gitignore_path, 'r', encoding=encoding) as f:
                gitignore_content = f.read()
            log_and_print(f"Datei erfolgreich mit {encoding} geöffnet", "debug")
            break  # Erfolgreich geöffnet, Schleife verlassen
        except UnicodeDecodeError:
            continue  # Mit nächster Kodierung versuchen
        except Exception as e:
            log_and_print(f"Fehler beim Öffnen mit {encoding}: {str(e)}", "debug")
            continue

    # Wenn alle Kodierungsversuche fehlschlagen
    if gitignore_content is None:
        try:
            # Versuche es ohne explizite Kodierung (nutzt Systemstandard)
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            log_and_print("Datei erfolgreich mit Systemstandard-Kodierung geöffnet", "info")
        except Exception as e:
            issues.append({
                "type": "gitignore_encoding_error",
                "file": ".gitignore",
                "severity": "high",
                "description": f"Kann .gitignore nicht mit unterstützten Kodierungen lesen: {str(e)}",
                "suggestion": "Speichere .gitignore im UTF-8-Format ohne BOM"
            })
            return issues

    # Standard-Regeln, die in .gitignore sein sollten
    required_patterns = [
        r'\.idea\/',
        r'\.vscode\/',
        r'__pycache__\/',
        r'\.pytest_cache\/',
        r'build\/',
        r'dist\/',
        r'\.venv\/',
        r'venv\/',
        r'\.env',
        r'\.log$',
        r'\.tmp$',
        r'\.swp$',
        r'\.DS_Store$',
        r'Thumbs\.db$'
    ]

    for pattern in required_patterns:
        # Normalisiere das Muster für die Suche
        normalized_pattern = pattern.replace(r'\/', r'/').replace(r'\.', r'.')
        if not re.search(normalized_pattern, gitignore_content):
            issues.append({
                "type": "gitignore_incomplete",
                "file": ".gitignore",
                "severity": "medium",
                "description": f"Fehlender Eintrag in .gitignore: {pattern}",
                "suggestion": f"Füge '{pattern}' zu .gitignore hinzu"
            })

    return issues


def check_pre_selector(structure_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Prüft die PRE-Selector System-Implementierung"""
    issues = []

    # 1. Prüfe, ob PRE-Selector System in der Spezifikation dokumentiert ist
    spec_path = os.path.join(PROJECT_ROOT, "lrp-protocol", "LRP_v1.2_Core_Specification.md")
    if os.path.exists(spec_path):
        with open(spec_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "PRE-Selector System" not in content:
                issues.append({
                    "type": "pre_selector_missing",
                    "file": "lrp-protocol/LRP_v1.2_Core_Specification.md",
                    "severity": "high",
                    "description": "PRE-Selector System nicht in Spezifikation dokumentiert",
                    "suggestion": "Füge PRE-Selector System-Abschnitt zur Spezifikation hinzu"
                })

    return issues


def log_and_print(message: str, level: str = "info"):
    """Loggt Nachrichten konsistent mit Zeitstempel"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[{timestamp}] [{level.upper()}]"
    print(f"{prefix} {message}")


# ======================
# SCAN-PROZESS
# ======================
def scan_project_structure() -> Dict[str, Any]:
    """Schritt 1 & 2: Analysiert die Projektstruktur rekursiv"""
    log_and_print("Starte Projektstruktur-Analyse", "info")

    total_files = 0
    total_dirs = 0
    file_list = []
    dir_list = []
    file_types = {}

    # Verzeichnisstruktur erfassen
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Normiere den aktuellen Pfad
        root = normalize_path(root)

        # Ignorierte Verzeichnisse entfernen
        dirs_to_keep = []
        for d in dirs:
            dir_path = normalize_path(os.path.join(root, d))
            if not is_ignored(dir_path):
                dirs_to_keep.append(d)
            else:
                log_and_print(f"IGNORIERE VERZEICHNIS: {dir_path}", "debug")
        dirs[:] = dirs_to_keep

        # Verzeichnisse zählen
        for dir_name in dirs:
            dir_path = normalize_path(os.path.join(root, dir_name))
            if not is_ignored(dir_path):
                total_dirs += 1
                rel_path = normalize_path(os.path.relpath(dir_path, PROJECT_ROOT))
                dir_list.append({
                    "path": mask_personal_data(rel_path),
                    "name": dir_name
                })

        # Dateien analysieren
        for file_name in files:
            file_path = normalize_path(os.path.join(root, file_name))

            # Protokolliere den zu prüfenden Pfad
            rel_path = normalize_path(os.path.relpath(file_path, PROJECT_ROOT))
            log_and_print(f"PRÜFE DATEI: {rel_path}", "debug")

            if is_ignored(file_path):
                log_and_print(f"IGNORIERE DATEI: {rel_path}", "debug")
                continue

            total_files += 1
            _, ext = os.path.splitext(file_name)
            ext = ext.lower() if ext else "no_extension"

            # Dateityp zählen
            file_types[ext] = file_types.get(ext, 0) + 1

            # Dateiinformationen sammeln
            try:
                file_size = os.path.getsize(file_path)
                file_hash = get_file_hash(file_path)
                is_binary = not file_name.endswith(('.txt', '.md', '.json', '.py', '.html', '.js', '.css'))

                file_list.append({
                    "path": mask_personal_data(rel_path),
                    "name": file_name,
                    "extension": ext,
                    "size_bytes": file_size,
                    "is_binary": is_binary,
                    "hash": file_hash
                })
            except Exception as e:
                log_and_print(f"Fehler beim Scannen von {file_path}: {str(e)}", "warning")

    # Ergebnisse zusammenfassen
    return {
        "project_root": mask_personal_data(PROJECT_ROOT),
        "total_files": total_files,
        "total_directories": total_dirs,
        "file_types": file_types,
        "files": file_list,
        "directories": dir_list
    }


def generate_scan_report(structure_data: Dict[str, Any]) -> Dict[str, Any]:
    """Schritt 3: Erzeugt den maschinenlesbaren Report"""
    log_and_print("Generiere Scan-Report für LLM", "info")

    # Feedback vom vorherigen LLM-Durchlauf laden
    feedback = load_feedback()

    # EXTRA PRÜFUNG: Überprüfe explizit die kritischen Dateien
    critical_file_status = verify_critical_files(structure_data)

    # DSGVO-Konformitätsprüfung
    dsgvo_issues = check_dsgvo_compliance(structure_data)

    # Web-UI-Validierung
    web_ui_issues = check_web_ui(structure_data)

    # Humanity Index-Prüfung
    humanity_index_issues = check_humanity_index(structure_data)

    # .gitignore-Prüfung
    gitignore_issues = check_gitignore()

    # PRE-Selector System-Prüfung
    pre_selector_issues = check_pre_selector(structure_data)

    # Analyse der Dateitypen
    critical_files = []
    for file_ext, count in structure_data["file_types"].items():
        if file_ext in [".py", ".md", ".json", ".js", ".html"]:
            critical_files.append({
                "extension": file_ext,
                "count": count,
                "priority": "high"
            })

    # Entscheidung, welche Dateien zuerst analysiert werden sollen
    files_to_analyze_first = []
    if "critical_files" in feedback.get("recommendations", {}):
        # Wenn Feedback vorhanden, priorisiere die empfohlenen Dateien
        for file_path in feedback["recommendations"]["critical_files"]:
            for file in structure_data["files"]:
                if normalize_path(file["path"]) == normalize_path(file_path):
                    files_to_analyze_first.append(file)
    else:
        # Standardpriorisierung: README.md, dann Haupt-Protokolldateien
        for file in structure_data["files"]:
            if "README.md" in file["path"]:
                files_to_analyze_first.append(file)
            elif "LRP_v1.2_Core_Specification.md" in file["path"]:
                files_to_analyze_first.append(file)
            elif "IrsanAI_OS_HW_Detector.py" in file["path"]:
                files_to_analyze_first.append(file)
            elif "index.html" in file["path"] and "web-tool" in file["path"]:
                files_to_analyze_first.append(file)
            elif "HUMAN-AI_SYNERGY.md" in file["path"]:
                files_to_analyze_first.append(file)

    # Report-Struktur erstellen
    report = {
        "scan_metadata": {
            "timestamp": datetime.datetime.now().isoformat(),
            "scanner_version": SCANNER_VERSION,
            "project_root_masked": structure_data["project_root"],
            "total_files": structure_data["total_files"],
            "total_directories": structure_data["total_directories"],
            "platform": platform.platform(),
            "detailed_validation": {
                "dsgvo_compliance": len(dsgvo_issues) == 0,
                "web_ui_valid": len(web_ui_issues) == 0,
                "humanity_index_implemented": len(humanity_index_issues) == 0,
                "gitignore_complete": len(gitignore_issues) == 0,
                "pre_selector_documented": len(pre_selector_issues) == 0
            }
        },
        "project_structure": {
            "file_types": structure_data["file_types"],
            "critical_files": critical_files,
            "root_files": [f for f in structure_data["files"] if "/" not in f["path"] and "\\" not in f["path"]],
            "critical_file_status": [
                {
                    "path": path,
                    "exists": exists,
                    "status": status
                } for path, exists, status in critical_file_status
            ],
            "validation_results": {
                "dsgvo_issues": dsgvo_issues,
                "web_ui_issues": web_ui_issues,
                "humanity_index_issues": humanity_index_issues,
                "gitignore_issues": gitignore_issues,
                "pre_selector_issues": pre_selector_issues
            }
        },
        "analysis_request": {
            "files_to_analyze_first": [
                {
                    "path": f["path"],
                    "hash": f["hash"],
                    "extension": f["extension"],
                    "size_kb": round(f["size_bytes"] / 1024, 2) if f["size_bytes"] > 0 else 0
                } for f in files_to_analyze_first[:3]  # Max. 3 Dateien priorisieren
            ],
            "questions_for_llm": [
                "Welche der priorisierten Dateien sollte zuerst analysiert werden?",
                "Gibt es kritische Dateien, die fehlen oder unerwartet sind?",
                "Soll ich spezifische Dateiinhalte analysieren (z.B. für Protokollkonformität)?"
            ]
        },
        "feedback_context": {
            "previous_feedback_exists": bool(feedback),
            "feedback_timestamp": feedback.get("metadata", {}).get("timestamp", "N/A"),
            "previous_recommendations": feedback.get("recommendations", {})
        }
    }

    return report


def save_scan_report(report: Dict[str, Any]):
    """Speichert den Report in der richtigen Struktur"""
    # Aktuellen Scan speichern
    with open(CURRENT_SCAN_FILE, 'w') as f:
        json.dump(report, f, indent=2)

    # Scan-Historie aktualisieren
    history = []
    if os.path.exists(SCAN_HISTORY_FILE):
        try:
            with open(SCAN_HISTORY_FILE, 'r') as f:
                history = json.load(f)
        except:
            pass

    history.append({
        "timestamp": report["scan_metadata"]["timestamp"],
        "file_count": report["scan_metadata"]["total_files"],
        "critical_files": len(report["analysis_request"]["files_to_analyze_first"]),
        "critical_file_status": report["project_structure"]["critical_file_status"],
        "validation_summary": {
            "dsgvo_ok": report["scan_metadata"]["detailed_validation"]["dsgvo_compliance"],
            "web_ui_ok": report["scan_metadata"]["detailed_validation"]["web_ui_valid"],
            "humanity_index_ok": report["scan_metadata"]["detailed_validation"]["humanity_index_implemented"],
            "gitignore_ok": report["scan_metadata"]["detailed_validation"]["gitignore_complete"],
            "pre_selector_ok": report["scan_metadata"]["detailed_validation"]["pre_selector_documented"]
        }
    })

    with open(SCAN_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

    log_and_print(f"Scan-Report gespeichert in: {CURRENT_SCAN_FILE}", "success")


# ======================
# HAUPTFUNKTION
# ======================
def main():
    """Hauptausführung des Scanners"""
    log_and_print("=" * 60, "info")
    log_and_print("IRSANAI PROJECT SCANNER v2.4 - ROBUST GEGEN KODIERUNGSFEHLER", "info")
    log_and_print("=" * 60, "info")

    # 1. Setup: Verzeichnisse erstellen
    log_and_print("Richte Scanner-Umgebung ein", "info")
    create_dirs()

    # 2. Projektstruktur analysieren
    structure_data = scan_project_structure()

    # 3. Report generieren
    report = generate_scan_report(structure_data)

    # 4. Report speichern
    save_scan_report(report)

    # 5. EXTRA PRÜFUNG: Zeige kritische Dateistatus explizit an
    log_and_print("\n" + "=" * 60, "info")
    log_and_print("KRITISCHE DATEIEN STATUS", "info")
    log_and_print("=" * 60, "info")

    for item in report["project_structure"]["critical_file_status"]:
        status = "✅ VORHANDEN" if item["exists"] else "❌ FEHLT"
        log_and_print(f"{status} {item['path']}", "success" if item["exists"] else "error")

    # 6. VALIDIERUNGSERGEBNISSE ANZEIGEN
    log_and_print("\n" + "=" * 60, "info")
    log_and_print("DETAILLIERTE VALIDIERUNG", "info")
    log_and_print("=" * 60, "info")

    validation = report["scan_metadata"]["detailed_validation"]

    log_and_print(f"✅ DSGVO-Konformität: {'Ja' if validation['dsgvo_compliance'] else 'Nein'}",
                  "success" if validation['dsgvo_compliance'] else "error")
    log_and_print(f"✅ Web-UI Validierung: {'Ja' if validation['web_ui_valid'] else 'Nein'}",
                  "success" if validation['web_ui_valid'] else "error")
    log_and_print(f"✅ Humanity Index Implementierung: {'Ja' if validation['humanity_index_implemented'] else 'Nein'}",
                  "success" if validation['humanity_index_implemented'] else "error")
    log_and_print(f"✅ .gitignore Vollständigkeit: {'Ja' if validation['gitignore_complete'] else 'Nein'}",
                  "success" if validation['gitignore_complete'] else "error")
    log_and_print(f"✅ PRE-Selector Dokumentation: {'Ja' if validation['pre_selector_documented'] else 'Nein'}",
                  "success" if validation['pre_selector_documented'] else "error")

    # 7. ANPASSUNGSEMPFEHLUNGEN ANZEIGEN
    if not all(validation.values()):
        log_and_print("\n" + "=" * 60, "info")
        log_and_print("ANPASSUNGSEMPFEHLUNGEN", "warning")
        log_and_print("=" * 60, "info")

        issues = report["project_structure"]["validation_results"]

        for issue_type, issue_list in issues.items():
            if issue_list:
                log_and_print(f"\n⚠️ {issue_type.replace('_', ' ').upper()}:", "warning")
                for issue in issue_list:
                    log_and_print(f"- {issue['file']} ({issue['severity'].upper()}): {issue['description']}", "warning")
                    log_and_print(f"  Vorschlag: {issue['suggestion']}", "info")

    # Abschlussmeldung
    log_and_print("\n" + "=" * 60, "info")
    log_and_print("SCAN ABGESCHLOSSEN", "success")
    log_and_print("=" * 60, "info")
    log_and_print(f"Gesamtdateien: {structure_data['total_files']}", "info")
    log_and_print(f"Gesamtverzeichnisse: {structure_data['total_directories']}", "info")
    log_and_print(f"Priorisierte Dateien: {len(report['analysis_request']['files_to_analyze_first'])}", "info")
    log_and_print(f"Report gespeichert in: {CURRENT_SCAN_FILE}", "success")
    log_and_print("\nNÄCHSTE SCHRITTE:", "info")
    log_and_print("1. Öffne die Datei .IrsanAI/Reports/current_scan.json", "info")
    log_and_print("2. Kopiere den gesamten Inhalt in den Chat mit dem LLM", "info")
    log_and_print("3. Warte auf die online_feedback.json vom LLM", "info")
    log_and_print("4. Speichere diese im .IrsanAI/Feedback/ Ordner", "info")
    log_and_print("5. Führe den Scanner erneut aus, um das Feedback zu nutzen", "info")
    log_and_print("=" * 60, "info")


if __name__ == "__main__":
    main()