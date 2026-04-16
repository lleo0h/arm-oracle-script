import oci
import constants
import time
import random
from datetime import datetime

def debug(text: str):
  print(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

def createAmpereVirtualMachine(compute_client: oci.core.ComputeClient, ad_name: str):
  launch_details = oci.core.models.LaunchInstanceDetails(
    compartment_id=constants.COMPARTMENT_ID,
      availability_domain=ad_name,
      shape=constants.SHAPE,
      shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
        ocpus=constants.OCPUS,
        memory_in_gbs=constants.MEMORY_IN_GB
      ),
      display_name="ampere",
      source_details=oci.core.models.InstanceSourceViaImageDetails(
        image_id=constants.IMAGE_ID,
        boot_volume_size_in_gbs=constants.STORAGE_IN_GB
      ),
      create_vnic_details=oci.core.models.CreateVnicDetails(
        subnet_id=constants.SUBNET_ID,
        assign_public_ip=True
      ),
      metadata={
        "ssh_authorized_keys": constants.loadFile(constants.PUBLIC_KEY_PATH)
      }
    )

  return compute_client.launch_instance(launch_details)

config = oci.config.from_file()
identity_client = oci.identity.IdentityClient(config)
compute_client = oci.core.ComputeClient(config)
availability_domains = identity_client.list_availability_domains(constants.COMPARTMENT_ID).data

while True:
  for ad in availability_domains:
    try:
      debug(f"Trying to create the instance in {ad.name}.")
      createAmpereVirtualMachine(compute_client, ad.name)
      debug("The instance was created successfully.")
      break
    except oci.exceptions.ServiceError as e:
      debug(e.message)
  else:
    r = 30 + random.randrange(1, 5)
    debug(f"Next attempt in {r} seconds.")
    time.sleep(r)
    continue

  break