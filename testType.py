from recommendations.recommendations_pb2 import BookCategory, RecommendationRequest

#Basic check
request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)
print(request.user_id)

#type error
#request = RecommendationRequest(user_id="00A", category=BookCategory.SCIENCE_FICTION, max_results=3)
#print(request.user_id)

# Fields are optionals, you'll need to validate that all them are set
request = RecommendationRequest(user_id=2, category=BookCategory.SCIENCE_FICTION)
print(request.max_results) # 0 is return, is the default value
