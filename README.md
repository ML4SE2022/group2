<div align="center">

<h1>Group 2 PLBART</h1>

This project covers implementing AST for the PLBART model. Our model is fine-tuned using the CodeXGlue dataset. The original PLBART code can be found [here](https://github.com/wasiahmad/PLBART). The original paper is also linked, [Unified Pre-training for Program Understanding and Generation](https://www.aclweb.org/anthology/2021.naacl-main.211/).

</div>

______________________________________________________________________

## Setup

We can setup a conda environment in order to run experiments, the first step is to download the dependencies. We
assume [anaconda](https://www.anaconda.com/) is installed. The additional requirements
(noted in [requirements.txt](https://github.com/wasiahmad/PLBART/blob/main/requirements.txt)) can be installed by
running the following script:

```
bash install_env.sh
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
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=4>Code to Code</td>
            <td><a href="https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/code-to-code-trans" target="_blank">Code translation</a></td>
            <td>Java, C#</td>
            <td rowspan=4><a href="https://drive.google.com/file/d/15jokCxFQ9BUbptMsrfj4RdH_KiNkTRP2" target="_blank">[LINK]</a></td>
            <td><a href="https://github.com/wasiahmad/PLBART/tree/main/scripts/code_to_code/translation">[LINK]</a></td>
            <td><a href="https://drive.google.com/drive/folders/1KKdBWTRjnxC70icQrCbCXuj6ahMFQlE0" target="_blank">[LINK]</a></td>
        </tr>
    </tbody>
</table>

#### Step1. Download PLBART checkpoint

```bash
cd pretrain
bash download.sh
cd ..
```

#### Step2. Download the data

```bash
cd data/codeXglue
bash download.sh
cd ../..
```

#### Step3. Build parser for CodeBLEU evaluation

```bash
cd evaluation/CodeBLEU/parser
bash build.sh
cd ../../..
```

#### Step4. Prepare the data, train and evaluate PLBART

```bash
cd scripts/code_to_code/translation
bash prepare.sh
bash run.sh GPU_IDS src_lang tgt_lang model_size
cd ../../..
```
Here is an example for fine-tuning from java to c#:
```bash
bash run.sh 0 java cs base
```

Note. We fine-tuned our model on 1 `NVIDIA Quadro P1000` (4gb) GPU (~ 8 hours).