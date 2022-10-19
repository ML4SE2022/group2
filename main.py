from transformers import PLBartForConditionalGeneration, PLBartTokenizer


tokenizer = PLBartTokenizer.from_pretrained("uclanlp/plbart-java-cs", src_lang="java", tgt_lang="cs")
example_java_phrase = "public ObjectId getObjectId() {return objectId;}"
inputs = tokenizer(example_java_phrase, return_tensors="pt")
model = PLBartForConditionalGeneration.from_pretrained("uclanlp/plbart-java-cs")
translated_tokens = model.generate(**inputs)
print(tokenizer.batch_decode(translated_tokens, skip_special_tokens=True))
