from huggingface_hub import InferenceClient

client = InferenceClient(
    model="black-forest-labs/FLUX.2-klein-4B", provider="replicate"
)

# Any valid image path
result = client.image_to_image(
    "/Users/abubakar/.cache/huggingface/daggr/files/3b9410ddfedadaa2.png",
    prompt="a cat wearing a hat",
)
