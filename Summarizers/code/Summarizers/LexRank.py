# Importing the parser and tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# Import the LexRank summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer


def summarize(my_parser, sentences_count = 3):
    error = True
    # Initializing the parser

    lex_rank_summarizer = LexRankSummarizer()
    lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count = sentences_count)

    summary = ''
    for sentence in lexrank_summary:
        summary += str(sentence)
    return summary
