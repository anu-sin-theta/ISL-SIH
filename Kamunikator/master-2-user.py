import firebase_admin
from firebase_admin import credentials, firestore
import azure.cognitiveservices.speech as speechsdk
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient
from translator import translate_text_azure
import webbrowser
import threading
import time

cred = credentials.Certificate('isl-sih-firebase-adminsdk-34c6u-4b9c452afa.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Azure Speech SDK configuration
speech_key = "db94b5a202ac4a7aacde0b5343ed2264"
service_region = "centralindia"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

translator_key = "538e9f9c82f34fe7a44ebb1151616531"
translator_endpoint = "https://api.cognitive.microsofttranslator.com"
translator_client = TextTranslationClient(endpoint=translator_endpoint, credential=AzureKeyCredential(translator_key))

stop_thread = False
last_data_time = time.time()

def text_to_speech(text):
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def open_video_feed(user):
    url = f"http://127.0.0.1:5000/video_feed/{user}"
    webbrowser.open(url)

def video_feed_thread(user):
    global stop_thread
    open_video_feed(user)
    while not stop_thread:
        time.sleep(1)

if __name__ == "__main__":
    video_thread = None
    while True:
        try:
            anubhav_ref = db.collection('users').document('Sanskar')
            anubhav_doc = anubhav_ref.get()
            all_ref = db.collection('users').document('all')
            all_doc = all_ref.get()

            if anubhav_doc.exists:
                anubhav_data = anubhav_doc.to_dict()
                anubhav_text = anubhav_data.get('output', '')
                if anubhav_text:
                    try:
                        translated_text = translate_text_azure(anubhav_text)
                        text_to_speech(translated_text)
                        if video_thread is None or not video_thread.is_alive():
                            stop_thread = False
                            video_thread = threading.Thread(target=video_feed_thread, args=("Sanskar",))
                            video_thread.start()
                        last_data_time = time.time()
                        anubhav_ref.set({'output': ''})
                    except Exception as e:
                        print(f"Error processing Anubhav's data: {e}")

            if all_doc.exists:
                all_data = all_doc.to_dict()
                all_text = all_data.get('output', '')
                if all_text:
                    try:
                        translated_text = translate_text_azure(all_text)
                        text_to_speech(translated_text)
                        if video_thread is None or not video_thread.is_alive():
                            stop_thread = False
                            video_thread = threading.Thread(target=video_feed_thread, args=("Anubhav",))
                            video_thread.start()
                        last_data_time = time.time()
                        all_ref.set({'output': ''})
                    except Exception as e:
                        print(f"Error processing 'all' data: {e}")

            if not anubhav_doc.exists and not all_doc.exists:
                print("Neither Anubhav nor 'all' documents exist.")

            if time.time() - last_data_time > 9:
                stop_thread = True
                if video_thread is not None:
                    video_thread.join()
                    video_thread = None

        except Exception as e:
            print(f"Error in main loop: {e}")