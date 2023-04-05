import os
import glob
from subtitle_translator import SubsTranslator, load_glossary
playrole = 'Act as an translator, spelling corrector and improver. The content I provide to you, you will translate it and answer in the corrected and improved version of my text, Keep the meaning same, but make them more literary. Do not write explanations.'
#以后可能加更多人设进行翻译，现在就先这样吧
language = '中文'   # default language 
output_dir = './srtt' # output directory
OpenAI_API = ' ' # OpenAI API 这里输入你的API
srt_files = glob.glob('./srt/**/*.srt', recursive=True)
progress_file = './progress.json'
glossary = load_glossary('./glossary.json') #术语库

if __name__ == '__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for srt_file in srt_files:
        relative_path = os.path.relpath(srt_file, './srt')
        output_file = os.path.join(output_dir, relative_path)

        output_file_dir = os.path.dirname(output_file)
        if not os.path.exists(output_file_dir):
            os.makedirs(output_file_dir)

        SubsTranslator(srt_file, output_file, language, OpenAI_API,playrole = playrole, relative_path=relative_path, progress_file=progress_file,glossary=glossary)