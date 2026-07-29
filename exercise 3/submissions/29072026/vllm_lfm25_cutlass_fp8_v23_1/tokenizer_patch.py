import json
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

original_apply_chat_template = PreTrainedTokenizerBase.apply_chat_template
original_encode = PreTrainedTokenizerBase.encode
original_call = PreTrainedTokenizerBase.__call__

# Native ChatML template (Bỏ qua Jinja2 siêu chậm)
def fast_apply_chat_template(self, conversation, chat_template=None, add_generation_prompt=False, tokenize=False, **kwargs):
    try:
        text = ""
        for msg in conversation:
            role = msg["role"] if isinstance(msg, dict) else getattr(msg, "role", "")
            content = msg["content"] if isinstance(msg, dict) else getattr(msg, "content", "")
            text += f"<|im_start|>{role}\n{content}<|im_end|>\n"
            
        if add_generation_prompt:
            text += "<|im_start|>assistant\n"
            
        if tokenize:
            return self.encode(text)
        return text
    except Exception as e:
        print(f"[Tokenizer Patch] Fallback apply_chat_template: {e}")
        return original_apply_chat_template(self, conversation, chat_template=chat_template, add_generation_prompt=add_generation_prompt, tokenize=tokenize, **kwargs)

PreTrainedTokenizerBase.apply_chat_template = fast_apply_chat_template

# Prefix Caching cho Tokenizer Encode
class EncodeCache:
    def __init__(self):
        self.cached_prefix_str = None
        self.cached_prefix_ids = None
        self.cached_prefix_call = None

_cache = EncodeCache()

def fast_encode(self, text, *args, **kwargs):
    if isinstance(text, str):
        try:
            if _cache.cached_prefix_str and text.startswith(_cache.cached_prefix_str):
                suffix = text[len(_cache.cached_prefix_str):]
                suffix_ids = original_encode(self, suffix, *args, **kwargs)
                return _cache.cached_prefix_ids + suffix_ids
            
            boundary = "<|im_end|>\n<|im_start|>user\n"
            idx = text.find(boundary)
            if idx != -1:
                prefix_str = text[:idx + len(boundary)]
                suffix_str = text[idx + len(boundary):]
                
                _cache.cached_prefix_str = prefix_str
                _cache.cached_prefix_ids = original_encode(self, prefix_str, *args, **kwargs)
                
                suffix_ids = original_encode(self, suffix_str, *args, **kwargs)
                return _cache.cached_prefix_ids + suffix_ids
        except Exception as e:
            print(f"[Tokenizer Patch] Fallback encode: {e}")
            pass
            
    return original_encode(self, text, *args, **kwargs)

PreTrainedTokenizerBase.encode = fast_encode

def fast_call(self, text, *args, **kwargs):
    if isinstance(text, str):
        try:
            if _cache.cached_prefix_str and text.startswith(_cache.cached_prefix_str):
                suffix = text[len(_cache.cached_prefix_str):]
                suffix_res = original_call(self, suffix, *args, **kwargs)
                
                # Merge dicts
                res = dict(suffix_res)
                if _cache.cached_prefix_call is None:
                    _cache.cached_prefix_call = dict(original_call(self, _cache.cached_prefix_str, *args, **kwargs))
                
                for k in res.keys():
                    if isinstance(res[k], list) and k in _cache.cached_prefix_call:
                        res[k] = _cache.cached_prefix_call[k] + res[k]
                return suffix_res.__class__(res)
                
            boundary = "<|im_end|>\n<|im_start|>user\n"
            idx = text.find(boundary)
            if idx != -1:
                prefix_str = text[:idx + len(boundary)]
                suffix_str = text[idx + len(boundary):]
                
                _cache.cached_prefix_str = prefix_str
                _cache.cached_prefix_ids = original_encode(self, prefix_str)
                _cache.cached_prefix_call = dict(original_call(self, prefix_str, *args, **kwargs))
                
                suffix_res = original_call(self, suffix_str, *args, **kwargs)
                res = dict(suffix_res)
                for k in res.keys():
                    if isinstance(res[k], list) and k in _cache.cached_prefix_call:
                        res[k] = _cache.cached_prefix_call[k] + res[k]
                return suffix_res.__class__(res)
        except Exception as e:
            print(f"[Tokenizer Patch] Fallback __call__: {e}")
            pass
            
    return original_call(self, text, *args, **kwargs)

PreTrainedTokenizerBase.__call__ = fast_call

print(">>> [Viettel AI Race] SUCCESS: Injected ChatML & Prefix Caching for Tokenizer!")
