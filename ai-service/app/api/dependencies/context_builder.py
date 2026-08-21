from app.application.interfaces.context_builder import ( ContextBuilderInterface,)
from app.application.services.context_builder import ContextBuilder

def get_context_builder() -> ContextBuilderInterface:
    return ContextBuilder()