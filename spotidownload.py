import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import re

# Set up authentication with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="b85cc0deefc14b86b4216e9e4122d163",
                                                           client_secret="814018c1cd8644578fb730d16dae61d7"))

def sanitize_filename(filename):
    """Remove or replace characters that are not allowed in filenames."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_preview(track_name, output_directory):
    # Search for the track on Spotify
    results = sp.search(q=track_name, type='track', limit=20)  # Increased limit for better results
    if results['tracks']['items']:
        for track in results['tracks']['items']:
            track_name = sanitize_filename(track['name'])
            artist_name = sanitize_filename(track['artists'][0]['name'])
            filename = f"{track_name} - {artist_name}.mp3"
            output_file = os.path.join(output_directory, filename)
            
            preview_url = track['preview_url']
            
            if preview_url:
                print(f"Downloading preview for: {track['name']} by {track['artists'][0]['name']}")
                
                # Download the preview clip
                response = requests.get(preview_url)
                if response.status_code == 200:
                    with open(output_file, 'wb') as file:
                        file.write(response.content)
                    print(f"Preview downloaded successfully as {output_file}")
                    # Stop after downloading the first available preview
                    return  # Exit the function after successfully downloading one preview
                else:
                    print(f"Failed to download preview. Status code: {response.status_code}")
            else:
                print(f"No preview available for: {track['name']} by {track['artists'][0]['name']}")
        print("No previews available for any of the tracks.")
    else:
        print("No results found for the specified track.")

def download_multiple_previews(track_names, output_directory):
    """Download previews for multiple tracks."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for track_name in track_names:
        download_preview(track_name, output_directory)

# List of track names to download
track_names = [
    "Modelito by Mora",
    "Acid Plaat Vieze Asbak Remix",
    "AIRBNB by Mora",
    "DIAMONDS by Dei vi and Mora",
    "DONDE SE APRENDE A QUERER by Mora",
    "Lekkere Boterham",
    "Visstick Gooi Die Kanker Kick",
    "IK TRIP'M",
    "Cluster bomb by USH",
]


output_directory = "C:\\Users\\oscar.cardona\\Previews"  


download_multiple_previews(track_names, output_directory)