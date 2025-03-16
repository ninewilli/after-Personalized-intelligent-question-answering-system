from transformers import WhisperProcessor, WhisperForConditionalGeneration

import librosa
import torch
from zhconv import convert
import warnings
processor = WhisperProcessor.from_pretrained("listen/openai/model/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("listen/openai/model/whisper-small")
tokenizer = WhisperProcessor.from_pretrained("listen/openai/model/whisper-small")
warnings.filterwarnings("ignore")
#load audio file
def listen():
    audio_file = f"listen/latestSpeech/output.wav"
    audio, sampling_rate = librosa.load(audio_file, sr=16_000)
    model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language="zh", task="transcribe")
    input_features = processor(audio, return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    # transcription = processor.batch_decode(predicted_ids)

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return convert(transcription, 'zh-cn')
