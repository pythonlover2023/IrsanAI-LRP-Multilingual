#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
github_repo_preparer.py
Version: 1.0
Beschreibung: Intelligenter GitHub-Repository-Optimierer für IrsanAI-Projekte
Achtung: Dieses Skript analysiert das aktuelle Projektverzeichnis und erstellt
         einen Report, der hilft, das Projekt für GitHub bereitzumachen.

WICHTIGER HINWEIS:
Dieses Skript erfasst ausschließlich technische Projektinformationen, die für die
Vorbereitung eines GitHub-Repositories erforderlich sind. Es werden KEINE persönlichen Daten,
Nutzerverhalten oder sensible Informationen erfasst.

Datenschutz:
- Alle Pfade mit Benutzernamen werden maskiert (z.B. C:\\Users\\%username%\\...)
- Keine Netzwerkverbindungen während der Ausführung
- Vollständige Transparenz über erfasste Daten
"""

import os
import sys
import json
import re
import logging
import shutil
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Tuple, Optional

# ======================
# KONFIGURATION
# ======================
VERSION = "1.0"
OPTIMIZATION_REPORT_FILE = "IrsanAI_github_optimization_report.json"
LOG_FILE = "IrsanAI_github_optimizer.log"
ANONYMIZATION_SALT = "irsanai_optimizer_salt_2023"

# ======================
# LOGGING SETUP
# ======================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("IrsanAI_GitHub_Optimizer")


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
# DATENSCHUTZ-FUNKTIONEN
# ======================
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


def anonymize_path(path: str) -> str:
    """Anonymisiert einen Pfad durch Hashing mit Salt"""
    combined = f"{path}{ANONYMIZATION_SALT}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()[:16]


# ======================
# UMGEBUNGSANALYSE
# ======================
def analyze_project_structure(root_dir: str) -> Dict[str, Any]:
    """Analysiert die Projektstruktur und erstellt einen Report"""
    log_and_print(f"[ANALYZE] Analysiere Projektstruktur: {root_dir}")

    # Maskiere den Projekt-Root für den Report
    safe_root_dir = mask_personal_data(root_dir)

    total_files = 0
    total_directories = 0
    file_types = {}
    ignored_files = 0
    ignored_directories = 0
    suspicious_files = []

    # Typische Dateien/Ordner, die NICHT in GitHub gehören
    IGNORE_PATTERNS = [
        # IDE-spezifische Dateien
        r'\.idea\/.*',  # PyCharm
        r'\.vscode\/.*',  # VS Code
        r'\.project',  # Eclipse
        r'\.c9\/.*',  # Cloud9
        r'\.metadata\/.*',  # Eclipse

        # Build/Cache-Dateien
        r'__pycache__\/.*',
        r'\.pytest_cache\/.*',
        r'\.mypy_cache\/.*',
        r'build\/.*',
        r'dist\/.*',
        r'\.egg-info\/.*',

        # Virtuelle Umgebungen
        r'venv\/.*',
        r'env\/.*',
        r'virtualenv\/.*',
        r'\.venv\/.*',

        # Temporäre Dateien
        r'\.tmp\/.*',
        r'\.temp\/.*',
        r'\.swp$',
        r'\.swo$',
        r'~$',

        # Betriebssystem-spezifische Dateien
        r'Desktop\.ini$',
        r'Thumbs\.db$',
        r'\.DS_Store$',

        # Lokale Konfigurationsdateien
        r'\.env$',
        r'\.env\.local$',
        r'\.env\.development$',
        r'\.env\.production$',

        # Log-Dateien
        r'\.logs?\/.*',
        r'\.log$',

        # Lokale Backups
        r'\.bak$',
        r'\.backup$',
        r'\.old$',

        # PyCharm-spezifische Dateien
        r'\.cache\/.*',
        r'\.local\/JetBrains\/.*',
        r'cpython-cache\/.*',

        # Andere Entwicklungsumgebungen
        r'\.ipynb_checkpoints\/.*',
        r'\.jupyter\/.*',

        # IrsanAI-spezifische temporäre Dateien
        r'IrsanAI_github_optimizer\.log$',
        r'IrsanAI_scanner\.log$'
    ]

    # Typische Dateien/Ordner, die in GitHub BELIEBEN sollen
    KEEP_PATTERNS = [
        r'^\.gitignore$',
        r'^README\.md$',
        r'^LICENSE$',
        r'^requirements\.txt$',
        r'^pyproject\.toml$',
        r'^setup\.py$',
        r'^IrsanAI_.*\.py$',
        r'^\.IrsanAI\/\.gitkeep$',  # Nur .gitkeep im .IrsanAI-Verzeichnis
        r'^\.IrsanAI\/README\.md$',  # Nur README.md im .IrsanAI-Verzeichnis
        r'^docs\/.*',
        r'^tests\/.*',
        r'^game_assets\/.*',
        r'^\.github\/.*',
        r'^web-tool\/.*',
        r'^lrp-protocol\/.*'
    ]

    # IrsanAI-spezifische Regeln für die Bewertung
    IRSANAI_RULES = [
        {
            "id": "rule_001",
            "name": "Korrekte .IrsanAI-Struktur",
            "description": "Das .IrsanAI-Verzeichnis sollte nur .gitkeep und README.md enthalten",
            "pattern": r'^\.IrsanAI$',
            "check_func": lambda path, is_dir, content: is_dir and (
                    len([f for f in os.listdir(path) if not f.startswith('.')]) == 0 or
                    (".gitkeep" in os.listdir(path) and "README.md" in os.listdir(path))
            ),
            "severity": "warning",
            "recommendation": "Entferne alle Unterordner aus .IrsanAI/ außer .gitkeep und README.md"
        },
        {
            "id": "rule_005",
            "name": "Korrekte .gitignore",
            "description": ".gitignore sollte kritische Einträge enthalten",
            "pattern": r'^\.gitignore$',
            "check_func": lambda path, is_dir, content: not is_dir and (
                    content is None or all(
                pattern in content for pattern in [
                    "*.pyc", "__pycache__", ".idea", ".venv",
                    "*.log", "*.tmp", "*.bak", "*.backup", "*.old", ".DS_Store"
                ]
            )
            ),
            "severity": "error",
            "recommendation": "Erweitere .gitignore mit kritischen Einträgen"
        },
        {
            "id": "rule_007",
            "name": "Keine IDE-spezifischen Dateien",
            "description": "Keine IDE-spezifischen Dateien im Repository",
            "pattern": r'.*',
            "check_func": lambda path, is_dir, content: not any(
                re.match(pattern, path) for pattern in IGNORE_PATTERNS
            ),
            "severity": "error",
            "recommendation": "Entferne IDE-spezifische Dateien"
        }
    ]

    directory_structure = {}
    file_analysis = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Berechne relativen Pfad für die Struktur
        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == ".":
            rel_path = ""

        # Verarbeite Verzeichnisse
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            rel_dir_path = os.path.join(rel_path, dirname) if rel_path else dirname

            # Prüfe auf Ignorierung
            ignore = False
            for pattern in IGNORE_PATTERNS:
                if re.match(pattern, rel_dir_path):
                    ignore = True
                    break

            if not ignore:
                # Füge zum Verzeichnisbaum hinzu
                current = directory_structure
                parts = rel_dir_path.split(os.sep)
                for part in parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
            else:
                ignored_directories += 1

        # Verarbeite Dateien
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_file_path = os.path.join(rel_path, filename) if rel_path else filename

            # Prüfe auf Ignorierung
            ignore = False
            for pattern in IGNORE_PATTERNS:
                if re.match(pattern, rel_file_path):
                    ignore = True
                    break

            if not ignore:
                # Zähle Dateitypen
                _, ext = os.path.splitext(filename)
                file_types[ext] = file_types.get(ext, 0) + 1
                total_files += 1

                # Analysiere Dateiinhalt
                try:
                    file_size = os.path.getsize(full_path)
                    anonymized_id = anonymize_path(full_path)

                    # Nur kleine Dateien analysieren, um Performance zu gewährleisten
                    content_preview = ""
                    if file_size < 10000:  # Nur Dateien < 10KB
                        try:
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(500)  # Nur die ersten 500 Zeichen
                                content_preview = content.replace('\n', ' ').strip()
                                if len(content) > 500:
                                    content_preview += "..."
                        except:
                            pass

                    file_analysis[rel_file_path] = {
                        "type": "Unbekannt",
                        "size": file_size,
                        "anonymized_id": anonymized_id,
                        "content_preview": content_preview
                    }

                    # Bestimme Dateityp basierend auf Inhalt
                    if filename.endswith('.py'):
                        file_analysis[rel_file_path]["type"] = "Python"
                    elif filename.endswith('.md'):
                        file_analysis[rel_file_path]["type"] = "Markdown"
                    elif filename.endswith('.json'):
                        file_analysis[rel_file_path]["type"] = "JSON"
                    elif filename.endswith('.html'):
                        file_analysis[rel_file_path]["type"] = "HTML"
                    elif filename.endswith('.js'):
                        file_analysis[rel_file_path]["type"] = "JavaScript"
                    elif filename.endswith('.txt'):
                        file_analysis[rel_file_path]["type"] = "Text"
                except Exception as e:
                    log_and_print(f"[ANALYZE] Fehler bei Dateianalyse {rel_file_path}: {str(e)}", "warning")
            else:
                ignored_files += 1

    total_directories = sum(1 for _, dirnames, _ in os.walk(root_dir) for _ in dirnames)

    # Prüfe Regeln
    rule_violations = []
    for rule in IRSANAI_RULES:
        if re.match(rule["pattern"], ""):  # Prüfe auf Root-Verzeichnis
            if not rule["check_func"](root_dir, True, ""):
                rule_violations.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "path": "",
                    "severity": rule["severity"],
                    "recommendation": rule["recommendation"]
                })
        else:
            for dirpath, _, filenames in os.walk(root_dir):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_dir)

                    if re.match(rule["pattern"], rel_path):
                        try:
                            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            if not rule["check_func"](rel_path, False, content):
                                rule_violations.append({
                                    "rule_id": rule["id"],
                                    "rule_name": rule["name"],
                                    "path": rel_path,
                                    "severity": rule["severity"],
                                    "recommendation": rule["recommendation"]
                                })
                        except:
                            pass

    # Erstelle Recommendations
    recommendations = {
        "gitignore_entries": [".idea/", "IrsanAI_github_optimizer.log"],
        "delete_candidates": [],
        "rename_candidates": [],
        "move_candidates": [],
        "create_candidates": [],
        "fix_candidates": [
            {"path": ".gitignore", "reason": "Wichtige Projektdatei", "severity": "low"},
            {"path": "README.md", "reason": "Wichtige Projektdatei", "severity": "low"},
            {"path": ".github", "reason": "Wichtiges Projektverzeichnis", "severity": "low"},
            {"path": ".IrsanAI", "reason": "Wichtiges Projektverzeichnis", "severity": "low"},
            {"path": "lrp-protocol", "reason": "Wichtiges Projektverzeichnis", "severity": "low"},
            {"path": "web-tool", "reason": "Wichtiges Projektverzeichnis", "severity": "low"}
        ],
        "rule_violations": rule_violations,
        "additional_notes": []
    }

    # Generiere Report
    report = {
        "scan_timestamp": datetime.now().isoformat(),
        "optimizer_version": VERSION,
        "project_root": safe_root_dir,  # MASKIERTER ROOT-PFAD!
        "total_files": total_files,
        "total_directories": total_directories,
        "ignored_files": ignored_files,
        "ignored_directories": ignored_directories,
        "kept_files": total_files,
        "kept_directories": total_directories,
        "file_types": file_types,
        "suspicious_files": suspicious_files,
        "recommendations": recommendations,
        "directory_structure": directory_structure,
        "file_analysis": file_analysis
    }

    return report


# ======================
# OPTIMIERUNGSFUNKTIONEN
# ======================
def generate_gitignore_content(report: Dict[str, Any]) -> str:
    """Generiert den Inhalt für eine .gitignore-Datei"""
    content = f"""# Generated by IrsanAI GitHub Repository Optimizer v{VERSION}
# Do not edit manually - this file is automatically generated

# IDE-spezifische Dateien
.idea/
.vscode/
.project
.c9/
.metadata/

# Build/Cache-Dateien
__pycache__/
*.pyc
*.pyo
*.pyd
*.typed
build/
dist/
*.egg-info/
.pytest_cache/
.mypy_cache/

# Virtuelle Umgebungen
venv/
env/
virtualenv/
.venv/

# Temporäre Dateien
*.tmp
*.temp
*.swp
*.swo
*~
Thumbs.db
.DS_Store

# Lokale Konfigurationsdateien
.env
.env.local
.env.*.local

# Log-Dateien
*.log

# Lokale Backups
*.bak
*.backup
*.old

# PyCharm-spezifische Dateien
.cache/
.cpython-cache/
.local/JetBrains/

# Andere Entwicklungsumgebungen
.ipynb_checkpoints/
.jupyter/

# IrsanAI-spezifische temporäre Dateien
IrsanAI_github_optimizer.log
IrsanAI_scanner.log
"""
    return content


def apply_recommendations(report: Dict[str, Any]) -> List[str]:
    """Wendet die Recommendations auf das Projekt an"""
    actions = []

    # Lösche temporäre Dateien
    for candidate in report["recommendations"]["delete_candidates"]:
        path = os.path.join(report["project_root"], candidate["path"])
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                actions.append(f"Gelöscht: Verzeichnis {candidate['path']}")
            else:
                os.remove(path)
                actions.append(f"Gelöscht: Datei {candidate['path']}")

    # Erstelle .gitignore, falls nötig
    gitignore_path = os.path.join(report["project_root"], ".gitignore")
    try:
        with open(gitignore_path, 'w') as f:
            f.write(generate_gitignore_content(report))

        if not os.path.exists(gitignore_path):
            actions.append("Erstellt: .gitignore")
        else:
            actions.append("Aktualisiert: .gitignore - Vollständiger Inhalt geschrieben")
    except Exception as e:
        log_and_print(f"[ERROR] Fehler beim Schreiben von .gitignore: {str(e)}", "error")

    # Korrigiere .IrsanAI-Struktur
    irsanai_path = os.path.join(report["project_root"], ".IrsanAI")
    if os.path.exists(irsanai_path) and os.path.isdir(irsanai_path):
        # Entferne alle Unterordner, behalte nur .gitkeep und README.md
        for item in os.listdir(irsanai_path):
            item_path = os.path.join(irsanai_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                actions.append(f"Gelöscht: Unterordner {os.path.join('.IrsanAI', item)}")

    return actions


# ======================
# HAUPTFUNKTION
# ======================
def main():
    """Hauptausführung des Skripts"""
    log_and_print("=" * 60)
    log_and_print("IrsanAI GITHUB REPOSITORY OPTIMIZER v1.0")
    log_and_print("=" * 60)

    # Ermittle aktuelles Verzeichnis (UNMASKIERT für Dateioperationen)
    real_project_root = os.path.abspath(os.getcwd())

    # KRITISCH: IMMER ZUERST .gitignore AKTUALISIEREN - VOR DER ANALYSE!
    # WICHTIG: Verwende den ECHTEN, UNMASKIERTEN Pfad für Dateioperationen
    gitignore_path = os.path.join(real_project_root, ".gitignore")
    try:
        with open(gitignore_path, 'w') as f:
            f.write(generate_gitignore_content({
                "project_root": real_project_root,
                "file_types": {}
            }))
        log_and_print(f"[FIX] .gitignore wurde vor Analyse aktualisiert")
    except Exception as e:
        log_and_print(f"[WARNING] .gitignore konnte nicht vor Analyse aktualisiert werden: {str(e)}", "warning")

    try:
        # Analysiere Projektstruktur MIT MASKIERTEM PFAD NUR FÜR DEN REPORT
        log_and_print(f"[ANALYZE] Starte Analyse des Projekts: {real_project_root}")
        report = analyze_project_structure(real_project_root)

        # Speichere Report
        with open(OPTIMIZATION_REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)

        log_and_print(f"\n[REPORT] Erfolgreich! Optimierungs-Report gespeichert in: {OPTIMIZATION_REPORT_FILE}")

        # Wende Recommendations an
        log_and_print("\n[OPTIMIZE] Wende Optimierungsempfehlungen an...")
        actions = apply_recommendations(report)

        for action in actions:
            log_and_print(f"- {action}")

        # Zusammenfassung anzeigen
        log_and_print("\n" + "=" * 60)
        log_and_print("OPTIMIERUNGS-ZUSAMMENFASSUNG")
        log_and_print("=" * 60)
        log_and_print(f"Gesamtdateien: {report['total_files']}")
        log_and_print(f"Gesamtverzeichnisse: {report['total_directories']}")
        log_and_print(f"Ignorierte Dateien: {report['ignored_files']}")
        log_and_print(f"Ignorierte Verzeichnisse: {report['ignored_directories']}")

        if report['recommendations']['rule_violations']:
            log_and_print("\nGEFUNDENE REGELVERSTÖSSE:")
            for violation in report['recommendations']['rule_violations']:
                severity = violation['severity'].upper()
                log_and_print(f"- [{severity}] {violation['rule_name']}: {violation['recommendation']}")
        else:
            log_and_print("\nKEINE REGELVERSTÖSSE GEFUNDEN - Projekt ist GitHub-fähig!")

        log_and_print("=" * 60)
        log_and_print("Der nächste Schritt: Führe git add . und git commit aus,")
        log_and_print("um das optimierte Projekt in GitHub zu pushen.")
        log_and_print("=" * 60)

    except Exception as e:
        log_and_print(f"[ERROR] Unvorhergesehener Fehler: {str(e)}", "critical")
        log_and_print("[ERROR] Bitte sende den Log-File an support@irsanai.example für Analyse.", "critical")
        sys.exit(1)


if __name__ == "__main__":
    main()