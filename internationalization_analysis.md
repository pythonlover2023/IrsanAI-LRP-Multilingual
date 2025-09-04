# IrsanAI-LRP Internationalisierung - Analyse der sprachabhängigen Inhalte

## Identifizierte sprachabhängige Elemente

### 1. HTML-Struktur und Meta-Informationen
- `<html lang="de">` - Sprache ist fest auf Deutsch eingestellt
- `<title>IrsanAI-LRP v1.2 – ONLY-ONE-PROMPT GENERATOR</title>` - Deutscher Titel
- Meta-Beschreibungen und Keywords fehlen, müssten mehrsprachig ergänzt werden

### 2. Benutzeroberfläche (UI-Texte)
- Hauptüberschrift: "IrsanAI-LRP v1.2 – ONLY-ONE-PROMPT GENERATOR"
- Anweisungstext: "So funktioniert das ONLY-ONE-PROMPT SYSTEM:"
- Formular-Labels: "Beschreibe dein Projektvorhaben:"
- Button-Texte: "IrsanAI - LRP Dokument generieren", "In Zwischenablage kopieren", "Zurücksetzen", "Als Markdown herunterladen", "IrsanAI - LRP Dokument Validieren"
- Placeholder-Text: "Beschreibe, was du erreichen möchtest..."
- Warnhinweise und Statusmeldungen

### 3. Anweisungstexte und Hilfetexte
- Umfangreiche Anweisungen in deutscher Sprache
- Schritt-für-Schritt-Anleitungen
- Warnhinweise und wichtige Notizen
- Validierungsfehlermeldungen

### 4. JavaScript-generierte Inhalte
- Dynamisch generierte LRP-Dokumente
- Fehlermeldungen und Validierungstexte
- Benachrichtigungen und Statusmeldungen
- Zeitstempel und Metadaten-Beschreibungen

### 5. Protokoll-spezifische Inhalte
- Das generierte LRP-Dokument enthält deutsche Anweisungen für LLMs
- Metadaten-Beschreibungen
- Systemanweisungen und Protokollregeln
- Validierungsregeln und Compliance-Checks

## Herausforderungen bei der Internationalisierung

### Technische Herausforderungen
1. **Dynamische Inhalte**: Große Teile des Textes werden dynamisch in JavaScript generiert
2. **Protokoll-Konsistenz**: Das LRP-Protokoll muss in allen Sprachen funktional identisch bleiben
3. **Validierung**: Validierungslogik muss sprachunabhängig funktionieren
4. **Metadaten**: Maschinenlesbare Teile müssen sprachunabhängig bleiben

### Inhaltliche Herausforderungen
1. **Fachterminologie**: Technische Begriffe müssen konsistent übersetzt werden
2. **Anweisungsklarheit**: Komplexe Anweisungen müssen in allen Sprachen verständlich bleiben
3. **Kulturelle Anpassung**: UI-Patterns und Kommunikationsstil müssen kulturell angepasst werden
4. **Rechtschreibung und Grammatik**: Verschiedene Sprachen haben unterschiedliche Regeln

## Empfohlene Internationalisierungsstrategie

### 1. JSON-basierte Lokalisierung
Verwendung von JSON-Dateien für alle übersetzten Texte mit hierarchischer Struktur.

### 2. Spracherkennungs- und Auswahlsystem
Automatische Spracherkennung basierend auf Browser-Einstellungen mit manueller Überschreibungsmöglichkeit.

### 3. Modulare Protokoll-Generierung
Trennung von sprachabhängigen und sprachunabhängigen Teilen des LRP-Protokolls.

### 4. Responsive Design-Anpassungen
Berücksichtigung unterschiedlicher Textlängen und Leserichtungen.

