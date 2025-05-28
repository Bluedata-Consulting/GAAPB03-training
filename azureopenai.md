## Setting up Azure OpenAI

Execute the following **once**; substitute your own names where indicated:

```bash
# ✧ Login ✧
az login                       # interactive browser auth




# ✧ Create the Cognitive account ✧
az cognitiveservices account create \
    --name <myResourceName> \
    --resource-group Tredence-B3 \
    --location eastus \
    --kind OpenAI \
    --sku s0

# ✧ Fetch the endpoint URL ✧
az cognitiveservices account show \
    --name <myResourceName> \
    --resource-group Tredence-B3 \
  | jq -r .properties.endpoint

# ✧ Fetch the primary key ✧
az cognitiveservices account keys list \
    --name <myResourceName> \
    --resource-group Tredence-B3 \
  | jq -r .key1

```


### Launch VS code by using the command line
```bash
code
```

- create a file named .env and store below environment variables in it.

```
AZURE_OPENAI_ENDPOINT="https://<myResourceName>.openai.azure.com/"
AZURE_OPENAI_API_KEY="<primary‑key>"

```


```bash

# ✧ Deploy the GPT‑4o mini model ✧
az cognitiveservices account deployment create \
    --name <myResourceName> \
    --resource-group Tredence-B3 \
    --deployment-name myllm \
    --model-name gpt-4o-mini \
    --model-version "2024-07-18" \
    --model-format OpenAI \
    --sku-capacity 1 \
    --sku-name Standard
```

> **Considerations**
>
> * **Quota:** A Standard SKU provides 1 compute unit; API requests above the quota will be throttled.
> * **Naming rules:** Resource names must be globally unique and 2–24 characters.
> * **Azure CLI vs PowerShell:** The above commands run in Bash or PowerShell Core. Ensure `jq` is installed for JSON parsing.

---