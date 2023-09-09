# # from gensim import models

# # # Load pre-trained word vectors
# # w = models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, limit=500000)

# # # Calculate gender bias vectors
# # gender_bias_man = w['man'] - w['woman']
# # gender_bias_woman = w['woman'] - w['man']
# # average_gender_bias = (gender_bias_woman + gender_bias_man) / 2

# # # Define sets of words representing men and women
# # men = ['man', 'men', 'boy', 'guy', 'dude', 'male']
# # women = ['woman', 'women', 'girl', 'lady', 'gal', 'female']

# # # Calculate the average vector for words associated with men and women, respectively
# # sum_vector_men = sum(w[word] for word in men)
# # average_vector_men = sum_vector_men / len(men)

# # sum_vector_women = sum(w[word] for word in women)
# # average_vector_women = sum_vector_women / len(women)

# # # Calculate gender-neutral vectors
# # gender_neutral_vector_men = average_vector_men - gender_bias_woman
# # gender_neutral_vector_women = average_vector_women - gender_bias_man

# # # Find gender-neutral similar words
# # neutral_words_men = w.similar_by_vector(gender_neutral_vector_men, topn=10)
# # neutral_words_women = w.similar_by_vector(gender_neutral_vector_women, topn=10)

# # print("Gender-neutral words related to men:")
# # for word, similarity in neutral_words_men:
# #     print(f"{word}: {similarity}")

# # print("\nGender-neutral words related to women:")
# # for word, similarity in neutral_words_women:
# #     print(f"{word}: {similarity}")


# # from gensim.models import KeyedVectors

# # def find_gender_neutral_synonyms(input_word, model_path, limit=50000):
# #     # Load the pre-trained Word2Vec model
# #     word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=limit)
    
# #     # Calculate gender bias vectors
# #     gender_bias_man = word_vectors['man'] - word_vectors['woman']
# #     gender_bias_woman = word_vectors['woman'] - word_vectors['man']
    
# #     # Get the word vector for the input word
# #     input_vector = word_vectors[input_word]
    
# #     # Calculate the gender-neutral vector for the input word
# #     if input_word.lower().endswith('man'):
# #         gender_neutral_vector = input_vector - gender_bias_woman
# #     elif input_word.lower().endswith('woman'):
# #         gender_neutral_vector = input_vector - gender_bias_man
# #     else:
# #         gender_neutral_vector = input_vector
    
# #     # Find similar words to the gender-neutral vector
# #     similar_words = word_vectors.similar_by_vector(gender_neutral_vector, topn=10)
# #     sim = "chairman"
# #     # print(f"sim: {word_vectors[sim]}")
# #     synonyms = [synonym for synonym, _ in word_vectors.most_similar(sim, topn=15)]

# #     print(f"simila_words of {sim}: {synonyms}")

# #     # Filter out any words that contain 'man' or 'woman' to ensure gender neutrality
# #     gender_neutral_synonyms = [word for word, _ in similar_words if 'man' not in word.lower() and 'woman' not in word.lower()]
    
# #     return gender_neutral_synonyms

# # # Example usage:
# # input_word = 'king'
# # model_path = 'GoogleNews-vectors-negative300.bin'
# # gender_neutral_synonyms = find_gender_neutral_synonyms(input_word, model_path)

# # if gender_neutral_synonyms:
# #     print(f"Gender-neutral synonyms of '{input_word}': {', '.join(gender_neutral_synonyms)}")
# # else:
# #     print(f"No gender-neutral synonyms found for '{input_word}'.")


# # import spacy
# # from spacy import displacy
# # nlp = spacy.load("en_core_web_sm")
# # string = "We would like to show you a description here but the site won’t allow us."
# # strdocs = nlp(string)
# # for token in strdocs:
# #     print(f""" 
# #     TOKEN: {token.text}
# # =====
# # {token.tag_ = }
# # {token.head.text = }
# # {token.dep_ = }
# # """
# #     )

# # displacy.serve(strdocs,style = "dep")  

# # import spacy
# # from spacy import displacy

# # text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."

# # nlp = spacy.load("en_core_web_sm")
# # doc = nlp(text)
# # displacy.serve(doc, style="ent")

# # import spacy

# # nlp = spacy.load("en_core_web_sm")
# # doc = nlp("Where are you?")
# # print(doc[2].morph)  # 'Case=Nom|Person=2|PronType=Prs'
# # print(doc[2].pos_)  # 'PRON'

# # import spacy

# # nlp = spacy.load("en_core_web_sm")
# # doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
# # for token in doc:
# #     print(token.text, token.dep_, token.head.text, token.head.pos_,
# # #             [child for child in token.children])
# # import spacy

# # nlp = spacy.load("en_core_web_sm")
# # doc = nlp("Credit and mortgage account holders must submit their requests")

# # root = [token for token in doc if token.head == token][0]
# # print(f"{list(root.rights)[0]=}")
# # subject = list(root.lefts)[0]
# # for descendant in subject.subtree:
# #     assert subject is descendant or subject.is_ancestor(descendant)
# #     print(descendant.text, descendant.dep_, descendant.n_lefts,
# #             descendant.n_rights,
# #             [ancestor.text for ancestor in descendant.ancestors])
# # import transformers


# # from transformers import *
# # import torch

# # model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
# # tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")
# # # model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase-small")
# # # tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase-small")
# # model = model.half()  # Convert model to half-precision


# # def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=2, num_beams=2):
# #   # tokenize the text to be form of a list of token IDs
# #   inputs = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
# #   # generate the paraphrased sentences
# #   outputs = model.generate(
# #     **inputs,
# #     num_beams=num_beams,
# #     num_return_sequences=num_return_sequences,
# #     batch_size=1 # Set a smaller batch size
# #   )
# #   # decode the generated sentences using the tokenizer to get them back to text
# #   return tokenizer.batch_decode(outputs, skip_special_tokens=True)

# # sentence = "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences."
# # # get_paraphrased_sentences(model, tokenizer, sentence, num_beams=10, num_return_sequences=10)
# # get_paraphrased_sentences(model, tokenizer, sentence, num_beams=2, num_return_sequences=2)
# # # Set a smaller batch size
# # torch.cuda.empty_cache()

# import requests

# API_URL = "https://api-inference.huggingface.co/models/tuner007/pegasus_paraphrase"
# headers = {"Authorization": "Bearer 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"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
	
# input = "Google News is a news aggregator service developed by Google. It presents a continuous flow of links to articles organized from thousands of publishers and magazines. Google News is available as an app on Android, iOS, and the Web. Google released a beta version in September 2002 and the official app in January 2006"
# print(f"inputs: {input}")
# output = query({
# 	"inputs": input,
# })
# print(output)

import requests

API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "The answer to the universe is",
})
print(output)


# import requests

# UNICHECK_CLIENT_ID = '19eff14a67717636c590'
# UNICHECK_CLIENT_SECRET = '02299d04a3fdf4e3799c3ce3721ab76ba36c66f3'
# UNICHECK_BASE_URL = 'https://api.unicheck.com'
# def get_access_token():
#     token_url = f'{UNICHECK_BASE_URL}/oauth/access-token'
#     data = {
#         'grant_type': 'client_credentials',
#         'client_id': UNICHECK_CLIENT_ID,
#         'client_secret': UNICHECK_CLIENT_SECRET,
#     }
#     response = requests.post(token_url, data=data)
#     access_token = response.json().get('access_token')
#     return access_token
# def plagiarism_check(text):

# 	access_token = get_access_token()
# 	headers = {f"Authorization": "Bearer {access_token}",
#               "Accept":  "application/vnd.api+json",
#               "Content-Type": "application/vnd.api+json	",
# 			  }
# 	data = {
#             "data": text
#         }
# 	plagcheck_url = f"{UNICHECK_BASE_URL}/similarity/checks"
# 	response = requests.post(plagcheck_url, headers=headers, json = data)
# 	print(response)

# plagiarism_check("I am not ready.")
    