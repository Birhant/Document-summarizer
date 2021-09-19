from sumy.summarizers.lsa import LsaSummarizer



def summarize(my_parser, sentences_count = 3):
    error = True
    # Initializing the parser
    summarizer = LsaSummarizer()
    lsa_summary =summarizer(my_parser.document, sentences_count = sentences_count)

    summary = ''
    for sentence in lsa_summary:
        summary += str(sentence)
    return summary


