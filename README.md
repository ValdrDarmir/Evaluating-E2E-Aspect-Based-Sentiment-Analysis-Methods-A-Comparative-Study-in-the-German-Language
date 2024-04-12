# Evaluating-E2E-Aspect-Based-Sentiment-Analysis-Methods-A-Comparative-Study-in-the-German-Language

## Abstract

There are various tasks to be solved in the area of aspect-based sentiment analysis (ABSA). 
These include the end-to-end (E2E) ABSA task, aspect-opinion pair extraction, aspect category sentiment analysis and more.
Specifically, in the E2E task, aspect pairs consisting of aspect term and polarity are determined.
There are many methods in the English language that accomplish this task. 
In other languages, such as German, such methods tend to be less analyzed or evaluated. 
For this reason, we evaluated the performance of existing English aspect-based sentiment analysis methods in the German language.
We selected three different methods, two graph neural network methods and a generative transformer method, and trained and evaluated them with two corpora, namely GermEval 2017 and MobASA.
The graph-based approaches are a graph convolution network and a graph attention network.
The generative method is based on OpenAI GPT 3.5 and uses text-to-text sentence completion.
The best model (graph attention network) achieved an F1-score of 70.05 \% and 74.35 \% on GermEval 2017 and MobASA.
The other graph-based method, the graph convolution network, achieved an F1-score of 57.28 \% and 72.14 \% on GermEval 2017 and MobASA.
The weakest method did achieve an F1-score of 23.58 \% and 27.00 \% on GermEval 2017 and MobASA.
While the generative transformer method with GPT 3.5 performed comparably worse than the benchmark in the paper by Simmering and Huoviala (2023) the graph neural network models consistently achieved state-of-the-art results.
Overall, our work provides insights into the effectiveness of individual methods in this domain.



## 01 Generative Method with Large Language Modells [1](##Source)

**Requirements:**
- openai 0.28.0

**Usage:**

- Create a config.py file in the same folder as *01/main.py* 
- Create a variable with ```API_KEY = "YOUR_OPENAI_KEY"```

Run the model:
- Exchange the prompts and json file in the *main.py* (optional):
    - Change ```json_file``` in ```loadFunction()``` for a new json output schema.
    - Change the ```prompt``` in ```loadPrompt()```for a new prompt.

- Change the corpus or model:
    - Exchange the corpus in the variable ```name_list``` in the function  ```def chatGPTcall()```
    - Exchange the Model parameter (for example ```model``` or
                    ```temperature```) in ```def chatGPTcall()```
- Run *main.py*

```bash
python main.py 
``` 

Evaluate the model:
- Add the used corpus as the variable to ```xml_file_name = "Your_Corpus.xml"``` for the evaluation in *evaluate.py*
- Run *evaluate.py*

```bash
python evaluate.py
```
## 02 Relational Graph Attention Network [2]

**Requirements:**

- Python 3.6.8
- PyTorch 1.2.0
- [Transformers](https://github.com/huggingface/transformers)
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

## 03 Aspect-specific Graph Convolutional Network [3]

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

## Corpora 

We have included dummy corpora that show the structure of the respective corpora used for each model (This is because we do not have legal rights to distribute the corpora.). 
If you want to train your own corpora, the corresponding position in the code must be adapted.

- 01 Generative Method with Large Language Models
    - Update your corpora in the *input* folder.
- 02 Relational Graph Attention Network
    - Update your corpora in the *data/germeval* or *data/mobasa* folder. 
- 03 Aspect-specific Graph Convolutional Network
    - Update your corpora in the *datasets* folder. 

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


