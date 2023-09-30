import torch    

def get_device():
    # Check if GPU is available
    if torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")
