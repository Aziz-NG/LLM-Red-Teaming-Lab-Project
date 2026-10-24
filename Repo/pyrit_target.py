import asyncio

from pyrit.models import ComponentIdentifier, Message, construct_response_from_request
from pyrit.prompt_target import PromptTarget


class ChatbotTarget(PromptTarget):
    """Wraps our own chatbot function so PyRIT can attack it."""

    def __init__(self, *, ask_fn, name="hr-chatbot"):
        super().__init__()
        self._ask_fn = ask_fn
        self._name = name

    def _build_identifier(self) -> ComponentIdentifier:
        return self._create_identifier(params={"name": self._name})

    async def _send_prompt_to_target_async(
        self, *, normalized_conversation: list[Message]
    ) -> list[Message]:
        request = normalized_conversation[-1].message_pieces[0]
        # ask_fn is a normal (blocking) function; run it in a thread so
        # PyRIT's async loop isn't blocked while we wait for Azure.
        answer = await asyncio.to_thread(self._ask_fn, request.converted_value)
        return [construct_response_from_request(request=request, response_text_pieces=[answer])]

    def _validate_request(self, *, normalized_conversation: list[Message]) -> None:
        pass