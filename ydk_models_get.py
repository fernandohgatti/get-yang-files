import re
from ncclient import manager

# Context manager keeping ncclient connection alive for the duration of
# the context.
m = manager.connect(
    host='192.168.100.3',     # IP address of the XR device in your pod
    port=830,              # Port to connect to
    username='admin',      # SSH Username
    password='cisco',  # SSH Password
    hostkey_verify=False   # Allow unknown hostkeys not in local store
)
capabilities = []
# Write each capability to console
for capability in m.server_capabilities:
    # Print the capability
    #print("Capability: %s" % capability)
    # Store the capability list for later.
    capabilities.append(capability)


# Sort the list alphabetically.
capabilities = sorted(capabilities)

# List of modules that we store for use later
modules = []

# Iterate server capabilities and extract supported modules.
for capability in capabilities:
    # Scan the capabilities and extract modules via this regex.
    # i.e., if this was the capability string:
    #   http://www.cisco.com/calvados/show_diag?module=show_diag&revision=2012-03-27
    # then:
    #   show_diag
    # .. would be the module printed.
    # Scan capability string for module
    supported_model = re.search(r'module=([0-9a-zA-Z\-]+)(&|$)', capability)
    # If module found in string, store it.
    if supported_model is not None:
        # Module string was found, store it.
        print("Supported Model: %s" % supported_model.group(1))
        # Store the module for later use.
        modules.append(supported_model.group(1))


# List of models that we want to download.
# We will get the schema for each and write it to disk.
#models_desired = modules
# Iterate each desired model and write it to ./lab/models/
for model in modules:
#    # Get the model schema.
    schema = m.get_schema(model)
    # Open new file handle.
    with open("./profiles/bundles/yang/cisco-ios-xe/16.12.5/{}.yang".format(model), 'w') as f:
        # Write schema
        f.write(schema.data)