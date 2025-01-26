import json

class SpeakerSettings:
    def __init__(self, data):
        """
        Initializes SpeakerSettings with data from a dictionary.

        Args:
            data (dict): A dictionary containing speaker settings.
        """
        self.tts_engine = data.get("tts_engine", "F5TTS")
        self.autoregressive_model_path = data.get("autoregressive_model_path")
        self.diffusion_model_path = data.get("diffusion_model_path", "")
        self.vocoder_name = data.get("vocoder_name", "")
        self.tokenizer_json_path = data.get("tokenizer_json_path")
        self.voice = data.get("voice", "train_kennard")
        self.tortoise_seed = data.get("tortoise_seed", -1)
        self.sample_size = data.get("sample_size", 2)
        self.tortoise_iterations = data.get("tortoise_iterations", 25)
        self.use_deepspeed = data.get("use_deepspeed", False)
        self.use_hifigan = data.get("use_hifigan", False)
        self.use_s2s = data.get("use_s2s", False)
        self.s2s_engine = data.get("s2s_engine", "RVC")
        self.selected_voice = data.get("selected_voice", "kathrine")
        self.f0method = data.get("f0method", "rmvpe")
        self.index_rate = data.get("index_rate", 0)
        self.f0pitch = data.get("f0pitch", 0)
        self.resample_sr = data.get("resample_sr", "40000:v1 Models")
        self.rms_mix_rate = data.get("rms_mix_rate", 50)
        self.protect = data.get("protect", 33)
        self.filter_radius = data.get("filter_radius", 3)
        self.f5tts_voice = data.get("f5tts_voice", "kathrine")
        self.f5tts_model = data.get("f5tts_model")
        self.f5tts_tokenizer = data.get("f5tts_tokenizer")
        self.f5tts_vocoder = data.get("f5tts_vocoder", "vocos")
        self.f5tts_duration_model = data.get("f5tts_duration_model", False)
        self.f5tts_speed = data.get("f5tts_speed", 100)
        self.f5tts_seed = data.get("f5tts_seed", -1)

    def to_dict(self):
        """
        Converts the SpeakerSettings object back to a dictionary.

        Returns:
            dict: A dictionary representing the speaker settings.
        """
        return self.__dict__

class Speaker:
    def __init__(self, data):
        """
        Initializes a Speaker object with data from a dictionary.

        Args:
            data (dict): A dictionary containing speaker information.
        """
        self.name = data.get("name", "Narrator")
        self.color = data.get("color", "#000000")
        self.settings = SpeakerSettings(data.get("settings", {}))

    def to_dict(self):
        """
        Converts the Speaker object back to a dictionary.

        Returns:
            dict: A dictionary representing the speaker.
        """
        return {
            "name": self.name,
            "color": self.color,
            "settings": self.settings.to_dict()
        }

class Speakers:
    def __init__(self, data):
        """
        Initializes a Speakers object with data from a dictionary.

        Args:
            data (dict): A dictionary containing speaker data.
        """
        self.speakers = {
            speaker_id: Speaker(speaker_data) 
            for speaker_id, speaker_data in data.items()
        }

    def to_dict(self):
        """
        Converts the Speakers object back to a dictionary.

        Returns:
            dict: A dictionary representing the speakers.
        """
        return {
            speaker_id: speaker.to_dict() 
            for speaker_id, speaker in self.speakers.items()
        }

    def __getitem__(self, speaker_id):
        """
        Allows accessing speakers using indexing (e.g., speakers[1]).

        Args:
            speaker_id (str or int): The ID of the speaker.

        Returns:
            Speaker: The Speaker object with the given ID.
        """
        return self.speakers[speaker_id]

    def __setitem__(self, speaker_id, speaker):
        """
        Allows modifying or adding speakers using indexing (e.g., speakers[1] = new_speaker).

        Args:
            speaker_id (str or int): The ID of the speaker.
            speaker (Speaker): The Speaker object to set.
        """
        self.speakers[speaker_id] = speaker