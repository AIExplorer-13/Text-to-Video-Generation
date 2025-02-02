from typing import List, Tuple
import os
import math
import random
import numpy as np
import requests
from moviepy.editor import (CompositeVideoClip, ImageSequenceClip, TextClip,
                            VideoFileClip, clips_array, AudioFileClip, CompositeAudioClip)
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.fx.all import crop
from PIL import Image


def get_image_from_url(image_url: str):
    res = requests.get(image_url, stream=True)
    res.raise_for_status()
    return Image.open(res.raw)


def resize_image(image: Image.Image, size: Tuple[int, int]):
    return image.resize(size=size)


def images_to_video(image_urls: List[str], video_size: Tuple[int, int], fps: float = 1/4):
    images = []
    for image_url in image_urls:
        try:
            image = get_image_from_url(image_url)
            images.append(image)
        except Exception as error:
            print(f"Error getting image from url: {image_url}", error)

    images = [resize_image(image, video_size) for image in images]
    # for index, image in enumerate(images):
    #     image.save(f'images/{index}.png')
    np_images = [np.asarray(image) for image in images]
    image_sequence = ImageSequenceClip(np_images, fps=fps)
    return image_sequence


def get_random_clip(required_duration: int) -> VideoFileClip:
    # Randomly select a video from asset videos
    saved_videos = os.listdir('assets/video')
    random_video_path = f'assets/video/{random.choice(saved_videos)}'
    video = VideoFileClip(random_video_path)
    video_duration = int(video.duration)
    # If audio duration is longer than full video duration, just clip the full video
    if (required_duration > video_duration):
        return video

    # Randomly extract a clip from the video that matches the audio duration
    clip_start = random.randint(0, video_duration - required_duration)
    clip: VideoFileClip = video.subclip(
        clip_start, clip_start + required_duration)
    return clip


def crop_clip(clip: VideoFileClip, target_size: Tuple[int, int]):
    original_width, original_height = clip.size
    target_width, target_height = target_size
    # Crop to desired size from center
    x1 = (original_width - target_width) // 2 if target_width < original_width else 0
    x2 = original_width - x1
    y1 = (original_height -
          target_height) // 2 if target_height < original_height else 0
    y2 = original_height - y1
    cropped_clip = crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
    return cropped_clip


def create_video(image_urls: List[str], seconds_per_image: int, audio_filepath: str, video_filepath: str):
    audio_clip = AudioFileClip(audio_filepath)
    
    # Video containing relevant stock images
    images_video = images_to_video(
        image_urls=image_urls, video_size=(1080, 720), fps=1/seconds_per_image)
    
    # Ensure that the image video has the correct duration
    images_video = images_video.subclip(0, audio_clip.duration)
    
    # Set the audio of the images video
    combined_video = images_video.set_audio(audio_clip)
    
    # Write the final video to file
    combined_video.write_videofile(video_filepath)
    return combined_video



def burn_subtitles_into_video(video_filepath: str, subtitles_filepath: str, final_output_filepath: str):
    video = VideoFileClip(video_filepath)

    def generator(text): return TextClip(txt=text, font='Segoe-UI-Bold', fontsize=100,
                                         color='white', stroke_color='black', stroke_width=5,
                                         method='caption', align='center', size=video.size)

    subtitles = SubtitlesClip(subtitles_filepath, generator)
    final_video = CompositeVideoClip(
        [video, subtitles.set_position(('center', 'center'))])

    final_video: VideoFileClip = final_video.subclip(0,-0.1)
    final_video.write_videofile(final_output_filepath)

    return final_video


def main():
    ...


if __name__ == '__main__':
    main()
