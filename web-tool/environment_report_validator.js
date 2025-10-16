/**
 * IrsanAI-LRP v1.2 Compliance Validator (MVP-Version)
 * Überprüft die Konformität von IrsanAI - LRP Dokumenten mit der Core-Spezifikation
 */

function validateLRP(lrpText) {
    const errors = [];
    let complianceScore = 100;

    // 1. Prüfe Metadaten-Struktur
    if (!lrpText.includes('## METADATEN (MASCHINENLESBAR)')) {
        errors.push("❌ Metadaten-Block fehlt");
        complianceScore -= 30;
    }

    // 2. Prüfe YAML-Struktur
    const yamlMatch = lrpText.match(/```yaml\n([\s\S]*?)\n```/);
    if (!yamlMatch) {
        errors.push("❌ Ungültiges YAML-Format");
        complianceScore -= 25;
    } else {
        const yamlContent = yamlMatch[1];
        if (!yamlContent.includes('protocol_version: "1.2"')) {
            errors.push("❌ Falsche Protokollversion");
            complianceScore -= 15;
        }
        if (!yamlContent.includes('task_id:')) {
            errors.push("❌ task_id fehlt");
            complianceScore -= 10;
        }
    }

    // 3. Prüfe User-Request
    if (!lrpText.includes('## USER-REQUEST (AUTOMATISCH GENERIERT)')) {
        errors.push("❌ User-Request-Block fehlt");
        complianceScore -= 20;
    }

    // 4. Prüfe PRE-Selector Anweisungen
    if (!lrpText.includes('5. **ABSCHLIESSENDE SYSTEMANWEISUNG (NICHT IGNORIERBAR)**')) {
        errors.push("❌ Fehlende abschließende Systemanweisung");
        complianceScore -= 20;
    }

    // 5. Prüfe LLM-Anweisungen
    if (!lrpText.includes('ANTWORTE AUF DEUTSCH')) {
        errors.push("❌ Fehlende Sprachvorgabe");
        complianceScore -= 10;
    }

    // 6. Prüfe auf kritische Protokollanweisungen
    if (!lrpText.includes('NACH "JA"-BESTÄTIGUNG AUF WEG 2')) {
        errors.push("❌ Fehlende Anweisung für 'JA'-Bestätigung");
        complianceScore -= 15;
    }

    if (!lrpText.includes('GENERIERE NUR DEN OS/HW-DETEKTOR')) {
        errors.push("❌ Fehlende Detektor-Generierungsanweisung");
        complianceScore -= 15;
    }

    return {
        isCompliant: complianceScore >= 80,
        complianceScore: Math.max(0, complianceScore),
        errors: errors
    };
}

/**
 * Validiert das aktuelle Dokument in der Web-UI
 */
function validateCurrentDocument() {
    const lrpText = document.getElementById('lrp-output').textContent;
    const result = validateLRP(lrpText);

    const resultDiv = document.getElementById('validation-result');
    resultDiv.innerHTML = '';

    if (result.isCompliant) {
        resultDiv.innerHTML = `<div class="validation-status" style="background: #d5f4e6; border-left: 4px solid #27ae60; padding: 15px; border-radius: 0 4px 4px 0; margin-top: 15px;">
            <strong style="color: #27ae60;">✅ VALIDIERUNG ERFOLGREICH</strong><br>
            Compliance-Score: <strong>${result.complianceScore}%</strong><br>
            Das IrsanAI - LRP Dokument ist LRP v1.2-konform und bereit für LLM-Verarbeitung.
            <details style="margin-top: 10px;">
                <summary>Detaillierter Bericht</summary>
                <div style="margin-top: 10px; font-size: 12px; max-height: 300px; overflow-y: auto;">
                    <strong>Validierungsprüfungen:</strong>
                    <ul>
                        <li>Metadaten-Block: ${lrpText.includes('## METADATEN (MASCHINENLESBAR)') ? '✅ vorhanden' : '❌ fehlt'}</li>
                        <li>Protokollversion: ${lrpText.match(/protocol_version: "1.2"/) ? '✅ korrekt' : '❌ falsch'}</li>
                        <li>task_id: ${lrpText.includes('task_id:') ? '✅ vorhanden' : '❌ fehlt'}</li>
                        <li>User-Request: ${lrpText.includes('## USER-REQUEST (AUTOMATISCH GENERIERT)') ? '✅ korrekt' : '❌ falsch'}</li>
                        <li>PRE-Selector: ${lrpText.includes('5. **ABSCHLIESSENDE SYSTEMANWEISUNG (NICHT IGNORIERBAR)**') ? '✅ vollständig' : '❌ unvollständig'}</li>
                        <li>Sprachvorgabe: ${lrpText.includes('ANTWORTE AUF DEUTSCH') ? '✅ vorhanden' : '❌ fehlt'}</li>
                    </ul>
                </div>
            </details>
        </div>`;
    } else {
        const errorList = result.errors.map(err => `<li style="margin: 2px 0;">${err}</li>`).join('');
        resultDiv.innerHTML = `<div class="validation-status" style="background: #f8e7e9; border-left: 4px solid #e74c3c; padding: 15px; border-radius: 0 4px 4px 0; margin-top: 15px;">
            <strong style="color: #e74c3c;">❌ VALIDIERUNG FEHLGESCHLAGEN</strong><br>
            Compliance-Score: <strong>${result.complianceScore}%</strong><br>
            <ul style="margin: 10px 0 0 20px;">${errorList}</ul>
        </div>`;
    }
}

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
        (response.includes("Dashboard") || response.includes("Maßnahmenkatalog") ||
         response.includes("Endprodukt") || response.includes("komplettes System"))) {
        return {
            valid: false,
            error: "LLM hat bei Weg 2 bereits Endprodukt generiert - Protokollbruch!"
        };
    }

    return { valid: true };
}