import inspect
try:
    import vllm.model_executor.models.lfm2 as lfm2
    print(inspect.getsource(lfm2))
except ImportError as e:
    print("ImportError:", e)
except Exception as e:
    print("Exception:", e)
