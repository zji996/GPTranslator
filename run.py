import os
import glob
from subtitle_translator import SubsTranslator, load_glossary, SubsSummarizer
playrole = 'Act as an translator, spelling corrector and improver. The content I provide to you, you will translate it and answer in the corrected and improved version of my text, Keep the meaning same, but make them more literary. Do not write explanations.'
playrolesummary = 'Act as a Summarizer, spelling corrector and improver. you will summarize subtitle and translate it to other language.'
#以后可能加更多人设进行翻译，现在就先这样吧
language = '简体中文'   # default language 
output_dir = './srtt' # output directory
OpenAI_API = ' ' # OpenAI API 这里输入你的API
srt_files = glob.glob('./srt/**/*.srt', recursive=True)
progress_file = './progress.json'
glossary = load_glossary('./glossary.json') #术语库

if __name__ == '__main__':
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("Choose an option:")
    print("1. Translate only")
    print("2. Summarize only")
    print("3. Translate and summarize")
    print("4. Exit")
    choice = int(input("Enter the number of your choice: "))

    if choice == 4:
        exit()

    for srt_file in srt_files:
        relative_path = os.path.relpath(srt_file, './srt')
        output_file = os.path.join(output_dir, relative_path)

        output_file_dir = os.path.dirname(output_file)
        if not os.path.exists(output_file_dir):
            os.makedirs(output_file_dir)

        if choice in [1, 3]:
            SubsTranslator(srt_file, output_file, language, OpenAI_API, playrole=playrole, relative_path=relative_path, progress_file=progress_file, glossary=glossary)

        if choice in [2, 3]:
            summary_output_file = os.path.splitext(output_file)[0] + '.txt'
            SubsSummarizer(srt_file, summary_output_file, language, OpenAI_API, playrole=playrolesummary, task='Summarize the following text to')