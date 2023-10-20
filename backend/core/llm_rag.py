import torch
import re

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")
device = "cuda"

def llm_rag(user_query, chunks):
    chunk_text = "\n ".join(chunks)
    
    prompt = f"""
    Details: {chunk_text}

    Respond to the User Input based ONLY on the Details given above.

    User Input: {user_query}

    """

    messages = [{"role": "user", "content": prompt}]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

    model_inputs = encodeds.to(device)
    model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=2000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)

    text = decoded[0]
    matches = re.findall('\[/INST\](.*?)</s>', text, flags=re.DOTALL)
    resp = matches[0].strip() if len(matches) > 0 else ''
    return resp