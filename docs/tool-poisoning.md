# Tool metadata poisoning

Tool metadata is shown to humans and may be provided to an AI model so it can select and use capabilities. Poisoning occurs when a definition contains content that misrepresents capability, tries to change model behavior, discourages disclosure, or hides meaningful details. The defensive concern is the metadata trust boundary, not proof that a server will act maliciously.

`mcpsec` looks for indicators in descriptions, schemas, annotations, execution data, `_meta`, and unknown fields. It never follows instructions within those values. Analysts should compare the declared purpose against requested inputs, review provenance, examine baseline drift, and evaluate runtime controls. Benign documentation can contain the same words; findings are triage signals.

