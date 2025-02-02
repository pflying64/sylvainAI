from openai import OpenAI
import json

client = OpenAI()

file_ids = [
    'file-JZLJLyFkorZ69uhkcfMptv',
    'file-HDgCVW5WK2oCFVMnQhRz6V',
    'file-2xQRWtf6nJNzpyPCgCiu7S',
    'file-P8BaQZFsNFQ6gzGszKswnY'
]

# Crea un thread
thread = client.beta.threads.create()

# Crea un messaggio che richiede il contenuto dei file
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Per favore leggimi il contenuto di questi file e restituiscimelo in formato testo",
    file_ids=file_ids
)

# Lista gli assistenti disponibili
assistants = client.beta.assistants.list()
assistant_id = assistants.data[0].id

# Crea una run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

# Aspetta che la run sia completata e ottieni la risposta
while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    if run_status.status == 'completed':
        break

# Ottieni i messaggi
messages = client.beta.threads.messages.list(thread_id=thread.id)

# Salva le risposte
for msg in messages.data:
    if msg.role == "assistant":
        for content in msg.content:
            if content.type == 'text':
                filename = f"assistant_response.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content.text.value)
                print(f"Risposta salvata in {filename}")

print("Processo completato")