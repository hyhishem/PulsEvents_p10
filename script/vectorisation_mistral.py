from mistralai import Mistral

client = Mistral(api_key='vCQ3tG5Tn8RQINBzrO69MQiMokXW1cOf')

def get_text_embedding(input):
    embeddings_batch_response = client.embeddings.create(
          model="mistral-embed",
          inputs=input
      )
    return embeddings_batch_response.data[0].embedding
    
text_embeddings = get_text_embedding('Le chat est blanc.')


print(text_embeddings)

print(len(text_embeddings))
