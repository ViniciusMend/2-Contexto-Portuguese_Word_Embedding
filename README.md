# RECODING CONTEXTO GAME IN PYTHON
<img src="assets/contexto.png"
     alt="Contexto"
     style="width: 100%; height: 50%" />

[Contexto](https://contexto.me/) is a a game based on an algorithm that describes and analyzes the degree of similarity, or context, in which words are used in the Portuguese language. This project, is a recoding of this system, using the same data and techniques in Python.

## Motivation
This project aims to use Natural Language Processing (NLP) using Word2Vec and Gensim to build a complete system based on Game Contexto.

## Objectives
1. To recreate a Context system for improve Data Science and NLP skills
2. To build a Data Science project using techniques other than commonly used machine learning

## Dataset Overview
- Skip-gram 1000 dimensões: A txt document (2.8 GB) containing 929606 trained words and represented as a vector with 1000 numeric values
    - column1: the word
    - column2 - column1001: the numeric values
    
- Skip-gram 50 dimensões: A txt document (168 MB) containing 929606 trained words and represented as a vector with 50 numeric values
    - column1: the word
    - column2 - column51: the numeric values

- Lista de palavras Português-BR: A single column contains 261798 Brazilian Portuguese words

Dataset Source:
1. [Skip-gram 1000 dimensões](http://nilc.icmc.usp.br/nilc/index.php/repositorio-de-word-embeddings-do-nilc)
2. [Skip-gram 50 dimensões](http://nilc.icmc.usp.br/nilc/index.php/repositorio-de-word-embeddings-do-nilc)
3. [Lista de palavras Português-BR](https://www.ime.usp.br/~pf/estruturas-de-dados/aulas/sandbox/br-utf8.txt)

## Results
The developed system is a available [here](), and contains the following features:

### Page 1: Jogo
The first "Jogo" page presents the main application, which is the same resource present in the original Context system. In this system,
there are 10 different words for the user to choose, and after that, the user tries to find the secret word by writing other words, and the system tells how far or close the entered word is from the secret word. The objective is to find the word number 1.

<p align="center">
  <img alt="Page1" title="#Page1" src="assets/page1.png" width="400px">
</p>

### Page 2: Lista Palavras
The second "Lista Palavras" page presents an additional application not found in the original system, which allows the user to find the 500 most similar words for the word typed.

<p align="center">
  <img alt="Page2" title="#Page2" src="assets/page2.png" width="100%" height="50%">
</p>

### Page 3: Sobre
The final "Sobre" page presents some information about the project and the based system.

<p align="center">
  <img alt="Page3" title="#Page3" src="assets/page3.png" width="100%" height="50%">
</p>

Note: The system has been fully developed for Portuguese speakers, which means that any word entered in the system must be in Portuguese.

## Contact
Please, be welcome to copy and modified this project for improvement and changes. I am available for doubls and any discuss, and you can find and send me message by thoses links:

<div>
  <a href="https://www.instagram.com/vini_henr/" target="_blank"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" target="_blank"></a>
  <a href = "mailto:viniciushenrique9510@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
  <a href="https://www.linkedin.com/in/vinicius-henrique-engproducao" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
  <a href="https://medium.com/@viniciushenrique9510" target="_blank"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" target="_blank"></a>
</div>
