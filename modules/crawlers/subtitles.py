from modules.crawlers.utils import get_parsed_page
from modules.crawlers.utils import extract_content
from modules.crawlers.utils import extract_root

# External libs
import requests, os
import pandas as pd
import time
import srt

# Internal files
from src.utils import extract_zip

class Subtitles():

    def __init__(self, url='https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese%2F'):
        self.url = url
        self.root = extract_root(url)
        self.anime_df = self.get_anime_df()

        self.anime_df = pd.read_parquet('data/animes.parquet')
        self.anime_df = self.get_anime_df()


    def is_anime_link(self, link):
        has_strong = '<strong>' in str(link)
        return has_strong


    def extract_anime_links(self):
        webpage = get_parsed_page(self.url)
        if webpage is not None:
            links = webpage.find_all('a')
            anime_links = filter(self.is_anime_link, links)
            return list(anime_links)
        else:
            return None
    

    def make_anime_tuples(self, anime_links):
        anime_tuples = []

        for link in anime_links:
            name = extract_content(link)
            path = link['href']
            anime_tuples.append((name, path))

        return anime_tuples
    
    
    def get_animes(self):
        anime_links = self.extract_anime_links()
        if anime_links is not None:
            anime_tuples = self.make_anime_tuples(anime_links)
            return anime_tuples
        else:
            return None
    

    def open_animes(self):
        return pd.read_parquet('data/animes.parquet')


    def get_anime_df(self):
        try:
            anime_df = self.open_animes()
        except:
            data = self.get_animes()
            if data is not None:
                anime_df = pd.DataFrame(
                    data,
                    columns=['anime_name', 'anime_path']
                )
                anime_df['anime_id'] = anime_df.index
                anime_df.to_parquet('data/animes.parquet', index=False)
                return anime_df
            else:
                return None
        

    def filter_anime(self, anime_name):
        anime_name = anime_name.lower()
        return self.anime_df[
            self.anime_df.anime_name == anime_name
        ]


    def anime_in_df(self, anime):
        filtered_df = self.filter_anime(anime)
        return len(filtered_df) > 0


    def get_path(self, anime):
        if self.anime_in_df(anime):
            filtered_df = self.filter_anime(anime)
            path = filtered_df['anime_path'].values[0]
        else:
            path = None
        return path


    def get_anime_page(self, anime):
        path = self.get_path(anime)
        webpage = get_parsed_page(self.root+path)
        return webpage


    def is_subtitle_file_link(self, link):
        return (
            '.srt' in str(link) 
            or '.rar' in str(link) 
            or '.zip' in str(link) 
            or '.7z' in str(link)
        )
    
    
    def get_subtitle_file_links(self, webpage):
        return [
            subtitle_file for subtitle_file in webpage.find_all('a')
            if self.is_subtitle_file_link(subtitle_file['href'])
        ]


    def get_subtitle_file_name(self, subtitle_file):
        return extract_content(subtitle_file)
    
    
    def get_subtitle_file_link(self, subtitle_file):
        url = self.root + subtitle_file['href']
        return '%20'.join(
            (url).split()
        )

    
    def get_pre_downloaded_folders(self):
        return os.listdir('data/pre_downloaded_subs')
    
    def get_pre_downloaded_anime_names(self):
        folders = self.get_pre_downloaded_folders()
        return [
            ' '.join(
                a.split('_')
            ).lower() for a in
            folders
        ]


    def get_folder_name(self, pre_downloaded_anime):
        folders = self.get_pre_downloaded_folders()
        animes = self.get_pre_downloaded_anime_names()
        anime_index = animes.index(pre_downloaded_anime)
        return 'data/pre_downloaded_subs/' + folders[anime_index]


    def is_pre_downloaded(self, anime):
        pre_downloaded_animes = self.get_pre_downloaded_anime_names()
        return anime.lower() in pre_downloaded_animes
    
    
    def get_external_subtitlte_files(self, anime):
        webpage = self.get_anime_page(anime)
        
        subtitle_files = self.get_subtitle_file_links(webpage)
        subtitle_file_names = [self.get_subtitle_file_name(subtitle_file) for subtitle_file in subtitle_files]
        subtitle_file_links = [self.get_subtitle_file_link(subtitle_file) for subtitle_file in subtitle_files]

        return subtitle_file_names, subtitle_file_links

    
    def get_subtitle_files_df(self, anime):
        names, links = self.get_external_subtitlte_files(anime)
        subtitle_files_df = pd.DataFrame(
            [], columns=['anime_name', 'subtitle_file_name', 'subtitle_file_link']
        )

        subtitle_files_df['subtitle_file_name'] = pd.Series(names)
        subtitle_files_df['subtitle_file_link'] = pd.Series(links)
        subtitle_files_df['anime_name'] = anime

        return subtitle_files_df


    def is_zip_file(self, filename):
        return (
            '.zip'  in os.path.splitext(filename)[1] or
            '.rar'  in os.path.splitext(filename)[1] or
            '.7z'   in os.path.splitext(filename)[1]
        )


    def download_external_subtitle_files(self, subtitle_files_df):
        subtitle_content  = []
        filenames = []

        for index, row in subtitle_files_df.iterrows():
            if self.is_zip_file(row['subtitle_file_name']):
                zip_filenames, zip_contents = extract_zip(row['subtitle_file_link'])
                if zip_contents is not None:
                    subtitle_content = subtitle_content + zip_contents
                    filenames  = filenames + zip_filenames
            else:
                subtitle_content.append(requests.get(row['subtitle_file_link']).text)
                filenames.append(row['subtitle_file_name'])
            time.sleep(0.05)

        return subtitle_content, filenames
    

    def get_external_subtitle_df(self, anime):
        subtitle_files_df = self.get_subtitle_files_df(anime)
        subtitle_content, filenames = self.download_subtitle_files(subtitle_files_df)
        
        episode_list = []

        for i in range(len(filenames)):
            try:
                subtitles = srt.parse(subtitle_content[i])
                episode_subs = []
                for sub in subtitles:
                    episode_subs = episode_subs + [
                        (anime, filenames[i], sub.start, sub.end, sub.content)
                    ]
                episode_list += [episode_subs]
            except:
                pass

        subtitle_df = pd.DataFrame(
            [item for sublist in episode_list for item in sublist],
            columns=['anime_name', 'filename', 'start_time', 'end_time', 'content']
        )

        return subtitle_df

    
    def get_internal_subtitle_df(self, anime):
        folder = self.get_folder_name(anime)
        files = [
            folder + '/' + name
            for name in os.listdir(folder)
        ]

        episode_list = []

        for name in files:
            try:
                f = open(name, encoding='utf8')
                content = f.read()
                subtitles = srt.parse(content)
                episode_subs = []
                for sub in subtitles:
                    episode_subs = episode_subs + [
                        (anime, name, sub.start, sub.end, sub.content)
                    ]
                episode_list += [episode_subs]
            except:
                pass
            
        subtitle_df = pd.DataFrame(
            [item for sublist in episode_list for item in sublist],
            columns=['anime_name', 'filename', 'start_time', 'end_time', 'content']
        )

        return subtitle_df
    

    def get_subtitle_df(self, anime):
        if self.is_pre_downloaded(anime):
            return self.get_internal_subtitle_df(anime)
        else:
            return self.get_external_subtitle_df(anime)