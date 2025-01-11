# IAU Exam
This script will help you prepare yourself to IAU final exam.

## Instalation
```bash
git clone https://github.com/xtruhlar/IAU-Old-Tests-Script.git
cd IAU-Old-Tests-Script
python3 script.py
or
python script.py
```

## Usage:
Select mode:
- 1: Sequential (Question 1 to 170)
- 2: Random (All question but shuffled)
- 3: 30 Questions Test (Random 30 questions)

Question will guide you how to answer:
### Type 1:
```md
1. Convolutional Neural Network can be trained mainly as a supervised learning.
	a) Áno
	b) Nie
```
To get point you have to answer with single option + `)`. Example: `a)`

### Type 2:
```md
2. Among the following, which one are hyperparameters
	a) number of layers in the neural network
	b) learning rate α (alpha)
	c) size(s) of hidden layers
	d) number of iterations
```
If multiple answers are correct, you have to type all of them to get full points. Example `a) b) c) d)`

### Type 3:
```md
7. Assign to the correct group (Singular Value Decomposition / Distributional Semantics): - SVD: , Distributional Semantics:
	a) Truncated SVD
	b) Word Embeddings 
	c) CBOW
	d) Latent Semantic Indexing (LSI)
	e) Skip-Gram
	f) Latent Semantic Analysis (LSA)
```
If you have to connect term and option, either the `(`, `)` will guide you, or there is NOTE in the question, that is saying how is the correct answer structured. In this example it is `SVD: , Distributional Semantics:`. Answer: SVD: a) d) f), Distributional Semantics: b) c) e)
