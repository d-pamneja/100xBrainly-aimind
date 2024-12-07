from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from pinecone import Pinecone, ServerlessSpec
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.prompt_values import PromptValue
from langchain_core.runnables import RunnablePassthrough

import validators
import requests
import os
import uuid

from .exception import CustomException
from .logger import logging
from dotenv import load_dotenv
load_dotenv()

import os
import sys
import time

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# OpenAI Instances
openAI_client = OpenAI(api_key=OPENAI_API_KEY)
embedding_model = openAI_client.embeddings

# Pinecone Instances
pc = Pinecone(api_key = PINECONE_API_KEY, environment = PINECONE_API_ENV)
index = pc.Index(PINECONE_INDEX_NAME)

