"""Loader registry. Importing this package registers built-in plugins."""
from loaders.registry import load_source, register_loader
from loaders import text, structured, pdf, web, database, docx
__all__ = ["load_source", "register_loader"]
