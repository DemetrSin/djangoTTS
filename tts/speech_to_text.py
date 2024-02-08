from pydub import AudioSegment
import speech_recognition as sr


class STT:
    recognizer = sr.Recognizer()

    @staticmethod
    def mp3_to_wav(mp3_file, wav_file):
        audio = AudioSegment.from_mp3(mp3_file)
        audio.export(wav_file, format="wav")
        return wav_file

    def audio_to_text(self, audiofile):
        with sr.AudioFile(audiofile) as source:
            duration = source.DURATION
            total_duration_processed = 0
            chunk_duration = 10
            full_text = ''
            while total_duration_processed < duration:
                recorded_audio = self.recognizer.listen(source, phrase_time_limit=duration)
                total_duration_processed += chunk_duration
                print("Processed {} seconds out of {} seconds".format(total_duration_processed, duration))

                try:
                    text = self.recognizer.recognize_google(
                        recorded_audio,
                        language="en-US"
                    )
                    full_text += text

                except:
                    pass
            return full_text
