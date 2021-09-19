from sumy.summarizers.luhn import LuhnSummarizer




def summarize(parser, sentences_count = 3):
    # Initializing the parser
    summarizer = LuhnSummarizer()
    luhn_summary =summarizer(parser.document, sentences_count = sentences_count)
    summary = ''
    for sentence in luhn_summary:
        summary += str(sentence)
    return summary




