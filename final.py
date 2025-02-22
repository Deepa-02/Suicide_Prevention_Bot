import os
import smtplib
from email.mime.text import MIMEText
from langchain.prompts import PromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.embeddings import OllamaEmbeddings
import chainlit as cl
import azure.cognitiveservices.speech as speechsdk
import pyaudio
import wave
from textblob import TextBlob
import requests
import httpx

load_dotenv()

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")
AZURE_SPEECH_ENDPOINT = os.getenv("AZURE_SPEECH_ENDPOINT")

GEOLOCATION_API_KEY = os.getenv("GEOLOCATION_API_KEY")  

prompt_template = """ 
    You are a compassionate therapy assistant, dedicated to providing support to individuals who may be experiencing emotional distress, sadness, or difficult personal challenges. Drawing from psychological principles, including insights from the book Psychology of Human Relations by Stevy Scarbrough, PhD, you aim to offer thoughtful guidance, motivational stories, and assistance in navigating tough emotions.

    Your task is to be present and empathetic. If a person reaches out feeling down or overwhelmed, you are there to listen and offer supportive responses. You are trained to recognize emotional cues, such as sadness, anger, or frustration, and respond accordingly. If the user expresses a desire to end the conversation, you will respect that choice and gently close the dialogue.

    In addition to text responses, you are capable of handling voice inputs, transcribing them, and analyzing the emotional tone. When appropriate, based on the mood detected, you will offer motivational stories that can uplift and inspire the person, pulling from real-life experiences or insights that can help shift their perspective.
    
    Context: {context} Question: {question}

    Helpful answer:
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=prompt_template, input_variables=['context', 'question'])
    return prompt

def retrieval_qa_chain(llm, prompt, db):
    return RetrievalQA.from_chain_type(
        llm, retriever=db.as_retriever(), chain_type_kwargs={"prompt": prompt}
    )

def load_llm():
    return ChatGroq(model="llama3-8b-8192", temperature=0.5)

def qa_bot():
    index_name = "suicidalbot"
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    db = PineconeVectorStore.from_existing_index(index_name, embeddings)

    llm = load_llm()
    qa_prompt = set_custom_prompt()
    return retrieval_qa_chain(llm, qa_prompt, db)

def fetch_geolocation_by_ip():
    try:
        ip = requests.get('https://api.ipify.org').text  
        response = requests.get(f"https://apiip.net/api/check?accessKey={GEOLOCATION_API_KEY}&ip={ip}")
        response.raise_for_status()  
        location = response.json()
        return location
    except Exception as e:
        print(f"Error fetching geolocation by IP: {e}")
        return None

def fetch_geolocation():
    location = fetch_geolocation_by_ip()
    if location:
        print("Geolocation fetched successfully!")
        return location
    else:
        print("Could not fetch geolocation.")
        return None

def send_notification(email, message, location=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    subject = 'Suicidal Attempt Detected'
    body = f"Conversations related to suicidal attempt:\n\n{message}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'therapybot@example.com'
    msg['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())

def record_audio(filename, duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    print("Recording...")

    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    """
    Transcribe audio using Azure Speech Service
    """
    
    speech_config = speechsdk.SpeechConfig(
        subscription=AZURE_SPEECH_KEY, 
        region=AZURE_SPEECH_REGION
    )
    
    
    speech_config.speech_recognition_language = "en-US"
    
 
    audio_config = speechsdk.audio.AudioConfig(filename=filename)
    

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )
    
 
    result = speech_recognizer.recognize_once_async().get()
    

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Transcript: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
        return "Sorry, I couldn't understand what you said."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
        return "Speech recognition was canceled."
    return ""

def detect_mood(text):
    sentiment = TextBlob(text).sentiment.polarity
    if sentiment < 0.1:
        return "sad"
    elif 0.1 <= sentiment <= 0.5:
        return "neutral"
    else:
        return "happy"

def fetch_story_from_web(mood):
    search_url = "https://www.googleapis.com/customsearch/v1"
    api_key = os.getenv("GOOGLE_API")
    search_id='2532473ff45e94bfe'
    query = f"real motivational stories for {mood} mood"

    response = httpx.get(search_url,params={'key':api_key,'cx':search_id,'q': query, 'count': 1})
    response.raise_for_status()
    results = response.json()

    try:
        story_title = results['items'][0]['title']
        story_snippet = results['items'][0]['snippet']
        story_url = results['items'][0]['link']
        return f"{story_title}\n\n{story_snippet}\n\nRead more: {story_url}"
    except KeyError:
        return "Sorry, I couldn't fetch a story at the moment. Please try again later."

@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = '''Welcome to the Therapy Bot.
                I'm here to listen, support, and guide you through any emotions you're experiencing. Feel free to share what's on your mind—there's no judgment here.
                You can also record a voice message by typing 'record voice'. Take your time. I'm here when you're ready. 😊'''
    await msg.update()

    cl.user_session.set("chain", chain)
    cl.user_session.set("query_count", 0)
    cl.user_session.set("user_messages", [])

suicidal_keywords = ['suicide', 'self-harm', 'end my life', 'suicidal thoughts', 'kill myself']

@cl.on_message
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")
    query_count = cl.user_session.get("query_count", 0)
    user_messages = cl.user_session.get("user_messages", [])

    if chain is None:
        return

    try:
        if (message.content != 'record voice'):
            user_messages.append(message.content)
            cl.user_session.set("user_messages", user_messages)

        if message.content.lower() == 'record voice':
            audio_filename = 'user_audio.wav'
            record_audio(audio_filename)
            transcript = transcribe_audio(audio_filename)
            message.content = transcript
            user_messages.append(message.content)
            cl.user_session.set("user_messages", user_messages)

        full_conversation = " ".join(user_messages)

        for keyword in suicidal_keywords:
            if keyword in message.content.lower():
                location = fetch_geolocation()
                email = 'deepalakshmithamodharan@gmail.com'
                if location:
                    location_details = (
                        f"\n\n\nLocation Information:\n"
                        f"IP Address: {location['ip']}\n"
                        f"City: {location.get('city', 'Unknown')}\n"
                        f"Region: {location.get('regionName', 'Unknown')}\n"
                        f"Country: {location.get('countryName', 'Unknown')}\n"
                        f"PostalCode: {location.get('postalCode', 'Unknown')}\n"
                        f"Latitude: {location.get('latitude', 'Unknown')}\n"
                        f"Longitude: {location.get('longitude', 'Unknown')}\n"
                        )
                    send_notification(email, full_conversation + location_details, location)
                else:
                    send_notification(email, full_conversation, None)
                break
            
        mood = detect_mood(full_conversation)

        query_count += 1
        cl.user_session.set("query_count", query_count)

        if query_count % 3 == 0:
            story = fetch_story_from_web(mood)
            await cl.Message(content=f"I understand that you're in a {mood} mood. Here's a motivational story for you:\n\n{story}").send()

        res = await chain.acall({'query': message.content})
        answer = res['result']
        await cl.Message(content=answer).send()
    
    except Exception as e:
        await cl.Message(content=f"An error occurred: {e}").send()