import argparse
import pandas as pd
from functools import partial
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from emoji import demojize
from nltk.tokenize import TweetTokenizer

tokenizer = TweetTokenizer()


def normalize_tweet(tweet):
    norm_tweet = tweet.replace("cannot ", "can not ")
    norm_tweet = norm_tweet.replace("n't ", " n't ")
    norm_tweet = norm_tweet.replace("n 't ", " n't ")
    norm_tweet = norm_tweet.replace("ca n't", "can't")
    norm_tweet = norm_tweet.replace("ai n't", "ain't")

    norm_tweet = norm_tweet.replace("'m ", " 'm ")
    norm_tweet = norm_tweet.replace("'re ", " 're ")
    norm_tweet = norm_tweet.replace("'s ", " 's ")
    norm_tweet = norm_tweet.replace("'ll ", " 'll ")
    norm_tweet = norm_tweet.replace("'d ", " 'd ")
    norm_tweet = norm_tweet.replace("'ve ", " 've ")

    norm_tweet = norm_tweet.replace(" p . m .", "  p.m.")
    norm_tweet = norm_tweet.replace(" p . m ", " p.m ")
    norm_tweet = norm_tweet.replace(" a . m .", " a.m.")
    norm_tweet = norm_tweet.replace(" a . m ", " a.m ")

    return norm_tweet


def replace_user_handles(tweet, replace='@USER'):
    tokens = tokenizer.tokenize(tweet)

    new_tokens = []
    for token in tokens:
        if token.startswith("@"):
            new_tokens.append(replace)
        else:
            new_tokens.append(token)

    return " ".join(new_tokens)


def replace_urls(tweet, replace='HTTPURL'):
    tokens = tokenizer.tokenize(tweet)

    if type(replace) == str:
        new_tokens = []
        for token in tokens:
            lower_token = token.lower()
            if lower_token.startswith("http") or lower_token.startswith("www"):
                new_tokens.append(replace)
            else:
                new_tokens.append(token)

    return " ".join(new_tokens)


def replace_emojis(tweet, replace='demojize'):
    tokens = tokenizer.tokenize(tweet)

    new_tokens = []
    for token in tokens:
        if len(token) == 1:
            if replace == 'demojize':
                new_tokens.append(demojize(token))
            else:
                new_tokens.append(replace)
        else:
            new_tokens.append(token)

    return " ".join(new_tokens)


def preprocess_function(data, preprocessing_config):
    input_col = preprocessing_config['input_col']
    input_col_proc = f"{input_col}_proc"

    data[input_col_proc] = data[input_col]

    if preprocessing_config['lowercase']:
        data[input_col_proc] = data[input_col_proc].str.lower()

    if preprocessing_config['normalize']:
        data[input_col_proc] = data[input_col_proc].apply(normalize_tweet)

    if preprocessing_config['emojis']:
        data[input_col_proc] = data[input_col_proc].apply(partial(replace_emojis, replace=preprocessing_config['emojis']))

    if preprocessing_config['user_handles']:
        data[input_col_proc] = data[input_col_proc].apply(
            partial(replace_user_handles, replace=preprocessing_config['user_handles']))

    elif preprocessing_config['urls']:
        data[input_col_proc] = data[input_col_proc].apply(partial(replace_urls, replace=preprocessing_config['urls']))

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, help="path to the tsv-separated input file.")
    parser.add_argument("--input_col", type=str, help="name of the column where the text is stored in the input file. Default = 'text'", default='text')
    parser.add_argument("--lowercase", help="whether to lowercase the Tweet text before classification.", action='store_true')
    parser.add_argument("--normalize", help="whether to normalize the Tweet text before classification.", action='store_true')
    parser.add_argument("--urls", help="the string used to replace urls in the Tweet text before classification. If False, the urls are not replaced. Options: [str, False]. Default = False", default=False)
    parser.add_argument("--user_handles", help="the string used to replace user handles in the Tweet text before classification. If False, the user handles are not replaced. Options: [str, False]. Default = '@USER'", default='@USER')
    parser.add_argument("--emojis", help="the string used to replace emojis in the Tweet text before classification. If False, the emojis are not replaced. If 'demojize', the emojis are translated to text with the demojize library. Options: [str, 'demojize', False]. Default = 'demojize'", default='demojize')
    parser.add_argument("--output_path", type=str, help="path to the tsv-separated output file. If not provided the output_path is the directory of the input path and an '_out' appended to the input file name.")
    parser.add_argument("--device", type=int, help="determine the device to run the SciTweets Classifier model on. device < 0 uses CPUs only. device > 0 indicates which GPU to use. Default = -1", default=-1)
    args = parser.parse_args()

    input_path = args.input_path
    input_col = args.input_col

    preproc_lowercase = args.lowercase
    preproc_normalize = args.normalize
    preproc_urls = args.urls
    preproc_user_handles = args.user_handles
    preproc_emojis = args.emojis

    output_path = args.output_path

    if not output_path:
        if "/" in input_path:
            input_dir = "/".join(input_path.split("/")[:-1])+"/"
            input_fn = input_path.split("/")[-1]
            print(input_dir)
            print(input_fn)
        else:
            input_dir = ""
            input_fn = input_path

        input_type = input_fn.split(".")[1]
        input_fn = input_fn.split(".")[0]

        output_fn = input_fn+"_out."+input_type
        output_path = input_dir + output_fn

    device = args.device

    data = pd.read_csv(input_path, sep="\t")

    #  example data
    """
    data = pd.DataFrame({'text': [
        "Study on impacts of electricity generation shift via @DukeU https://www.eurekalert.org/news-releases/637217",
        "Study on impacts of electricity generation shift via @DukeU https://www.eurekalert.org/news-releases/637217",
        "Study on impacts of electricity generation shift via @DukeU https://www.eurekalert.org/news-releases/637217"
    ]})
    data.to_csv("Altmetric/scitweets_test.tsv", sep='\t', index=False)
    """

    preprocessing_config = {'input_col': input_col,
                            'lowercase': preproc_lowercase,
                            'normalize': preproc_normalize,
                            'urls': preproc_urls,
                            'user_handles': preproc_user_handles,
                            'emojis': preproc_emojis}

    data = preprocess_function(data, preprocessing_config)

    scitweets_tokenizer = AutoTokenizer.from_pretrained("sschellhammer/SciTweets_SciBert")
    scitweets_model = AutoModelForSequenceClassification.from_pretrained("sschellhammer/SciTweets_SciBert")

    scitweets_pipeline = pipeline('text-classification', model=scitweets_model, tokenizer=scitweets_tokenizer,
                                  device=device)  # device <0 for cpu-only

    res = scitweets_pipeline(data['text'].tolist(), return_all_scores=True)
    data['cat1_score'] = [r[0]['score'] for r in res]
    data['cat2_score'] = [r[1]['score'] for r in res]
    data['cat3_score'] = [r[2]['score'] for r in res]

    data.to_csv(output_path, sep='\t', index=False)


if __name__ == "__main__":
    main()
