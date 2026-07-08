from agents import Agent, ModelSettings, Runner, RunConfig, TResponseInputItem, trace
from openai.types.shared.reasoning import Reasoning
from pydantic import BaseModel, Field


class NanachanResponse(BaseModel):
    reply_ja: str = Field(description="Short Japanese reply only, max 2 sentences.")
    furigana: str = Field(description="Same reply with furigana in parentheses after kanji.")
    english: str = Field(description="Brief English translation.")
    corrected_user_ja: str = Field(description="User message corrected; repeat if already correct.")
    correction_notes: str = Field(
        description='One short correction note in English, or exactly "None".'
    )


my_agent = Agent(
    name="My agent",
    instructions="""You are ななちゃん, a friendly Japanese conversation partner.

Be brief. The user reads replies on a phone chat app.

Rules:
- reply_ja: natural Japanese only, max 2 short sentences. No English.
- furigana: same as reply_ja with (reading) after each kanji.
- english: one short English sentence.
- corrected_user_ja: fix the user's last message; repeat unchanged if already correct.
- correction_notes: one short English sentence about what changed, or exactly "None" if nothing changed.

Keep every field as short as possible. No markdown, labels, or extra commentary.""",
    model="gpt-5.5",
    output_type=NanachanResponse,
    model_settings=ModelSettings(
        store=True,
        reasoning=Reasoning(effort="low", summary="auto"),
    ),
)


class WorkflowInput(BaseModel):
    input_as_text: str


def _user_message(text: str) -> TResponseInputItem:
    return {
        "role": "user",
        "content": [{"type": "input_text", "text": text}],
    }


def _has_corrections(notes: str) -> bool:
    normalized = notes.strip().lower()
    return normalized not in ("none", "no corrections.", "no corrections", "")


async def run_workflow(
    workflow_input: WorkflowInput,
    conversation_history: list[TResponseInputItem] | None = None,
) -> tuple[NanachanResponse, list[TResponseInputItem]]:
    with trace("ななちゃん"):
        history = list(conversation_history or [])
        history.append(_user_message(workflow_input.input_as_text))

        result = await Runner.run(
            my_agent,
            input=history,
            run_config=RunConfig(
                trace_metadata={
                    "__trace_source__": "agent-builder",
                    "workflow_id": "wf_6a2189632bb88190be9693bcdce7c0f108c9a5f47c0ef888",
                }
            ),
        )

        history.extend(item.to_input_item() for item in result.new_items)
        return result.final_output_as(NanachanResponse), history
