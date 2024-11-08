import azure.cognitiveservices.speech as speechsdk

def recognize_speech_from_microphone(subscription_key, region):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)


    print("Speak into your microphone.")

    # Start speech recognition
    result = speech_recognizer.recognize_once_async().get()


    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return "Recognized: {}".format(result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized: {}".format(result.no_match_details)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        error_message = "Speech Recognition canceled: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            error_message += "\nError details: {}".format(cancellation_details.error_details)
        return error_message


if __name__ == "__main__":
    while 1:
        speech_key = "db94b5a202ac4a7aacde0b5343ed2264"
        service_region = "centralindia"
        result = recognize_speech_from_microphone(speech_key, service_region)
        print(result)