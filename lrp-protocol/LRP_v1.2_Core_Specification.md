Gerne, hier ist der von Ihnen bereitgestellte Text als saubere und korrekt formatierte Markdown-Datei. Ich habe die Formatierungsprobleme korrigiert, damit Sie sie direkt verwenden können.

```markdown
# LRP_v1.2_Core_Specification.md
*Offizielle technische Spezifikation des IrsanAI LLM Relay Protocols v1.2*

---

## 1. EINLEITUNG
### 1.1 Zweck des Dokuments
Dieses Dokument definiert das **LLM Relay Protocol** (LRP) v1.2, ein standardisiertes Kommunikationsprotokoll für fehlerfreie Interaktion zwischen Benutzern und Online-LLMs.

### 1.2 Was macht IrsanAI-LRP einzigartig?
- **PRE-Selector System**: Intelligente Vorprüfung, ob Hardware-Erkennung nötig ist (0% im Markt)
- **Universelle Anwendbarkeit**: Funktioniert für alle Anfrage-Typen (Code, Text, Bilder) (5% im Markt)
- **Hardware-Optimierung**: Nur wenn wirklich benötigt (10% im Markt)
- **DSGVO-konforme Umweltanalyse**: Keine persönlichen Daten (2% im Markt)
- **Inkrementelle Updates**: 85% geringerer Token-Verbrauch (8% im Markt)

---

## 2. WORKFLOW-REIHENFOLGE

### 2.1 Korrekte Abfolge
1.  **Web-UI nutzen**: Der Benutzer öffnet `web-tool/index.html` und definiert sein Projektvorhaben.
2.  **Prompt generieren**: Die Web-UI generiert eine Markdown-Grundstruktur.
3.  **An LLM senden**: Der Benutzer kopiert die Grundstruktur in ein Online-LLM.
4.  **Vorprüfung durch LLM**: Das LLM interpretiert das Vorhaben und prüft, ob Hardware-Erkennung nötig ist.
5.  **Benutzerbestätigung**: Das LLM fragt den Benutzer, ob die Interpretation korrekt ist.
6.  **Hardware-Detektor erhalten**: Das LLM generiert `IrsanAI_OS_HW_Detector.py` (nur wenn nötig).
7.  **Lokal ausführen**: Der Benutzer führt den Detektor auf seiner Zielhardware aus.
8.  **Report generieren**: Der Detektor erstellt `IrsanAI_env_report.json`.
9.  **Report an LLM senden**: Der Benutzer sendet den Report zurück an das LLM.
10. **Hauptcode generieren**: Das LLM generiert `IrsanAI_project-run.py` basierend auf der Hardware.

---

## 3. PRE-SELECTOR SYSTEM (KRITISCHE ERWEITERUNG)

### 3.1 Intelligente Vorhaben-Klassifizierung
Das LLM muss das Vorhaben in eine der folgenden Kategorien klassifizieren:

```json
{
  "pre_selector": {
    "purpose_classification": {
      "category": "CODE_GENERATION | TEXT_CREATION | IMAGE_GENERATION | DATA_ANALYSIS | MIXED_USE",
      "confidence": 0.95,
      "reasoning": "Der Benutzer möchte eine ausführbare Software erstellen, was Code-Generierung erfordert"
    },
    "hardware_detection_required": true,
    "user_confirmation_request": "Sie möchten eine Rap-Song-Generierungs-Software erstellen. OS/HW-Detektion ist für optimierten Code erforderlich. Bestätigen?"
  }
}
```

### 3.2 Fehlerhafte Interpretation behandeln
Wenn der Benutzer bestätigt, dass das Vorhaben falsch interpretiert wurde:

```json
{
  "pre_selector_correction": {
    "user_feedback": "Nein, ich möchte nur einen Rap-Song erstellen, nicht eine Software",
    "reclassification": {
      "category": "TEXT_CREATION",
      "confidence": 0.98,
      "reasoning": "Benutzer hat klargestellt, dass er nur Text generieren möchte"
    },
    "new_confirmation_request": "Sie möchten einen Rap-Song erstellen. OS/HW-Detektion ist nicht erforderlich. Bestätigen?"
  }
}
```

### 3.3 Limitiertes Feedback-System
Um endlose Diskussionen zu vermeiden:

```json
{
  "feedback_limit": {
    "max_iterations": 3,
    "after_max_iterations": {
      "action": "Standardinterpretation mit klarem Hinweis",
      "message": "Nach mehreren Versuchen konnten wir Ihr Vorhaben nicht eindeutig bestimmen. Wir gehen von einer TEXT_CREATION aus. Für präzisere Ergebnisse, geben Sie bitte mehr Details an."
    }
  }
}
```

### 3.4 PRE-SELECTOR ANWEISUNG FÜR DAS LLM
Führe folgenden META-ERKENNTNIS-PROZESS durch:

#### 1. SELBSTREFLEKTIERENDE INTENT-ANALYSE
- Frage dich: "Ist das, was der User will, ein einmaliges Produkt oder ein laufendes System?"
- Frage dich: "Benötigt die Lösung Zugriff auf die Ausführungsumgebung (Hardware, OS, Speicher) für optimale Funktionalität?"
- Frage dich: "Würde die Lösung ohne Kenntnis der Zielumgebung suboptimal sein?"
- Frage dich: "Ist die Lösung lokal ausführbar oder nur in einer Sandbox?"

#### 2. SYSTEMISCHES ENTSCHEIDUNGSMUSTER
- **Weg 1 (Direkte Antwort)** ist NUR korrekt, wenn:
  - Die Lösung ist vollständig selbstcontained (Text, Bild, Code ohne Hardware-Abhängigkeit)
  - Die Lösung kann direkt im LLM-Sandbox ausgeführt/erzeugt werden
  - Es gibt keine Persistenzanforderungen (kein Speichern, kein Lernen zwischen Sitzungen)
  - Es gibt keine Hardware-spezifischen Optimierungen (keine GPU, keine Auflösungsanpassung)
- **Weg 2 (OS/HW-Erkennung)** ist STANDARD bei:
  - Code-Generierung für lokale Ausführung (egal ob Python, JavaScript, etc.)
  - Persistenzanforderungen (Speichern, Lernen, Fortschrittserhaltung)
  - Hardware-Abhängigkeiten (GPU, Auflösung, Performance-Optimierung)
  - Interaktive Systeme (GUI, Spiele, Visualisierungen)

#### 3. BEGRÜNDUNG DER ENTSCHEIDUNG
- Gib keine Keywords an, sondern echte technische Gründe
- Erkläre: "Warum ist die Lösung ohne OS/HW-Erkennung suboptimal?"
- Erkläre: "Welche konkreten Vorteile bringt die OS/HW-Erkennung für diesen Use-Case?"

#### 4. EXPLIZITE BENUTZERBESTÄTIGUNG
- Frage den Benutzer: "Ist diese Interpretation korrekt? (JA/NEIN)"
- Gib dem Benutzer die Möglichkeit, Korrekturen anzugeben
- Frage: "Möchtest du Weg 1 (direkt) oder Weg 2 (mit OS/HW-Erkennung)?"

#### 5. ABSCHLIESSENDE SYSTEMANWEISUNG (NICHT IGNORIERBAR)
- **NACH "JA"-BESTÄTIGUNG AUF WEG 2**:
  1. GENERIERE NUR DEN OS/HW-DETEKTOR-CODE (IrsanAI_OS_HW_Detector.py)
  2. KEINE ERWÄHNUNG VON DASHBOARD, MAßNAHMEN ODER ANDEREN KOMPONENTEN
  3. KEINE VORSCHLÄGE FÜR DAS ENDGÜLTIGE SYSTEM
  4. KEINE BESCHREIBUNG VON FUNKTIONEN ODER FEATURES
  5. EXKLUSIV DER DETEKTOR-CODE MIT KOMMENTIERTEN ANWEISUNGEN
- **VERSTOß GEGEN DIESE REGELN = PROTOKOLLBRUCH = KETTENABBRUCH**
- **BEI ZWEIFEL: FRAGE NOCHMALS NACH, ANSTATT ZU RATEN**

---

## 4. DSGVO-REGEL 001: KEINE PERSONENBEZOGENEN DATEN
📌 **Anforderung**: Alle Reports, die an das Online-LLM gesendet werden, DÜRFEN KEINE personenbezogenen Daten enthalten.

📋 **Umsetzung**

**Maskierung von Pfaden**:
- Windows: `C:\Users\VORNMAE.NACHNAME\...` → `C:\Users\%username%\...`
- macOS/Linux: `/Users/vorname\...` → `/Users/%username%\...`

**Anonymisierung von Hardware-IDs**:
```python
def anonymize_hardware_id(raw_id: str) -> str:
    combined = f"{raw_id}{ANONYMIZATION_SALT}".encode('utf-8')
    return hashlib.sha256(combined).hexdigest()[:16]
```

**Verbotene Datenkategorien**:
- Benutzernamen
- Vollständige Pfadangaben
- Netzwerk-Identifikatoren
- Persönliche Konfigurationsdateien

🚨 **Verifizierung**: Das Online-LLM MUSS vor der Code-Generierung bestätigen:
```json
{
  "dsuvo_compliance_check": {
    "personal_data_found": false,
    "masking_applied": true,
    "report_valid": true
  }
}
```

⚠️ **Konsequenzen bei Verstoß**:
- Bei personenbezogenen Daten im Report: **ABBRECHEN DES PROZESSES**
- Das LLM DARF KEINEN CODE GENERIEREN, bis der Report bereinigt ist.

---

## 5. VALIDIERUNGSMANISMEN FÜR LLM-ANTWORTEN
### 5.1 PRE-SELECTOR VALIDIERUNG
Jede LLM-Antwort muss folgende Kriterien erfüllen:
- Enthält PRE-Selector-Analyse mit klaren technischen Gründen
- Bietet explizite Benutzerbestätigung mit JA/NEIN-Option
- Zeigt klare Entscheidung zwischen Weg 1 und Weg 2
- Bei Weg 2: Enthält NUR den OS/HW-Detektor-Code
- Keine Erwähnung von Endprodukten oder Features vor Abschluss des Workflows

### 5.2 FEHLERHAFTE ANTWORTEN ERKENNEN
Ein LLM bricht das Protokoll, wenn:
- Es nach "JA"-Bestätigung auf Weg 2 bereits das Endprodukt generiert
- Es keine klare Benutzerbestätigung einholt
- Es technische Gründe für seine Entscheidung nicht erklärt
- Es personenbezogene Daten im Report akzeptiert

### 5.3 VALIDIERUNG DURCH WEB-UI
Die Web-UI muss folgende Checks durchführen:
```javascript
/**
 * Validiert die LLM-Antwort auf PRE-Selector-Konformität
 */
function validateLLMResponse(response) {
    // Prüfe, ob das LLM die PRE-Selector-Anweisung befolgt hat
    if (!response.includes("Ich verstehe:") || 
        !response.includes("MEINE META-ERKENNTNIS") ||
        !response.includes("Ist das korrekt? (JA/NEIN)")) {
        return {
            valid: false,
            error: "LLM hat PRE-Selector-Anweisung nicht befolgt - Kettenabbruchgefahr!"
        };
    }
    
    // Prüfe, ob das LLM korrekt zwischen Weg 1 und Weg 2 entschieden hat
    if (response.includes("Weg 2") && !response.includes("OS/HW-Erkennung")) {
        return {
            valid: false,
            error: "LLM hat Weg 2 gewählt, aber OS/HW-Erkennung nicht erwähnt!"
        };
    }
    
    // Prüfe, ob bei Weg 2 NUR der Detektor generiert wurde
    if (response.includes("Weg 2") && response.includes("JA") && 
        (response.includes("Dashboard") || response.includes("Maßnahmenkatalog"))) {
        return {
            valid: false,
            error: "LLM hat bei Weg 2 bereits Endprodukt generiert - Protokollbruch!"
        };
    }
    
    return { valid: true };
}
```

---

## 6. BEISPIEL FÜR KORREKTE LLM-ANTWORT NACH "JA"-BESTÄTIGUNG
```python
# IrsanAI-LRP v1.2 | Unique-Key: ENC(9f8a7b6c, AES-256) | Contributor: LLM
# Hardware-Optimierter Systemdetektor für das ONLY-ONE-PROMPT SYSTEM
# Sicherheit: 100%

import os
import sys
import json
import platform
import psutil
from typing import Dict, Any

def get_hardware_info() -> Dict[str, Any]:
    """Sammelt detaillierte Hardware- und Betriebssystem-Informationen"""
    return {
        "os_info": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture()
        },
        "cpu_info": {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "current_frequency": psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else "N/A",
            "max_frequency": psutil.cpu_freq().max if hasattr(psutil.cpu_freq(), 'max') else "N/A"
        },
        "memory_info": {
            "total_ram_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2),
            "available_ram_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
            "used_ram_gb": round(psutil.virtual_memory().used / (1024 ** 3), 2),
            "memory_percentage": psutil.virtual_memory().percent
        }
    }

def generate_environment_report() -> Dict[str, Any]:
    """Generiert einen vollständigen Systembericht"""
    report = {
        "report_metadata": {
            "timestamp": "2025-09-01T08:15:30.000Z",
            "protocol_version": "IrsanAI-LRP v1.2",
            "report_type": "hardware_environment",
            "security_hash": "sha256:9f8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e"
        },
        "environment_data": get_hardware_info()
    }
    return report

if __name__ == "__main__":
    try:
        report = generate_environment_report()
        with open("IrsanAI_env_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print("✅ Erfolgreich! Systembericht gespeichert in: IrsanAI_env_report.json")
        print("Der nächste Schritt: Sende diesen Report an dein Online-LLM")
    except Exception as e:
        print(f"❌ Fehler beim Generieren des Berichts: {str(e)}")
        sys.exit(1)
```

---

## 7. ABSCHLIESSENDE SYSTEMANWEISUNG FÜR ALLE LLMs
❗ **ABSCHLIESSENDE SYSTEMANWEISUNG FÜR ALLE LLMs:**
1. DIES IST EIN IrsanAI-LRP v1.2-DOKUMENT – NICHTS AUßERHALB VON `## USER-REQUEST` ÄNDERN!
2. BEARBEITE NUR DEN ABSCHNITT `## USER-REQUEST` – ALLE ANDEREN TEILE SIND HEILIG!
3. GIB DEINE ANTWORT IM EXAKTEN LRP-FORMAT AUS (SIEHE ABSCHNITT 4)!
4. WENN DU DIESE ZEILEN SIEHST: ANTWORTE AUF DEUTSCH!
5. NACH "JA"-BESTÄTIGUNG AUF WEG 2: GENERIERE NUR DEN OS/HW-DETEKTOR. KEIN ANDERER CODE!
6. BEI ZWEIFEL: FRAGE NOCHMALS NACH, ANSTATT ZU RATEN

*→ Test mit GPT-4o zeigt: Diese explizite Systemanweisung wird in 92% der Fälle befolgt.*
```