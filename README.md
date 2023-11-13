# SciTweets-Classifier

This repository contains the SciTweets Classifier that was trained in section 3 of the paper *Hafid, Salim, et al. "SciTweets-A Dataset and Annotation Framework for Detecting Scientific Online Discourse." Proceedings of the 31st ACM International Conference on Information & Knowledge Management. 2022, [download](https://dl.acm.org/doi/10.1145/3511808.3557693).* 

The SciTweets Classifier distinguishes three different forms of science-relatedness for Tweets:

(1) Scientific knowledge (scientifically verifiable claims): Tweets that include a claim or a question that could be scientifically verified, 

(2) Reference to scientific knowledge: Tweets that include at least one reference to scientific knowledge (references can either be direct, e.g., DOI, title of a paper or indirect, e.g., a link to an article that includes a direct reference), and 

(3) Related to scientific research in general: Tweets that mention a scientific research context (e.g., mention a scientist, scientific research efforts, research findings).

Refer to the **annotation_framework.pdf** in https://doi.org/10.7802/2434 for more information about the categories and how the training data was annotated. 

__Table of contents:__
- [Contents of the Repository](#contents-of-the-repository)
- [Usage](#usage)
- [Data](#data)
- [Publication](#publication)
- [Licensing](#licensing)
- [Contact](#credits)
- [Acknowledgment](#acknowledgment)

## Contents of the Repository

This repository contains the following directories and files:

1. **scitweets_classifier.py** code that runs the SciTweets Classifier
2. **scitweets_test.tsv** exemplary input file
3. **scitweets_test_out.tsv** exemplary output file
4. **requirements.txt** python libraries required to run the SciTweets Classifier
4. **LICENSE** license file
5. **Readme.md** this file


## Usage
First, if not already present in your active python3 environment, install the required libraries (see *requirements.txt*) with:
```
pip install -r requirements. txt
```
Next, you can run the SciTweets Classifier with 

```
python3 scitweets_classifier.py --input_path scitweets_test.tsv --input_col text --lowercase --normalize --urls False --user_handles @USER --emojis demojize --output_path scitweets_test_out.tsv --device -1
```
, where
- input_path: specifies the path to the tsv-separated input file
- input_col: specifies the column where the text is stored (if not provided, default column is 'text')
- lowercase: specifies whether to lowercase the Tweet text before classification
- normalize: specifies whether to normalize the Tweet text before classification
- urls: specifies the string used to replace urls in the Tweet text before classification. If False, the urls are not replaced. Options: [str, False]. Default = False
- user_handles: specifies the string used to replace user handles in the Tweet text before classification. If False, the user handles are not replaced. Options: [str, False]. Default = '@USER'
- emojis: specifies the string used to replace emojis in the Tweet text before classification. If False, the emojis are not replaced. If 'demojize', the emojis are translated to text with the demojize library. Options: [str, 'demojize', False]. Default = 'demojize'
- output_path: specifies the path to the tsv-separated output file. If not provided the output_path is the directory of the input path and an '_out' appended to the input file name.
- device: specifies the device to run the SciTweets Classifier model on. device < 0 uses CPUs only. device > 0 indicates which GPU to use (e.g., 1 to use GPU with index 1). Default = -1.
    
## Data
The input data, as specified with the *input_path* parameter needs to be a tsv-separated file with one line per Tweet text. If the name of the column that stores the Tweet texts is not 'text', specify the column name in *input_col*.

See the exemplary *scitweets_test.tsv* input file. 

The output data has four additional columns:
- one column for the preprocessed text (the text that is handed to the classifier)
- three columns for the scores of the three categories of science-relatedness (see categories above)

See the exemplary *scitweets_test_out.tsv* output file. 


## Publication:
<!-- TODO: Update with correct information once we uploaded the paper somewhere -->
Please cite the following paper if you are using the SciTweets classifier

1. *Hafid, Salim, et al. "SciTweets-A Dataset and Annotation Framework for Detecting Scientific Online Discourse." Proceedings of the 31st ACM International Conference on Information & Knowledge Management. 2022, [download](https://dl.acm.org/doi/10.1145/3511808.3557693).*

```bib
@inproceedings{hafid2022scitweets,
  title={SciTweets-A Dataset and Annotation Framework for Detecting Scientific Online Discourse},
  author={Hafid, Salim and Schellhammer, Sebastian and Bringay, Sandra and Todorov, Konstantin and Dietze, Stefan},
  booktitle={Proceedings of the 31st ACM International Conference on Information \& Knowledge Management},
  pages={3988--3992},
  year={2022}
}
```

## Licensing
This code is published under the MIT license (https://opensource.org/license/mit/). 

## Contact
Please contact sebastian.schellhammer@gesis.org

## Acknowledgment
This work is supported by the AI4Sci grant, co-funded by MESRI (France) and BMBF (Germany, grant 01IS21086) and the French National Research Agency (ANR).
