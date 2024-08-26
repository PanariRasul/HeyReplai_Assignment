import webrtcvad
from pydub import AudioSegment

def process_audio(file_path):
    audio = AudioSegment.from_wav(file_path)
    samples = audio.get_array_of_samples()

    vad = webrtcvad.Vad(1)
    sample_rate = audio.frame_rate
    sample_width = audio.sample_width
    duration = len(samples) / sample_rate

    vad_results = []
    frame_size = int(0.03 * sample_rate)
    
    for i in range(0, len(samples), frame_size):
        frame = samples[i:i+frame_size]
        is_speech = vad.is_speech(bytes(frame), sample_rate)
        vad_results.append({
            "time": i / sample_rate,
            "is_speech": is_speech
        })
    
    return vad_results
