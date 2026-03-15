# KittenTTS OpenAI-compatible text-to-speech (TTS) API

Text-to-Speech API compatible with OpenAI TTS API format, built with [KittenTTS](https://github.com/KittenML/KittenTTS).

## Quick Start

### Docker

Build and run the Docker container in detached mode:

```bash
docker compose up -d --build
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements-api.txt

# Set API key (optional)
export KITTEN_TTS_API_KEY="your-api-key"

# Run the server
python main.py
```

Access the Web UI at **http://localhost:7860/**

![Demo](Screenshot_20260219_133313.png)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/audio/speech` | POST | Generate speech from text |
| `/v1/audio/models` | GET | List available models |
| `/v1/audio/voices` | GET | List available voices |
| `/swagger` | GET | API documentation |

### POST /v1/audio/speech

Generate speech from text.

**Request Body:**
```json
{
  "model": "kitten-tts-mini",
  "input": "Hello world",
  "voice": "Jasper",
  "response_format": "wav",
  "speed": 1.0
}
```

**Parameters:**
- `model` (required): Model name. Available: `kitten-tts-mini`, `kitten-tts-micro`, `kitten-tts-nano`
- `input` (required): Text to generate audio for (max 4096 characters)
- `voice` (required): Voice name. Available: `Bella`, `Jasper`, `Luna`, `Bruno`, `Rosie`, `Hugo`, `Kiki`, `Leo`
- `response_format` (optional): Audio format. Available: `wav`, `mp3`, `flac`, `opus`, `pcm`. Default: `wav`
- `speed` (optional): Speed of audio. Range: 0.25-4.0. Default: 1.0

**Response:**
Audio file in specified format

### GET /v1/audio/models

List available models.

**Response:**
```json
{
  "models": [
    {"id": "kitten-tts-mini", "name": "kitten-tts-mini"},
    {"id": "kitten-tts-micro", "name": "kitten-tts-micro"},
    {"id": "kitten-tts-nano", "name": "kitten-tts-nano"}
  ]
}
```

### GET /v1/audio/voices

List available voices.

**Response:**
```json
{
  "voices": [
    {"name": "Bella", "id": "Bella"},
    {"name": "Jasper", "id": "Jasper"},
    {"name": "Luna", "id": "Luna"},
    {"name": "Bruno", "id": "Bruno"},
    {"name": "Rosie", "id": "Rosie"},
    {"name": "Hugo", "id": "Hugo"},
    {"name": "Kiki", "id": "Kiki"},
    {"name": "Leo", "id": "Leo"}
  ]
}
```

## Configuration

### API Key

Set via environment variable:

```bash
export KITTEN_TTS_API_KEY="your-secure-key"
```

If not set, defaults to `sk-kitten-default-key`.

### Models

| Model | Hugging Face |
|-------|--------------|
| `kitten-tts-mini` | KittenML/kitten-tts-mini-0.8 |
| `kitten-tts-micro` | KittenML/kitten-tts-micro-0.8 |
| `kitten-tts-nano` | KittenML/kitten-tts-nano-0.8 |

### Voices

Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo

## Documentation

- Swagger UI: http://localhost:7860/swagger

## License

MIT
