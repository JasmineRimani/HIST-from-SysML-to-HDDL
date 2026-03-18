"""Custom exceptions used across the HIST package."""


class HistError(Exception):
    """Base exception for HIST-specific failures."""


class ConfigurationError(HistError):
    """Raised when the YAML configuration is missing fields or uses invalid values."""


class NotDefinedRequirements(ConfigurationError):
    """Raised when the config does not define domain requirements."""

    def __init__(self, message: str = "You defined no requirements for your domain!"):
        """Store the validation message for missing domain requirements."""

        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return the user-facing validation message."""

        return self.message


class DependencyError(HistError):
    """Raised when an optional runtime dependency required by a workflow is missing."""


class ModelValidationError(HistError):
    """Raised when the Papyrus model does not match the assumptions of the translator."""


class MissingModelPackageError(ModelValidationError):
    """Raised when a configured package cannot be found in the UML/XMI model."""

    def __init__(self, package_name: str):
        """Build a clear error message for a missing configured package."""

        message = (
            f"Could not find the package '{package_name}' in the Papyrus UML model. "
            "Check the package names in the model and in config/configuration.yaml."
        )
        super().__init__(message)
        self.package_name = package_name


class UnsupportedFeatureError(HistError):
    """Raised when a code path is intentionally not implemented yet."""
