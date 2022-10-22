# Group 2
This directory implements AST for the PLBART model. The model is fine-tuned using the CodeXGlue dataset.

# Fine-tuning the model
First build the parser to  run the scripts
```
cd parser
bash build.sh
cd ..
```

For preparing the data run

```
bash prepare.sh
```

For fine-tuning the model and evaluating it against the CodeXGlue benchmark run
```
bash run.sh
```