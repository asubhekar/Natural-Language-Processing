# -*- coding: utf-8 -*-
"""RobertA_QuestionAnsweing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13TK5YRIL3Nn1vKYwnjE2WANcAioPccUp

## Machine Reading Comprehension
"""

!pip install datasets

# Importing required libraries
import numpy as np
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, RobertaForQuestionAnswering

"""## RoBERTa for Question Answering

### Loading the dataset
"""

dataset = load_dataset("squad_v2")

random_choices = np.random.choice(len(dataset['train']['context']), 15)
question = []
context = []
ground_truth = []
for choice in range(0,15):
  q = dataset["train"]["question"][choice]
  c = dataset["train"]["context"][choice]
  a = dataset["train"]["answers"][choice]
  question.append(q)
  context.append(c)
  ground_truth.append(a)
print('Number of Questions = ',len(question))
print('Number of Contexts = ',len(context))
print('Number of Answers = ',len(ground_truth))

"""### Data Statistics"""

context_len = []
question_len = []
answer_len = []

for i in range(len(context)):
  context_len.append(len(context[i]))
  question_len.append(len(question[i]))
  answer_len.append(len(answer[i]['text']))

print("------CONTEXT STATS----------")
print("Maximum length of contexts = ", np.max(context_len))
print("Minimum length of contexts = ", np.min(context_len))
print("Average length of contexts = ", np.average(context_len))

print("------QUESTION STATS----------")
print("Maximum length of questions = ", np.max(question_len))
print("Minimum length of questions = ", np.min(question_len))
print("Average length of questions = ", np.average(question_len))

print("------ANSWER STATS----------")
print("Maximum length of answers = ", np.max(answer_len))
print("Minimum length of answers = ", np.min(answer_len))
print("Average length of answers = ", np.average(answer_len))

"""### RoBERTa model implementation"""

# Initializing the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
model = RobertaForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

# Tokenizing the inputs
inputs = tokenizer(question, context, padding=True, truncation=True, return_tensors="pt")

# Feeding the inputs to the model
with torch.no_grad():
    outputs = model(**inputs)
# Checking for output contents
outputs.keys()

answer_start_index = []
answer_end_index = []
for i in range(len(outputs.start_logits)):
  # Storing the start and end logits
  answer_start = torch.argmax(outputs.start_logits[i])
  answer_end = torch.argmax(outputs.end_logits[i])
  answer_start_index.append(answer_start)
  answer_end_index.append(answer_end)

decoded_output = []
predict_answer_tokens = []
predict_answer_tensors = []
for i in range(len(inputs['input_ids'])):
  # Predicting answer tokens
  pred_tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][i, answer_start_index[i] : answer_end_index[i] + 1])
  predict_answer_tokens.append(pred_tokens)
  # Converting tokens to string
  answer = tokenizer.convert_tokens_to_string(pred_tokens)
  decoded_output.append(answer)

for i in range(len(question)):
  print("Context : ", context[i])
  print("Question : ", question[i])
  print("Answer start index : ",answer_start_index[i])
  print("Answer end index : ",answer_end_index[i])
  print("Predicted answer tokens : ", predict_answer_tokens[i])
  print("Decoded answer : ", decoded_output[i])
  print("---------------------------")

"""## CHAT GPT for Question Answering

Based on the context, following questions were asked to CHAT GPT.

"""

context[0]

"""Question 1 : Based on the context, When did Beyonce start becoming popular?Answer should be 2 words

Answer : Late 1990s

Question 2 : Based on the context, What areas did Beyonce compete in when she was growing up? Answer should be 3 words

Answer : Singing and dancing

Question 3 : Based on the context, When did Beyonce leave Destiny's Child and become a solo singer?

Answer : During hiatus

Question 4 : Based on the context, In what city and state did Beyonce  grow up?

Answer : Houston, Texas

Question 5 : Based on the context, In which decade did Beyonce become famous?

Answer : Late 1990s

Question 6 : Based on the context, In what R&B group was she the lead singer?

Answer : Destiny's Child

Question 7 : Based on the context, What album made her a worldwide known artist?

Answer : "Dangerously in Love"

Question 8 : Based on the context, Who managed the Destiny's Child group?

Answer : Mathew Knowles

Questions 9 : Based on the context, When did Beyoncé rise to fame?

Answer : Late 1990s

Quesiton 10 : Based on the context. What role did Beyoncé have in Destiny's Child?

Answer : Lead singer

Question 11 : Based on the context, What was the first album Beyoncé released as a solo artist?

Answer : "Dangerously in Love"

Question 12 : Based on the context, Which songss featured the Billboard Hot 100 number-one singles

Answer : The Billboard Hot 100 number-one singles featured in Beyoncé's debut solo album "Dangerously in Love" are "Crazy in Love" and "Baby Boy."

Question 13 : Based on the context, who was mathew knowles?

Answer : Matthew Knowles, often referred to as Mathew Knowles, is the father of Beyoncé Knowles-Carter and was also her manager, as well as the manager of Destiny's Child.

Question 14 : Based on the context, what is Beyoncé relation to Houston, Texas?

Answer : Beyoncé was born and raised in Houston, Texas.

Question 15 : Based on the context, what year was "Dangerously in Love" released?

Answer : "Dangerously in Love" by Beyoncé was released in 2003.

## Claude AI for Question Answering

Based on context, following questions wer easked to Claude AI.
"""

context[0]

"""Question 1 : Based on the context, When did Beyonce start becoming popular?Answer should be 2 words

Answer : Based on the context provided, it states that Beyoncé "rose to fame in the late 1990s as lead singer of R&B girl-group Destiny's Child". So the timeframe when she started becoming popular was in the "late 1990s".
To summarize the 2-word timeframe for when Beyoncé began gaining widespread popularity and fame:
Late 1990s

Question 2 : Based on the context, What areas did Beyonce compete in when she was growing up? Answer should be 3 words

Answer : In the given background context, it states that Beyoncé "performed in various singing and dancing competitions as a child".
Therefore, answering this question based on the context provided, Beyoncé competed in:
"singing and dancing"
So the 3 words summarizing what types of areas Beyoncé competed in as a child are: singing and dancing

Question 3 : Based on the context, When did Beyonce leave Destiny's Child and become a solo singer?

Answer : In the provided context, it states:
"Their hiatus saw the release of Beyoncé’s debut album, Dangerously in Love (2003), which established her as a solo artist worldwide..."
This tells us that Destiny's Child took a hiatus (a break) and around 2003 is when Beyoncé left the group to pursue her solo singing career with the release of her debut solo album "Dangerously in Love" in 2003.
Therefore, based on the given context, Beyoncé left Destiny's Child and became a solo singer in 2003.

Question 4 : Based on the context, In what city and state did Beyonce grow up?

Answer : In the background context provided, it states that Beyoncé "Born and raised in Houston, Texas".
Therefore, the city and state where Beyoncé grew up, based on the given biographical information, is:
Houston, Texas
So the answer for where Beyoncé was raised, per the context, is that she grew up in Houston, Texas.

Question 5 : Based on the context, In which decade did Beyonce become famous?

Answer : In the context provided about Beyoncé's background, it states she "rose to fame in the late 1990s as lead singer of R&B girl-group Destiny's Child".
The late 1990s refers to the latter part of the 1990-1999 decade. So based on this contextual information, the decade when Beyoncé attained fame and became well-known is:
The 1990s
Therefore, the answer for the decade Beyoncé became famous, according to the details given, is the 1990s.

Question 6 : Based on the context, In what R&B group was she the lead singer?

Answer : In the provided background context on Beyoncé's career, it clearly states that she "rose to fame in the late 1990s as lead singer of R&B girl-group Destiny's Child".
Therefore, the R&B group where she was the lead singer, based on this context, was:
Destiny's Child
So the answer is that Beyoncé was the lead singer of the R&B girl group called Destiny's Child.

Question 7 : Based on the context, What album made her a worldwide known artist?

Answer : In the context provided, it states:
"Their hiatus saw the release of Beyoncé’s debut album, Dangerously in Love (2003), which established her as a solo artist worldwide..."
So her debut solo album "Dangerously in Love" released in 2003 is credited with establishing Beyoncé as an artist known worldwide.
Therefore, based on this contextual information, the album that made Beyoncé a worldwide known solo artist was:
Dangerously in Love

Question 8 : Based on the context, Who managed the Destiny's Child group?

Answer : Based on the context provided, Destiny's Child was managed by Beyoncé's father, Mathew Knowles. Specifically, the passage states:
"Managed by her father, Mathew Knowles, the group became one of the world's best-selling girl groups of all time."
So Mathew Knowles was the manager of the highly successful 1990s girl group Destiny's Child, which launched his daughter Beyoncé's singing career.

Questions 9 : Based on the context, When did Beyoncé rise to fame?

Answer : Based on the information in the provided context, Beyoncé rose to fame in the late 1990s as the lead singer of Destiny's Child. Specifically, the context states:
"Born and raised in Houston, Texas, she performed in various singing and dancing competitions as a child, and rose to fame in the late 1990s as lead singer of R&B girl-group Destiny's Child."
So Beyoncé transitioned from competing in singing/dancing competitions as a child in Houston, to hitting stardom with Destiny's Child in the late 1990s as their lead singer. That time period in the late '90s is when she initially rose to widespread fame.


Quesiton 10 : Based on the context. What role did Beyoncé have in Destiny's Child?

Answer : Based on the context provided, Beyoncé was the lead singer of Destiny's Child. The passage specifically states:
"and rose to fame in the late 1990s as lead singer of R&B girl-group Destiny\'s Child."
So Beyoncé's role in the highly successful girl group Destiny's Child was serving as their lead vocalist. The context confirms that she sang lead vocals for the group as they rose to fame together in the late 1990s before she later embarked on a solo career.

Question 11 : Based on the context, What was the first album Beyoncé released as a solo artist?

Answer : Based on the information in the provided context, the first album Beyoncé released as a solo artist was "Dangerously in Love" in 2003.
The passage states:
"Their hiatus saw the release of Beyoncé’s debut album, Dangerously in Love (2003), which established her as a solo artist worldwide..."
So after Destiny's Child went on hiatus, Beyoncé released her debut and first solo studio album in 2003 titled "Dangerously in Love". This album is credited with cementing her status as an international solo superstar in her own right.
Therefore, "Dangerously in Love" was the name of Beyoncé's first album released as a solo musical artist after her time with Destiny's Child.

Question 12 : Based on the context, Which songss featured the Billboard Hot 100 number-one singles

Answer : Based on the context provided, the Beyoncé songs that featured as number-one Billboard Hot 100 singles were "Crazy in Love" and "Baby Boy".
The passage states:
"earned five Grammy Awards and featured the Billboard Hot 100 number-one singles "Crazy in Love" and "Baby Boy"."
So her debut solo album "Dangerously in Love" produced two hugely popular #1 Billboard hits for Beyoncé - the songs "Crazy in Love" and "Baby Boy".
Therefore, according to the context, "Crazy in Love" and "Baby Boy" were the two singles from Beyoncé's early solo career that reached #1 on the Billboard Hot 100 chart.

Question 13 : Based on the context, who was mathew knowles?

Answer : Based on the context provided, Mathew Knowles was Beyoncé's father and the manager of Destiny's Child:
"Managed by her father, Mathew Knowles, the group became one of the world's best-selling girl groups of all time."
So Mathew Knowles was:
Beyoncé's father
The manager of the highly successful R&B girl group Destiny's Child, which Beyoncé was part of
In his role as Destiny's Child's manager, Mathew Knowles guided the group to become "one of the world's best-selling girl groups of all time". He also likely played a key role in nurturing his daughter Beyoncé's talent and helping launch her towards stardom.
Therefore, to summarize, Mathew Knowles was Beyoncé's father as well as her Destiny's Child group's manager.

Question 14 : Based on the context, what is Beyoncé relation to Houston, Texas?

Answer : Based on the details provided in the context, Beyoncé has a close connection to Houston, Texas because she was born and raised there:
"Born and raised in Houston, Texas..."
This clearly states that Houston is Beyoncé's hometown - it's where she was both born and spent her childhood/formative years.
The context goes on to detail how her early singing and performance origins trace back to Houston as well:
"she performed in various singing and dancing competitions as a child..."
So Beyoncé first built her talents in Houston by competing locally in singing and dancing contests as a young girl.
In summary, Beyoncé has strong ties to Houston as it is both her birthplace and the city where she was raised, and first started participating in the competitions that set the foundation for her eventual rise to superstardom from Destiny's Child onwards. Her relationship to Houston is that it is her hometown on multiple levels.

Question 15 : Based on the context, what year was "Dangerously in Love" released?

Answer : Based on the information provided in the context, Beyoncé's debut solo album "Dangerously in Love" was released in 2003.
The relevant quote from the passage is:
"Their hiatus saw the release of Beyoncé’s debut album, Dangerously in Love (2003), which established her as a solo artist worldwide..."
The key detail here is the year 2003 provided right after the album title "Dangerously in Love", indicating this was the release year for that critically and commercially successful first solo effort of hers.
Therefore, to directly answer the question, according to the context, the year Beyoncé's album "Dangerously in Love" was released is 2003.

## Result analysis and Evaluation

To get an idea of how well each model performs, we can check only one question across all 3 models.
"""

print("Ground Truth for first question : ", ground_truth[0])

"""Answer from RoBERTa for question 1: late 1990s

Answer from CHAT GPT for question 1: Late 1990s

Answer from Claude AI for question 1: Based on the context provided, it states that Beyoncé "rose to fame in the late 1990s as lead singer of R&B girl-group Destiny's Child". So the timeframe when she started becoming popular was in the "late 1990s". To summarize the 2-word timeframe for when Beyoncé began gaining widespread popularity and fame: Late 1990s

"""

print("Ground Trught for second question : ", ground_truth[1])

"""Answer from RoBERTa for question 2: singing and dancing

Answer from CHAT GPT for question 2: Singing and dancing

Answer from Claude AI for question 2: In the given background context, it states that Beyoncé "performed in various singing and dancing competitions as a child". Therefore, answering this question based on the context provided, Beyoncé competed in: "singing and dancing" So the 3 words summarizing what types of areas Beyoncé competed in as a child are: singing and dancing

After comparing with the ground truth, we can approximately calculate the performance.

RoBERTa : 70% (Grammatical issues since multiple answers do not have proper captilaization. Also multiple answers are incomplete and missing supporting text. The final answer still makes sense)

CHAT GPT : 80% (No grammatical issues overall and better punctuation compared to RoBERTa. But still missing a few support words in multiple questions)

Claude AI : 100% (No grammatical issues and no missing elements in the outcome)

## Comparison and Conclusion

Out of all 3 models (RoBERTa, CHAT GPT and Claude), Claude performs the best. Followed by CHAT GPT and then RoBERTa.

The major reason for performance difference in the model architecture. RoBERTa is a fairly simple model compared to CHAT GPT and Claude. RoBERTa fails to capture long term dependencies and looks only at the tokens which are important.

Similarly, CHAT GPT was able to capture better information and better grammatical differences.

Claude on the other hand out performed both as it looked at the entire context for the answer and highlighted the answers in the context itself and compiled a final output depending on the prompts.

Advantages of pretrained models:
   

*   Faster to train and generate results as the model is already trained, no compute needed.
*   Can have specific domain knowledge built-in through pretraining.
*   Can be custom tuned with your own labeled data for your task.
*   More predictable results since you start with an existing model.

Disadvantages of pretrained models:
* Cannot learn and improve beyond initial capabilities.
* Require expertise to properly tune and apply models.
* Limited flexibility to new data or tasks.


Advantages of LLMs:
* Can continuously learn and improve with more data/feedback.
* One model serves many tasks with fine-tuning.
* Requires less labeled data and expertise to apply.


Disadvantages of LLMs:
* Requires lots of compute time and cost to train from scratch.
* Results can be unpredictable until properly tuned.
* Potential for biased and harmful model behavior.
* Raises issues of model accountability and transparency.
"""

