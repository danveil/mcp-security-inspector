class McpsecError(Exception):
    """Expected application error safe to show to a user."""


class InputError(McpsecError):
    """Invalid or unsupported input."""


class RuleValidationError(McpsecError):
    """Invalid data-only rule configuration."""
