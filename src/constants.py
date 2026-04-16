def loadFile(path: str): 
  with open(path) as f:
    return f.read().strip()

environment = dict(l.strip().split("=", 1) for l in loadFile(".env").splitlines())

# OCI
COMPARTMENT_ID = environment.get("COMPARTMENT_ID")
SUBNET_ID = environment.get("SUBNET_ID")
IMAGE_ID = environment.get("IMAGE_ID")
PUBLIC_KEY_PATH = environment.get("PUBLIC_KEY_PATH")

# Machine
OCPUS = 4
MEMORY_IN_GB = 24
STORAGE_IN_GB = 100
SHAPE = "VM.Standard.A1.Flex"