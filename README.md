# Project Aurelius: Your Sovereign AI Audiologist

**CRITICAL DISCLAIMER:** This is an experimental proof-of-concept and is **NOT a medical device**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified audiologist regarding your hearing health. Use at your own risk.

## The Vision: A Personalized Audio World

Project Aurelius is an AI-powered hearing personalization platform that runs entirely on your local machine. Instead of a generic amplifier, Aurelius acts as your personal **AI Audiologist**. It learns your unique hearing profile and then enhances real-world audio in real-time, making sounds clearer and more vibrant, tailored specifically for you.

### How It Works: A Two-Step Process
1.  **Calibration (The Hearing Test):** In this mode, the AI's **Meta-Mind** guides you through a simple, interactive hearing test. It plays tones at different frequencies to map out your unique hearing abilities.
2.  **Live Enhancement (The Hearing Aid):** The results of your test are used to create a **Personal Audio Profile** (your frozen `Octave` skill). In 'run' mode, Aurelius uses this profile to process audio from your microphone, boosting only the frequencies you have trouble hearing, and sends the crystal-clear audio to your Bluetooth earbuds.

---

## How to Run the Live Test

### Step 1: System Prerequisites
*   **A quiet room**
*   **A good quality microphone**
*   **A pair of headphones or Bluetooth earbuds**
*   **Ollama** (for the AI guide): Install from [https://ollama.com/](https://ollama.com/) and run `ollama pull llama3`.
*   **PortAudio** (for audio processing):
    *   **Mac:** `brew install portaudio`
    *   **Ubuntu/Debian:** `sudo apt-get install libportaudio2`
    *   **Windows:** PortAudio is often included with Python audio libraries, but if you have issues, you may need to install it manually.

### Step 2: Set Up the Project
1.  Clone this repository and set up the Python environment:
    ```bash
    git clone https://github.com/your-username/Project-Aurelius.git
    cd Project-Aurelius
    pip install -r requirements.txt
    ```

### Step 3: Calibrate and Create Your Personal Profile
This is the most important step. Run the script in `calibrate` mode.
```bash
python aurelius.py calibrate