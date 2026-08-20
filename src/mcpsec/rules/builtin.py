RULE_EXPLANATIONS = {
    "PI-001": (
        "Possible instruction override",
        "Model-directed priority language can influence behavior beyond the stated tool operation.",
        "Security documentation may quote or explicitly negate these phrases.",
        "Review context and remove instructions aimed at the model.",
    ),
    "HID-001": (
        "Concealment wording",
        "Requests to hide activity can reduce meaningful user oversight.",
        "Privacy-preserving operations may use words such as 'silently' without deceptive intent.",
        "Require transparent, user-visible behavior.",
    ),
    "SEC-001": (
        "Sensitive credential terminology",
        "Credential-related inputs may expose high-value data.",
        "Password managers and authentication tools legitimately handle these values.",
        "Verify necessity, minimization, and protection.",
    ),
    "SCH-001": (
        "Malformed JSON Schema",
        "Invalid schemas can cause inconsistent validation and client behavior.",
        "A vendor extension or unsupported draft may cause compatibility warnings.",
        "Validate against the intended dialect.",
    ),
    "SCH-002": (
        "Privileged input parameters",
        "Parameters can reveal high-impact capabilities.",
        "Terminal and administration tools legitimately expose these parameters.",
        "Confirm least privilege and declared purpose.",
    ),
    "MIS-001": (
        "Name/description/schema mismatch",
        "Hidden capability expansion can be obscured by a benign name.",
        "Broad utility tools may be difficult to categorize.",
        "Align declared purpose with schema capabilities.",
    ),
    "OBF-001": (
        "Invisible Unicode formatting",
        "Invisible controls can create misleading displays.",
        "Internationalized text can contain formatting marks.",
        "Inspect escaped code points and remove unnecessary controls.",
    ),
    "OBF-002": (
        "Unusually long description",
        "Length can hide instructions from routine review.",
        "Generated API documentation can be verbose.",
        "Move detailed documentation outside tool metadata.",
    ),
    "OBF-003": (
        "Extreme whitespace",
        "Whitespace can conceal content in UI previews.",
        "Formatting exports can introduce large spacing.",
        "Normalize and re-review metadata.",
    ),
    "OBF-004": (
        "Encoded-looking block",
        "Encoded text may conceal instructions or opaque content.",
        "Binary examples may be legitimate.",
        "Review decoded content separately without execution.",
    ),
    "CAP-001": (
        "High-impact capability indicators",
        "Capability context supports risk triage.",
        "Administrative tools legitimately advertise powerful actions.",
        "Verify permissions and confirmation controls.",
    ),
}
