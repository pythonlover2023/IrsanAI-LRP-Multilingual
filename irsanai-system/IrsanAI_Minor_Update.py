# IrsanAI_Minor_Update.py
# IrsanAI-LRP v1.2 | Unique-Key: ENC(9f8a7b6c, AES-256) | Contributor: Qwen#5
# CHANGELOG: v1.0 - Erstellt für task_id=usr_20250828_1100_9f8a7b6c

# PATCH-INSTRUKTIONEN (AUTOMATISCH GENERIERT)
TARGET_FILE = "IrsanAI_project-run.py"
BACKUP_VERSION = "v2.2.1b"

# Sicherheitscheck vor Modifikation
VERIFICATION_HASH = "sha256:9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e"

# Präzise Änderungsanweisungen
PATCH_INSTRUCTIONS = [
    {
        "search_pattern": r"def validate_environment\(\):\s+.*?# SCHUTZSCHALTER",
        "replacement": "def validate_environment():\n    # NEU: Erweiterter Sicherheitscheck\n    if not check_hardware_compatibility():\n        raise HardwareIncompatibilityError()",
        "context_lines": 5,
        "max_occurrences": 1
    },
    {
        "search_pattern": r"except ValueError as e:\s+raise",
        "replacement": "except ValueError as e:\n    # IrsanAI-LRP | Feedback: Enable mit task_id=usr_20250828_1100_9f8a7b6c\n    raise",
        "context_lines": 3,
        "max_occurrences": 1
    }
]


def apply_patch():
    """Wendet den Patch auf die Zieldatei an"""
    import os
    import shutil
    import hashlib

    # Backup erstellen
    backup_path = f"{TARGET_FILE}.bak_{BACKUP_VERSION}"
    shutil.copy2(TARGET_FILE, backup_path)
    print(f"[PATCH] Backup erstellt: {backup_path}")

    # Datei lesen
    with open(TARGET_FILE, 'r') as f:
        content = f.read()

    # Hash-Prüfung
    current_hash = hashlib.sha256(content.encode()).hexdigest()
    if current_hash != VERIFICATION_HASH.split(':')[1]:
        print(
            f"[PATCH] FEHLER: Datei-Hash stimmt nicht überein! Erwartet: {VERIFICATION_HASH}, Gefunden: {current_hash}")
        print("[PATCH] ABBRUCH - möglicherweise wurden bereits Änderungen vorgenommen.")
        return False

    # Patch anwenden
    modified_content = content
    for patch in PATCH_INSTRUCTIONS:
        import re
        pattern = re.compile(patch["search_pattern"], re.DOTALL)
        matches = pattern.findall(modified_content)

        if matches and len(matches) <= patch["max_occurrences"]:
            modified_content = pattern.sub(patch["replacement"], modified_content)
            print(f"[PATCH] Erfolgreich ersetzt: {len(matches)}/{patch['max_occurrences']} Vorkommen")
        else:
            print(
                f"[PATCH] FEHLER: Keine Übereinstimmung für Pattern gefunden oder zu viele Vorkommen ({len(matches)}/{patch['max_occurrences']})")
            # Rollback zum Backup
            shutil.copy2(backup_path, TARGET_FILE)
            print(f"[PATCH] Rollback durchgeführt - Originalzustand wiederhergestellt")
            return False

    # Geänderte Datei speichern
    with open(TARGET_FILE, 'w') as f:
        f.write(modified_content)

    print(f"[PATCH] Erfolgreich angewendet! Neue Version: {TARGET_FILE}")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("IrsanAI MINOR UPDATE v1.0")
    print("=" * 60)
    success = apply_patch()
    if success:
        print("\nDer Patch wurde erfolgreich angewendet. Führen Sie IrsanAI_project-run.py erneut aus.")
    else:
        print("\nDer Patch konnte nicht angewendet werden. Überprüfen Sie die Fehlermeldung oben.")
    print("=" * 60)