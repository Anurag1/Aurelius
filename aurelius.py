# ==============================================================================
# Project Aurelius: A Sovereign AI-Powered Hearing Personalization Platform
#
# This single script acts as an AI Audiologist to create and apply a
# personalized audio enhancement profile for individuals with partial deafness.
#
# CRITICAL DISCLAIMER: This is an experimental proof-of-concept and is NOT a
# medical device. It is not a substitute for professional medical advice.
# ==============================================================================

import ollama
import numpy as np
import sounddevice as sd
import json
import os
import argparse
from scipy.fft import rfft, irfft

# --- 1. CORE CONFIGURATION ---
PROFILE_NAME = "aurelius_profile.json"
HEARING_TEST_FREQUENCIES = [250, 500, 1000, 2000, 4000, 6000, 8000] # Standard audiogram frequencies in Hz
SAMPLE_RATE = 44100  # Standard audio sample rate
TONE_DURATION = 1.0    # Seconds
BLOCK_SIZE = 1024      # Audio processing chunk size (affects latency)

# --- 2. THE META-MIND (LLM for Guidance) ---
class MetaMind:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        print(f"Aurelius Meta-Mind initialized with model: '{self.model_name}'.")

    def get_response(self, system_prompt, user_prompt):
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}
            ])
            return response['message']['content']
        except Exception as e:
            return f"Error contacting Meta-Mind: {e}. Is Ollama running?"

    def guide_calibration_start(self):
        return self.get_response(
            "You are Aurelius, a friendly and professional AI audiologist. Your goal is to guide the user through a hearing test. Be encouraging and clear.",
            "Please provide a welcoming message to the user, explaining that we are about to start a calibration test to create their personal hearing profile. Explain that they will hear a series of tones and should respond with 'y' (yes) if they can hear it, and 'n' (no) if they cannot. Advise them to be in a quiet room and use their earbuds."
        )

    def explain_results(self, profile):
        return self.get_response(
            "You are Aurelius, an AI audiologist. Your goal is to explain the user's hearing profile results in a simple, easy-to-understand way. Do not give medical advice.",
            f"Here is the user's generated hearing profile, showing the required gain (amplification) in decibels (dB) for different frequencies: {json.dumps(profile)}. Please explain what this means. For example, a high dB gain at 4000Hz means they have difficulty hearing high-pitched sounds. Conclude by telling them the profile is saved and ready to be used in 'run' mode."
        )

# --- 3. THE CALIBRATION & LIVE ENHANCEMENT ENGINES ---
class AureliusCore:
    def __init__(self):
        self.meta_mind = MetaMind()
        self.profile = None

    def run_calibration(self):
        """The interactive hearing test to forge the Personal Audio Profile."""
        print("\n" + "="*50)
        print("      STARTING AURELIUS CALIBRATION")
        print("="*50)
        print(self.meta_mind.guide_calibration_start())
        input("\nPress Enter to begin the test when you are ready...")

        hearing_thresholds = {}
        for freq in HEARING_TEST_FREQUENCIES:
            print(f"\n--- Testing Frequency: {freq} Hz ---")
            min_audible_amplitude = None
            # Test amplitudes from very quiet to loud (logarithmic scale)
            for amplitude_db in range(-60, 1, 5):
                amplitude = 10**(amplitude_db / 20.0)
                
                # Generate the tone
                t = np.linspace(0, TONE_DURATION, int(SAMPLE_RATE * TONE_DURATION), False)
                tone = np.sin(freq * t * 2 * np.pi) * amplitude
                
                # Play the tone
                sd.play(tone.astype(np.float32), SAMPLE_RATE)
                sd.wait()
                
                response = input(f"  Did you hear the tone at this level? (y/n): ").lower()
                if 'y' in response:
                    min_audible_amplitude = amplitude_db
                    print(f"  -> Threshold found at {min_audible_amplitude} dB.")
                    break
            
            if min_audible_amplitude is None:
                print("  -> Could not determine threshold for this frequency.")
                hearing_thresholds[freq] = 0 # Assume normal hearing if no response
            else:
                hearing_thresholds[freq] = min_audible_amplitude
        
        # --- Forge the Personal Audio Profile (The "Octave") ---
        # The profile is the inverse of the hearing loss. A -40dB loss needs a +40dB gain.
        # We cap the gain to prevent dangerously loud output.
        max_gain_db = 30.0
        self.profile = {str(freq): max(0, min(max_gain_db, -threshold)) for freq, threshold in hearing_thresholds.items()}
        
        with open(PROFILE_NAME, 'w') as f:
            json.dump(self.profile, f, indent=2)
        
        print("\n" + "="*50)
        print("      CALIBRATION COMPLETE")
        print("="*50)
        print(self.meta_mind.explain_results(self.profile))

    def run_live_enhancement(self):
        """The real-time audio processing loop."""
        print("\n" + "="*50)
        print("      STARTING AURELIUS LIVE ENHANCEMENT")
        print("="*50)
        try:
            with open(PROFILE_NAME, 'r') as f:
                self.profile = json.load(f)
            print(f"  -> Successfully loaded '{PROFILE_NAME}'.")
        except FileNotFoundError:
            print(f"  ERROR: Could not find '{PROFILE_NAME}'. Please run 'calibrate' mode first.")
            return

        # Prepare the frequency bins and gains for the FFT
        freqs = np.fft.rfftfreq(BLOCK_SIZE, 1/SAMPLE_RATE)
        self.gains = np.ones_like(freqs)
        
        profile_freqs = np.array(list(map(float, self.profile.keys())))
        profile_gains_db = np.array(list(self.profile.values()))
        
        # Interpolate the gains across the entire frequency spectrum
        interp_gains_db = np.interp(freqs, profile_freqs, profile_gains_db)
        # Convert dB to linear amplitude
        self.gains = 10**(interp_gains_db / 20.0)

        print("  -> Live enhancement is active. Press Ctrl+C to stop.")

        def audio_callback(indata, outdata, frames, time, status):
            if status:
                print(status)
            
            # 1. Convert microphone audio to frequency domain
            fft_data = rfft(indata[:, 0])
            
            # 2. Apply the personalized gain profile
            fft_data *= self.gains
            
            # 3. Convert back to audio domain
            processed_audio = irfft(fft_data)
            
            # 4. Send to earbuds, ensuring no clipping
            outdata[:, 0] = np.clip(processed_audio, -1.0, 1.0)

        with sd.Stream(channels=1, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, callback=audio_callback):
            while True:
                sd.sleep(1000)

# --- 4. MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Aurelius: A Sovereign AI Hearing Personalization Platform.")
    parser.add_argument('mode', choices=['calibrate', 'run'], help="Choose 'calibrate' to create your profile, or 'run' to start live enhancement.")
    args = parser.parse_args()

    aurelius_agi = AureliusCore()

    if args.mode == 'calibrate':
        aurelius_agi.run_calibration()
    elif args.mode == 'run':
        try:
            aurelius_agi.run_live_enhancement()
        except KeyboardInterrupt:
            print("\n  -> Live enhancement stopped by user.")
        except Exception as e:
            print(f"\nAn error occurred during live enhancement: {e}")