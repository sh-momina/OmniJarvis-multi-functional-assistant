# import torch
# from diffusers import StableDiffusionXLPipeline
# from PIL import Image
# import os

# def generate_image_locally(prompt):
#     folder = "Data"
#     os.makedirs(folder, exist_ok=True)

#     # Load model from Hugging Face (will download once and cache locally)
#     model_id = "stabilityai/stable-diffusion-xl-base-1.0"
#     pipe = StableDiffusionXLPipeline.from_pretrained(
#         model_id,
#         torch_dtype=torch.float16,
#         use_safetensors=True,
#     )

#     # Generate image
#     image = pipe(prompt).images[0]

#     # Save and show
#     filepath = os.path.join(folder, "generated_image.png")
#     image.save(filepath)
#     image.show()

# generate_image_locally("a cat eating ice cream and driving")
