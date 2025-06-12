from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
import torch

class ModelLoader:
    def __init__(self):
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        t2t_pipe = pipeline("text2text-generation", model="google/flan-t5-large", max_new_tokens=1000, min_length=10)
        self.text_llm = HuggingFacePipeline(pipeline=t2t_pipe)
        self.init_chains()

    def init_chains(self):
        empathetic_template = """You are a highly empathetic and skilled analyst in counseling psychology. \
        Carefully observe the user's input, considering the sentiment and emotion extracted from their message. \
        Provide a response that accurately acknowledges their feelings and offers supportive and understanding feedback. \
        Encourage further dialogue by asking thoughtful, open-ended questions and showing genuine interest in their thoughts and experiences. \
        Aim to make the user feel heard, valued, and comfortable, so they are motivated to continue chatting with you. \

        User Input: ```{user_input}``` , Sentiment: ```{sentiment}``` and Emotion: ```{emotion}```"""

        question_template = """You are a very knowledgeable and intelligent individual. \
        You are great at answering questions on a wide range of topics\
        in a concise and easy-to-understand manner. \
        When you don't know the answer to a question, you admit that you don't know. \
        Answer the question by understanding user intentions and feelings from sentiment and emotion given you below with question.

        Take the question below delimited by triple backticks and generate knowledgeable response for user and engage user in conversation.

        question: ```{user_input}```,Sentiment: ```{sentiment}``` and Emotion: ```{emotion}```"""

        general_template = """You are a friendly and engaging conversationalist. \
        You are great at having discussions on a wide range of topics\
        in a thoughtful and enjoyable manner. \
        When you don't have information on a topic, you admit that you don't know. \

        Take the user input below delimited by triple backticks and generate friendly response for user and engage user in conversation.

        user input: ```{user_input}```"""


        prompt_empathetic = PromptTemplate(template=empathetic_template, input_variables=['user_input', 'sentiment', 'emotion'])
        self.empathetic_chain = prompt_empathetic | self.text_llm

        question_prompt = PromptTemplate(template=question_template, input_variables=['user_input', 'sentiment', 'emotion'])
        self.question_chain = question_prompt | self.text_llm

        general_prompt = PromptTemplate(template=general_template, input_variables=['user_input'])
        self.general_chain = general_prompt | self.text_llm

    def get_emotion(self, user_input):
        emotions = [
            "Happiness", "Sadness", "Anger", "Fear", "Surprise", "Disgust", "Excitement", "Trust",
            "Anticipation", "Joy", "Frustration", "Boredom", "Confusion", "Anxiety", "Depression",
            "Enthusiasm", "Love", "Gratitude", "Optimism", "Pessimism", "Jealousy", "Shame", "Guilt",
            "Embarrassment", "Pride"
        ]
        return self.classifier(user_input, emotions)['labels'][0]

    def get_sentiment(self, user_input):
        inputs = self.tokenizer(user_input, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
        predicted_class_id = logits.argmax().item()
        return self.model.config.id2label[predicted_class_id]

    def classify_user_input(self, user_input):
        input_labels = ["is question", "is empathetic or emotional", "general conversation"]
        return str(self.classifier(user_input, input_labels)['labels'][0])

    def get_response(self, chain, user_input, sentiment, emotion):
        response = chain.invoke({
            "user_input": user_input,
            "sentiment": sentiment,
            "emotion": emotion
        })
        return response
    
    def get_general_response(self, chain, user_input):
        return chain.invoke({"user_input": user_input})

    def process_input(self, user_input):
        sentiment = self.get_sentiment(user_input).lower()
        emotion = self.get_emotion(user_input).lower()
        classify_input = self.classify_user_input(user_input)
        response = ''
        if classify_input == "is empathetic or emotional":
            response = self.get_response(self.empathetic_chain, user_input, sentiment, emotion)
        elif classify_input == "is question":
            response = self.get_response(self.question_chain, user_input, sentiment, emotion)
        else:
            response = self.get_general_response(self.general_chain, user_input)
        return response
