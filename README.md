<div align="center">

<h1>Group 2: PLBART with AST</h1>

This project covers the implementation of AST for the PLBART model. Our model is fine-tuned using the CodeXGlue dataset. The original PLBART code can be found [here](https://github.com/wasiahmad/PLBART). The original paper is also linked, [Unified Pre-training for Program Understanding and Generation](https://www.aclweb.org/anthology/2021.naacl-main.211/). We used WSL2 for the project.

</div>

______________________________________________________________________

## Docker Setup
There is the option to use a docker image to run the project. For this image all the dependencies are already installed and you can skip the local setup. The rest of the steps for performing pre-processing, fine-tuning, and evaluation are the same as detailed below. A NVIDIA GPU is necessary to use CUDA with GPU.

Install docker and run the following command to access the image.

```
docker run -it --gpus all jmoreirakanaley/plbart-ast
```

Activate the conda environment for running the experiments.
```
conda activate plbart
```

Access the project.
```
cd ~/plbart-ast
```

______________________________________________________________________

## Local Setup

We can setup a conda environment in order to run experiments, the first step is to download the dependencies. We
assume [anaconda](https://www.anaconda.com/) is installed. The additional requirements
(noted in [requirements.txt](https://github.com/ML4SE2022/group2/blob/main/requirements.txt)) can be installed by
running the following script:

```
bash install_env.sh
```

______________________________________________________________________
## Pre-processing Step
If you wish to only preprocess the dataset follow these steps.

#### Step 1. Build parser

```bash
cd scripts/code_to_code/translation/parser
bash build.sh
cd ..
```
#### Step 2. Prepare the data

```bash
bash prepare.sh src_lang tgt_lang
cd ../../..
```

______________________________________________________________________
## Fine-tuning

We fine-tune and evaluate PLBART with AST on the code-to-code downstream task from CodeXGLUE.

<table>
    <thead>
        <tr>
            <th>Type</th>
            <th>Task</th>
            <th>Language(s)</th>
            <th>Data</th>
            <th>Scripts</th>
            <th>Checkpoints</th>
            <th>Results</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=4>Code to Code</td>
            <td><a href="https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans" target="_blank">Code translation</a></td>
            <td>Java, C#</td>
            <td rowspan=4><a href="https://github.com/ML4SE2022/group2/tree/main/data/codeXglue/code-to-code/dataset" target="_blank">[LINK]</a></td>
            <td><a href="https://github.com/ML4SE2022/group2/tree/main/scripts/code_to_code/translation">[LINK]</a></td>
            <td><a href="https://drive.google.com/drive/folders/1TGbjJLAaHBc4NO9Ntwa6Zh7togpy77Kv" target="_blank">[LINK]</a></td>
            <td><a href="https://docs.google.com/spreadsheets/d/13PCi6XdwlFJfb8GItTasHWQyjFnYWyXm0FPn_k5hafM/edit?usp=sharing" target="_blank">[LINK]</a></td>
        </tr>
    </tbody>
</table>

#### Step 1. Download original PLBART base model

```bash
cd pretrain
bash download.sh
cd ..
```

#### Step 2. Build parser for CodeBLEU evaluation (skip if already done)

```bash
cd scripts/code_to_code/translation/parser
bash build.sh
cd ../../../..
```

#### Step 3. Download PLBART AST fine-tuned checkpoints (skip if already done)

```bash
cd scripts/code_to_code/translation
bash download.sh
cd ../../..
```

#### Step 4. Train and evaluate PLBART

```bash
cd scripts/code_to_code/translation
bash run.sh GPU_IDS src_lang tgt_lang model_size
cd ../../..
```
Here is an example for fine-tuning from java to c#:
```bash
bash run.sh 0 java cs base
```

Note. We fine-tuned our model on 1 `NVIDIA Quadro P1000` (4gb) GPU (~ 8 hours).

______________________________________________________________________
## Evaluation

If you wish to only evaluate the model against the CodeXGLUE benchmark. 

#### Step 1. Download PLBART AST fine-tuned checkpoints

To download the fine-tuned models for java to c# and c# to java

```bash
cd scripts/code_to_code/translation
bash download.sh
```

#### Step 2. Evaluate against CodeXGLUE
Run the evaluate.sh file
```bash
bash evaluate.sh GPU_IDS src_lang tgt_lang
```