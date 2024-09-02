import math
import sys
from uuid import uuid4
from image_fetcher import fetch_images
from subtitle_generator import generate_subtitles
from video_maker import burn_subtitles_into_video, create_video
from voice_generator import text_to_speech

def generate_video(topic: str):
    # Use your custom title and content directly
    video_title = "Hyundai's IPO and Market Impact in India"
    video_script = """Hi everybody! Hyundai is one of the most iconic companies to enter the Indian markets. It is hard to believe that a South Korean brand, which was once a difficult name to pronounce, is today about to launch the biggest IPO in the history of India. Indian stock markets could soon see their biggest ever IPO. South Korean automaker Hyundai is gearing up for a significant milestone by going public in India. Hyundai's IPO is poised to be one of the largest in recent times, potentially the biggest IPO ever in India. This would be India's largest IPO and the first van automaker since Maruti Suzuki in 2003. In 1996, when Hyundai entered the Indian market, Maruti was the most dominant player with a 60% market share, almost a monopoly amongst the middle class in India. Despite this, Hyundai came in with models like Santro, i10, i20, and Creta, making a significant impact. Today, Hyundai is the second-largest automaker in the country with a profit of 4,653 crores. In terms of profitability, Hyundai is way ahead of Maruti. In FY23, while Hyundai made a profit of 65,355 rupees per vehicle, Maruti made a profit of 4,939 rupees per vehicle. Now, after 28 years of establishing a stronghold in the Indian market, Hyundai plans to raise 25,000 crores with its IPO. Sounds fantastic, right? However, there are some hidden risks that Hyundai faces which may jeopardize all the progress they've made in India. All of this is detailed in a 436-page DRHP paper that Hyundai filed with SEBI. We've gone through all this data so that you can sit back and consume the most important bits of this 400-page document as easily as watching a movie. In this episode, let's dive into understanding how a South Korean company like Hyundai broke into the Indian automobile market, leaving behind giants like Tata and Mahindra. Despite being a foreign company, how did Hyundai achieve such high profitability and outpace a mammoth like Maruti in India? Most importantly, after making such amazing progress, what are the hidden risks that could topple Hyundai's growth in India? Also, a quick disclaimer: I am not a SEBI-registered investment adviser, and this video is not meant to give you investment advice but to only educate you about the rise of Hyundai in India. Before we move on, I want to quickly introduce you to our education partners of today's episode, Scaler School of Business. They are bringing something absolutely revolutionary. If you're seeking business education, Scaler is offering a full-time on-campus 18-month PG program in management and technology. This program is designed by leaders who have built billion-dollar businesses like Uber, Myntra, and Meesho. Today, legacy college names are useless without competitive skill sets. This is why, as part of the Scaler School of Business curriculum, you will work on real-world projects sourced from real companies. You will build your own business, take it to the market, generate revenue, and raise VC capital while studying on campus. Since Scaler has been in the education industry for seven long years, they already have access to 1,200+ company partners, something no other B-School in the country can offer right now. For their online programs, they've seen placement rates of 96% with a median CTC of 25 lakh rupees, verified by B2K Analytics, the same partner that verifies reports for IIMs. Now, Scaler School of Business is handpicking only 75 students for their founding cohort starting in August 2024. They have scholarships up to 100%, and applications are open right now. If you want to become a brilliant business leader, apply for Scaler School of Business using the link in my description and in the comment section. Now, on with the episode. The first thing you need to understand about a company is their philosophy of success. In this case, you need to understand what exactly is the philosophy that turned Hyundai into what it is today in India. Like we saw in the Boeing video, no matter how much profitability, EBITDA, or earnings per share a company has, if it deviates from its core philosophy, all these numbers will go for a toss. So let's understand the core philosophy and then move on to profitability, EBITDA, and other numbers. Now the question is, what exactly is the secret recipe for Hyundai's success in India? This story dates back to the early 1990s. Until this point, India only had a few car brands: Hindustan Ambassador, Contessa, Premier Padmini, Standard Herald, 2000, Maruti 800, Omni, and Gypsy."""
    keywords = ["Hyundai", "IPO", "automaker"]
    audio_filepath = f'output/audio/{uuid4()}.mp3'
    video_filepath = f'output/video/{uuid4()}.mp4'
    subtitles_filepath = f'output/subtitles/{uuid4()}.srt'
    final_output_filepath = f'output/final/{uuid4()}.mp4'
    seconds_per_image = 4

    # Generate voice-over narration using text-to-speech
    print("Generating voice-over narration...")
    tts_audio = text_to_speech(
        text=video_script, audio_filepath=audio_filepath)
    
    # Compute number of images required to fit voiceover duration
    number_of_images_required: int = math.ceil(
        tts_audio.duration / seconds_per_image)

    # Fetch images related to generated keywords
    print("Fetching images...")
    image_urls = fetch_images(
        search_terms=keywords, number_of_images=number_of_images_required)

    if not image_urls:
        print('No images found')
        sys.exit()

    print("Creating video...")
    create_video(image_urls=image_urls, seconds_per_image=seconds_per_image,
                 audio_filepath=audio_filepath, video_filepath=video_filepath)

    # Generate subtitles based on audio file
    print("Generating subtitles...")
    generate_subtitles(audio_filepath, subtitles_filepath)

    # Burn subtitles into video
    print("Burning subtitles...")
    burn_subtitles_into_video(
        video_filepath=video_filepath, subtitles_filepath=subtitles_filepath, final_output_filepath=final_output_filepath)


def main():
    topic_word_limit = 5
    while True:
        topic = input('Enter a topic: ')
        if (len(topic.split(' ')) <= topic_word_limit):
            break
        print(f'Topic must be {topic_word_limit} or less')
    generate_video(topic=topic)


if __name__ == '__main__':
    main()
