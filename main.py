from transformers import PLBartForConditionalGeneration, PLBartTokenizer, AutoTokenizer, AutoModelForSeq2SeqLM, \
    DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
from datasets import load_dataset, Dataset, concatenate_datasets


def preprocess(data):
    prefix = "translate Java to C#: "
    src_lang = "java"
    tgt_lang = "cs"
    inputs = [prefix + x[src_lang] for x in data["translation"]]
    targets = [x[tgt_lang] for x in data["translation"]]
    tokenized_inputs = tokenizer(inputs, text_target=targets, max_length=128, truncation=True)
    return tokenized_inputs


if __name__ == '__main__':

    tokenizer = AutoTokenizer.from_pretrained("uclanlp/plbart-java-cs")

    model = AutoModelForSeq2SeqLM.from_pretrained("uclanlp/plbart-base")

    dataset = load_dataset('code_x_glue_cc_code_to_code_trans')

    train_data = dataset["train"].select(range(100))
    print(train_data)
    test = [{"java": x, "cs": y} for x, y in zip(train_data["java"], train_data["cs"])]
    # print(test)
    dset = Dataset.from_dict({"translation": test})
    train_data = concatenate_datasets([train_data, dset], axis=1)
    train_data = train_data.remove_columns(['java', 'cs'])

    tokenized_train_data = train_data.map(preprocess, batched=True)
    print(tokenized_train_data[0])


    eval_data = dataset["test"].select(range(10))
    test = [{"java": x, "cs": y} for x, y in zip(eval_data["java"], eval_data["cs"])]
    # print(test)
    dset = Dataset.from_dict({"translation": test})
    eval_data = concatenate_datasets([eval_data, dset], axis=1)
    eval_data = eval_data.remove_columns(['java', 'cs'])
    tokenized_eval_data = eval_data.map(preprocess, batched=True)
    print(tokenized_eval_data)
    print(tokenized_eval_data[0])

    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=1,
        remove_unused_columns=True,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_data,
        eval_dataset=tokenized_eval_data,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model("./model")



