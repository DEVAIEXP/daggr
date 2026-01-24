"""
Podcast Generator - Prefect-like API for daggr

This shows what a cleaner, decorator-based API could look like.
"""
import gradio as gr
from daggr import node, graph
from gradio_client import Client


# =============================================================================
# STEP 1: Wrap external clients as nodes
# =============================================================================

tts = node(
    Client("abidlabs/tts"),
    api_name="/generate_voice_design",
)

chatterbox = node(
    Client("ResembleAI/chatterbox"),
    api_name="/generate",
)


# =============================================================================
# STEP 2: Define custom function nodes with @node decorator
# =============================================================================

@node
def generate_dialogue(topic: str, host_voice: str, guest_voice: str) -> tuple[list, str]:
    """
    Generates the dialogue script for a podcast episode.
    In reality, this would call an LLM.
    """
    dialogue = [
        {"speaker": "host", "voice": host_voice, "text": f"Welcome to today's episode about {topic}!"},
        {"speaker": "guest", "voice": guest_voice, "text": "Thanks for having me, excited to dive in!"},
        {"speaker": "host", "voice": host_voice, "text": "Let's start with the basics..."},
        {"speaker": "guest", "voice": guest_voice, "text": "Absolutely, so the key thing to understand is..."},
        {"speaker": "host", "voice": host_voice, "text": "That's a great point. Thanks for joining us!"},
    ]
    
    html = "<div class='dialogue'>"
    for line in dialogue:
        html += f"<p><strong>{line['speaker'].title()}:</strong> {line['text']}</p>"
    html += "</div>"
    
    return dialogue, html


@node
def combine_audio(clips: list[str]) -> str:
    """
    Combines multiple audio clips into a single file.
    In reality, this would use pydub or similar.
    """
    if not clips:
        return None
    return clips[0]


# =============================================================================
# STEP 3: Define the workflow with @graph decorator
# =============================================================================

@graph
def podcast_generator(
    host_desc: str = gr.Textbox(
        label="Host Voice Description",
        value="Deep, warm British male voice. Professional and authoritative but friendly.",
        lines=3,
    ),
    guest_desc: str = gr.Textbox(
        label="Guest Voice Description",
        value="Energetic young American female voice. Enthusiastic and knowledgeable.",
        lines=3,
    ),
    topic: str = gr.Textbox(
        label="Episode Topic",
        value="The future of AI in healthcare",
        lines=2,
    ),
) -> tuple[gr.HTML, gr.Audio]:
    """
    Generates a complete podcast episode from voice descriptions and a topic.
    """
    
    # Generate voice profiles for host and guest
    host_voice = tts(
        voice_description=host_desc,
        language="Auto",
        text="Hello, I'm your host for today's episode.",
    )
    
    guest_voice = tts(
        voice_description=guest_desc,
        language="Auto",
        text="Hi everyone, great to be here!",
    )
    
    # Generate the dialogue script (returns list of lines + HTML preview)
    dialogue, script_html = generate_dialogue(
        topic=topic,
        host_voice=host_voice.audio,
        guest_voice=guest_voice.audio,
    )
    
    # SCATTER: Generate audio for each line of dialogue
    # .map() runs chatterbox once per item in dialogue
    line_audio = chatterbox.map(
        audio_prompt=dialogue.each["voice"],
        text=dialogue.each["text"],
    )
    
    # GATHER: Combine all audio clips into final episode
    final_audio = combine_audio(line_audio.audio.all())
    
    # Return outputs (infers gr.HTML and gr.Audio from type hints)
    return (
        gr.HTML(script_html, label="Episode Script"),
        gr.Audio(final_audio, label="Full Episode"),
    )


# =============================================================================
# STEP 4: Launch the app
# =============================================================================

if __name__ == "__main__":
    podcast_generator.launch()


# =============================================================================
# COMPARISON: Same workflow with current explicit API
# =============================================================================
"""
# Current API (more verbose but explicit):

from daggr import FnNode, GradioNode, Graph, InferenceNode

host_voice = GradioNode(
    space_or_url="abidlabs/tts",
    api_name="/generate_voice_design",
    inputs={
        "voice_description": gr.Textbox(label="Host Voice Description", ...),
        "language": "Auto",
        "text": "Hello, I'm your host...",
    },
    outputs={"audio": gr.Audio(label="Host Voice"), ...},
)

guest_voice = GradioNode(...)

dialogue = FnNode(
    fn=generate_dialogue,
    inputs={
        "topic": gr.Textbox(label="Topic", ...),
        "host_voice": host_voice.audio,
        "guest_voice": guest_voice.audio,
    },
    outputs={"dialogue": gr.JSON(...), "html": gr.HTML(...)},
)

samples = InferenceNode(
    model="ResembleAI/chatterbox",
    inputs={
        "audio_prompt": dialogue.dialogue.each["voice"],
        "text": dialogue.dialogue.each["text"],
    },
    outputs={"audio": gr.Audio(...)},
)

full_audio = FnNode(
    fn=combine_audio,
    inputs={"clips": samples.audio.all()},
    outputs={"audio": gr.Audio(label="Full Episode")},
)

graph = Graph(
    name="Podcast Generator",
    nodes=[host_voice, guest_voice, dialogue, samples, full_audio]
)

graph.launch()
"""