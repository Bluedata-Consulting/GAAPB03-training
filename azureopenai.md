## Setting up Azure OpenAI

Execute the following **once**; substitute your own names where indicated:

```bash
# ✧ Login ✧
az login                       # interactive browser auth

# ✧ Create the Cognitive account ✧
az cognitiveservices account create \
    --name <myResourceName> \
    --resource-group Tredence-Batch2 \
    --location eastus \
    --kind OpenAI \
    --sku s0

# ✧ Fetch the endpoint URL ✧
az cognitiveservices account show \
    --name <myResourceName> \
    --resource-group Tredence-Batch2 \
  | jq -r .properties.endpoint

# ✧ Fetch the primary key ✧
az cognitiveservices account keys list \
    --name <myResourceName> \
    --resource-group Tredence-Batch2 \
  | jq -r .key1

```
