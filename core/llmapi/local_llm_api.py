from transformers import AutoTokenizer, AutoModelForCausalLM
from vllm import LLM, SamplingParams
from awq import AutoAWQForCausalLM
import os
import json

def get_quantization_method(model_path):
    config_file = os.path.join(model_path, 'config.json')
    if not os.path.exists(config_file):
        return None
    with open(config_file, 'r') as f:
        config = json.load(f)
    quant_config = config.get('quantization_config', {})
    return quant_config.get('quant_method')

def local_model_generate_text(prompt, system_instruction, model_configs):
    # Initialize the LLM with the specified model path
    # print(model_configs)
    # Running VLLM
    enable_quant = True
    model_path = model_configs.model
    quant_method = get_quantization_method(model_configs.model)

    quantization = quant_method if quant_method in {'awq', 'gptq'} else 'bitsandbytes'
    
    if enable_quant:
        print("Quantization enabled with method: ", quantization)
        llm = LLM(model=model_path,quantization=quantization,gpu_memory_utilization=0.95)
    else:
        print("no quantization")
        llm = LLM(model=model_path,gpu_memory_utilization=0.95)

    # Structure the input with special tokens
    prompt = f"<s>[INST] <<SYS>>\n{system_instruction}\n<</SYS>>\n\n{prompt} [/INST]"

    input_text = llm.llm_engine.tokenizer.tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt}],
        tokenize=False,
        add_generation_prompt=True
    )

    sampling_params = SamplingParams(temperature=model_configs.temperature, top_p=model_configs.top_p, max_tokens=model_configs.max_tokens)
    outputs = llm.generate([input_text], sampling_params)

    return outputs[0].outputs[0].text