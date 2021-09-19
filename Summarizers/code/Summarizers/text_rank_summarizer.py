from sumy.summarizers.text_rank import TextRankSummarizer




def summarize(my_parser, sentences_count = 3):
    error = True
    # Initializing the parser

    summarizer = TextRankSummarizer()
    text_rank_summary =summarizer(my_parser.document,sentences_count = sentences_count)
    summary = ''
    for sentence in text_rank_summary:
        summary += str(sentence)
    return summary


