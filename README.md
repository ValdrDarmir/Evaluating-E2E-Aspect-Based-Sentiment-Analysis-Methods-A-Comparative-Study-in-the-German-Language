# Evaluating-E2E-Aspect-Based-Sentiment-Analysis-Methods-A-Comparative-Study-in-the-German-Language

## 01 Generative Method with Large Language Modells

**Requirements:**
- openai 0.28.0

**Usage:**

- Create a config.py file in the same folder as 01/main.py 
- Create a variable with ```API_KEY = "YOUR_OPENAI_KEY"```

Run the model:
- Exchange the prompts and json file in the main.py (optional):
    - Change ```json_file``` in ```loadFunction()``` for a new json output schema.
    - Change the ```prompt``` in ```loadPrompt()```for a new prompt.

- Change the corpus or model:
    - Exchange the corpus in the variable ```name_list``` in the function  ```def chatGPTcall()```
    - Exchange the Model parameter (for example ```model``` or
                    ```temperature```) in ```def chatGPTcall()```
- Run main.py

```bash
python main.py 
``` 

Evaluate the model:
- Add the used corpus as the variable to ```xml_file_name = "Your_Corpus.xml"``` for the evaluation in evaluate.py
- Run evaluate.py

```bash
python evaluate.py
```
## 02 Relational Graph Attention Network

**Requirements:**

- Python 3.6.8
- PyTorch 1.2.0
- Transformers https://github.com/huggingface/transformers
- CUDA 9.0

**Usage:**

Glove Embedding:

- Download the GloVe vectors from this [link](https://www.deepset.ai/german-word-embeddings). 
- Then change the value of parameter ```--glove_dir``` to the directory of the word vector file.

BERT Embedding:

- Download the pytorch version pre-trained ```bert-base-german-cased``` model and vocabulary from the [link](https://huggingface.co/google-bert/bert-base-german-cased) provided by huggingface. 
- Then change the value of parameter ```--bert_model_dir``` to the directory of the bert model.

Run the data preprocessing file after adjusting the paths to your train 

```bash
python data_preprocess_germeval.py
```

```bash
python data_preprocess_mobasa.py
```

Run this command to train and evaluate the model.

```bash
python run.py --gat_bert --embedding_type bert --output_dir data/output-gcn --dropout 0.3 --hidden_size 200 --learning_rate 5e-5
```

## 03 Aspectspecific Graph Convolutional Network

**Requirements**

- Python 3.6
- PyTorch 1.0.0
- SpaCy 2.0.18
- numpy 1.15.4
- pandas 2.0.3

**Usage:**

Install Spacy

```bash
pip install spacy
```

Download the German Spacy vocabulary

```bash
python -m spacy download de_core_news_sm
```

Generate the dependency graph

```bash
python dependency_graph.py
```

Generate the dependency tree

```bash
python dependency_tree.py
```

- Download pretrained GloVe embeddings with this [link](https://www.deepset.ai/german-word-embeddings) and extract the file into glove/.
- Train the model with the german corpus and evaluate it

```bash
python train.py --model_name asgcn --dataset germeval --save True
```

## 04 Preprocessing

**Usage:**

- Exchange ```file_name``` and ```new_file_name``` with the corpus name
- Run main.py

```bash
python main.py
```

## Source

[1] Simmering, P. F., & Huoviala, P. (2023). Large language models for aspect-based sentiment analysis (arXiv:2310.18025). arXiv. https://doi.org/10.48550/arXiv.2310.18025

[GitHub ABSA LLM](https://github.com/qagentur/absa_llm)

[2] Wang, K., Shen, W., Yang, Y., Quan, X., & Wang, R. (2020). Relational Graph Attention Network for Aspect-based Sentiment Analysis (arXiv:2004.12362). arXiv. https://doi.org/10.48550/arXiv.2004.12362

[GitHub R-GAT](https://github.com/shenwzh3/RGAT-ABSA)

[3] Zhang, C., Li, Q., & Song, D. (2019). Aspect-based Sentiment Classification with Aspect-specific Graph Convolutional Networks (arXiv:1909.03477). arXiv. https://doi.org/10.48550/arXiv.1909.03477

[GitHub ASGCN](https://github.com/GeneZC/ASGCN)

## Citation

If you use our work, please cite our paper and link our repo.

```bibtex
@misc
    {weinberger_donhauser_2024_e2e_absa, 
    title = "Evaluating End-to-End Aspect-Based Sentiment Analysis Methods: A Comparative Study in the German Language", 
    author = "Weinberger, Markus and Donhauser, Niklas",  
    month = april, year = "2024", 
    address = "Regensburg, Germany", 
} 
```


