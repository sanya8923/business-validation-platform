#!/usr/bin/env python
import asyncio
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from validity_crew.crew import ValidityCrew


def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LangChain'
    }
    ValidityCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LangChain"
    }
    try:
        ValidityCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ValidityCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LangChain"
    }
    try:
        ValidityCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def serve():
    """
    Start the FastAPI server.
    """
    import uvicorn
    from validity_crew.api import app
    
    print("Starting Business Validation AI Engine...")
    print("FastAPI server will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "validity_crew.api:app",
        host="0.0.0.0", 
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "serve":
            serve()
        elif sys.argv[1] == "train":
            train()
        elif sys.argv[1] == "replay":
            replay()
        elif sys.argv[1] == "test":
            test()
        else:
            run()
    else:
        run()