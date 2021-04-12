from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)

import recommendations_pb2_grpc

#In a real recommendation microservice , the books would be stored in a database
books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id = 1, title = "the Maltese Falcon"),
        BookRecommendation(id = 2, title = "Muder on the orient express"),
        BookRecommendation(id = 3, title = "The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION:[
        BookRecommendation(id = 4, title = "The Hitchhiker's Guide to the galaxy"),
        BookRecommendation(id = 9, title = "Man's search for meaning"),
    ],
}

class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
        
        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    server()