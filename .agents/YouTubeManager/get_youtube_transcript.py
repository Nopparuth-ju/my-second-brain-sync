import sys
import re
import os
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing package: {package}...", flush=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure youtube-transcript-api is installed
install_and_import('youtube_transcript_api')

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

def extract_video_id(url):
    pattern = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def main():
    if len(sys.argv) < 2:
        print("Error: Please provide a YouTube URL as an argument.", file=sys.stderr)
        sys.exit(1)
        
    url = sys.argv[1]
    video_id = extract_video_id(url)
    
    if not video_id:
        print(f"Error: Invalid YouTube URL: {url}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Fetching transcript for video ID: {video_id}...", flush=True)
    
    try:
        # Instantiate the API class
        api = YouTubeTranscriptApi()
        
        # Get list of transcripts available
        transcript_list = api.list(video_id)
        
        transcript = None
        
        # Try to find Thai transcript
        try:
            transcript = transcript_list.find_transcript(['th'])
        except NoTranscriptFound:
            # Try to find English transcript
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                # Fallback to the first available transcript in the list
                for t in transcript_list:
                    transcript = t
                    break
        
        if not transcript:
            print("Error: No transcript (Thai, English, or others) could be found for this video.", file=sys.stderr)
            sys.exit(1)
            
        print(f"Selected transcript language: {transcript.language} ({transcript.language_code})", flush=True)
        data = transcript.fetch()
        
        # Format transcript text with basic timing blocks (every 30 seconds or so)
        full_text = []
        current_time = 0.0
        block_text = []
        
        for entry in data:
            block_text.append(entry.text)
            # Chunk text into readable paragraphs approximately every 30 seconds
            if entry.start - current_time > 30.0:
                time_str = f"[{int(current_time // 60):02d}:{int(current_time % 60):02d}]"
                full_text.append(f"{time_str} {' '.join(block_text)}")
                block_text = []
                current_time = entry.start
                
        if block_text:
            time_str = f"[{int(current_time // 60):02d}:{int(current_time % 60):02d}]"
            full_text.append(f"{time_str} {' '.join(block_text)}")
            
        output_content = "\n\n".join(full_text)
        
        # Write to temporary file for the agent to read
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_transcript.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)
            
        print(f"SUCCESS: Transcript successfully saved to {output_path}", flush=True)
        
    except TranscriptsDisabled:
        print("Error: Subtitles are disabled for this video.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
