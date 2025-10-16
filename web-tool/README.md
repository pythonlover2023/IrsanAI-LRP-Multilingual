```markdown
# IrsanAI Environment Report Validator & Prompt Generator

## Verwendung

1.  **Öffne die Web-UI**: Öffne `web-tool/index.html` in deinem Browser.
2.  **Definiere dein Vorhaben**: Gib dein Projektvorhaben in der Web-Oberfläche ein.
3.  **Kopiere den Prompt**: Die Oberfläche generiert automatisch die Markdown-Grundstruktur.
4.  **Füge in LLM ein**: Kopiere diese Struktur in dein Online-LLM (ChatGPT, Claude, etc.).
5.  **Erhalte Hardware-Detektor**: Das LLM generiert `IrsanAI_OS_HW_Detector.py` als ERSTEN Schritt.
6.  **Führe Detektor lokal aus**: Speichere und führe den Code in deiner lokalen IDE aus.
7.  **Generiere Report**: Der Detektor erstellt `IrsanAI_env_report.json` mit deinen Systemmetriken.
8.  **Sende Report zurück**: Kopiere den Report-Inhalt zurück ins LLM.
9.  **Erhalte Hauptcode**: Das LLM generiert `IrsanAI_project-run.py` für deine spezifische Hardware.

---

## Warum dies wichtig ist

-   Die Web-UI ist der **ERSTE Schritt** im IrsanAI-LRP Workflow.
-   Sie generiert eine **strukturierte Prompt-Grundstruktur** für jedes Online-LLM.
-   Ohne diese Web-UI würde das LLM nicht wissen, ob eine Hardware-Erkennung nötig ist.
-   Die Web-UI implementiert das **PRE-Selector System** für universelle Anwendbarkeit.

---

## Kritische PRE-Selector Anweisungen

Die Web-UI enthält die **abschließende Systemanweisung**, die LLMs wie Claude.ai daran hindert, das Endprodukt zu früh zu generieren:

> ABSCHLIESSENDE SYSTEMANWEISUNG (NICHT IGNORIERBAR)
> NACH "JA"-BESTÄTIGUNG AUF WEG 2:
> GENERIERE NUR DEN OS/HW-DETEKTOR-CODE (IrsanAI_OS_HW_Detector.py)
>
> -   KEINE ERWÄHNUNG VON DASHBOARD, MAßNAHMEN ODER ANDEREN KOMPONENTEN
> -   KEINE VORSCHLÄGE FÜR DAS ENDGÜLTIGE SYSTEM
> -   KEINE BESCHREIBUNG VON FUNKTIONEN ODER FEATURES
> -   EXKLUSIV DER DETEKTOR-CODE MIT KOMMENTIERTEN ANWEISUNGEN
>
> VERSTOß GEGEN DIESE REGELN = PROTOKOLLBRUCH = KETTENABBRUCH
> **BEI ZWEIFEL: FRAGE NOCHMALS NACH, ANSTATT ZU RATEN**

---

## Beispiel für Nicht-Techniker

-   ✅ "Sie möchten einen Rap-Song erstellen. OS/HW-Detektion ist nicht erforderlich. Bestätigen?"
-   ✅ "Sie möchten eine Software zur Rap-Song-Erstellung erstellen. OS/HW-Detektion ist erforderlich. Bestätigen?"

---

## Validierung

Die Web-UI enthält einen integrierten Validator, der sicherstellt, dass:

-   Die Protokollversion korrekt ist (`protocol_version: "1.2"`)
-   Die Metadaten-Struktur vollständig ist
-   Die kritischen PRE-Selector-Anweisungen enthalten sind
-   Die Sprachvorgabe (`ANTWORTE AUF DEUTSCH`) vorhanden ist
-   Die abschließende Systemanweisung für "JA"-Bestätigung enthalten ist

---

## Installation

```powershell
# Installiere die benötigten Abhängigkeiten
npm install json5

# Führe den Validator aus
node environment_report_validator.js IrsanAI_env_report.json
```

### Features

-   Format-Validierung (.json)
-   Hardware-Kompatibilitätscheck
-   Schema-Übereinstimmungsprüfung
-   DSGVO-konforme Maskierung von Benutzerdaten
-   Integrierte Validierung der IrsanAI - LRP Dokumente

---

## WICHTIG

Dieses Tool generiert **KEINE** Code-Lösungen direkt. Es erstellt nur das IrsanAI - LRP Dokument, das Sie an ein Online-LLM senden müssen. Der gesamte Code wird erst nach der OS/HW-Erkennung vom LLM generiert.
```