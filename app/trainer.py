import pandas as pd
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import Dataset

# **1. Load Dataset**
data = pd.read_parquet("hf://datasets/ruslanmv/ai-medical-chatbot/dialogues.parquet")
#data = pd.read_csv(df)

# Menggabungkan Patient (pertanyaan) dan Doctor (jawaban) menjadi format input-output
data["text"] = "Patient: " + data["Patient"] + " Doctor: " + data["Doctor"]

# Buat dataset HuggingFace
hf_dataset = Dataset.from_pandas(data[["text"]])

# **2. Load Model dan Tokenizer**
model_name = "w11wo/indo-gpt2-small"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# **3. Preprocessing**
# Tokenisasi dataset
def preprocess(batch):
    encoding = tokenizer(
        batch["text"],
        truncation=True,
        max_length=512,
        padding="max_length",
        return_tensors="pt"
    )
    return {
        "input_ids": encoding["input_ids"][0],
        "attention_mask": encoding["attention_mask"][0],
        "labels": encoding["input_ids"][0]
    }

hf_dataset = hf_dataset.map(preprocess)

# **4. Training Arguments**
training_args = TrainingArguments(
    output_dir="./fine_tuned_indo_gpt2",
    eval_strategy="steps",
    save_strategy="steps",
    logging_dir="./logs",
    logging_steps=50,
    save_steps=200,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    warmup_steps=500,
    learning_rate=5e-5,
    weight_decay=0.01,
    save_total_limit=2,
    fp16=True,  # Gunakan mixed precision untuk mempercepat training (jika GPU mendukung)
    push_to_hub=False  # Nonaktifkan jika Anda tidak ingin mengunggah ke HuggingFace Hub
)

# **5. Trainer**
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=hf_dataset,
    eval_dataset=hf_dataset
)


# **6. Train the Model**
trainer.train()

# **7. Save the Fine-Tuned Model**
model.save_pretrained("./fine_tuned_indo_gpt2")
tokenizer.save_pretrained("./fine_tuned_indo_gpt2")
