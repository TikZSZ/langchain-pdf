from app.chat.redis import client
import random
def random_componenet_by_score(component_type,componenet_map):
    if component_type not in ["llm", "retriever", "memory"]:
        raise ValueError(f"in valid componenet type recieved ${component_type}")
    scores = client.hgetall(f"{component_type}_score_values")
    counts = client.hgetall(f"{component_type}_score_counts")
    valid_componenet_names = componenet_map.keys()

    avg_scores = {}
    for name in valid_componenet_names:
        score = int(scores.get(name,1))
        count = int(counts.get(name,1))
        avg = score/count
        avg_scores[name] = max(avg,0.1)

    ## do a weighted average
    sum_scores = sum(avg_scores.values())
    random_val = random.uniform(0,sum_scores)
    cumulative = 0
    for name, score in avg_scores.items():
        cumulative += score
        if random_val <= cumulative:
            return name

    


def score_conversation(
    conversation_id: str, score: float, llm: str, retriever: str, memory: str
) -> None:
    score = min(max(score,0),1)
    client.hincrby("llm_score_values",llm,score)
    client.hincrby("llm_score_counts",llm,1)
    client.hincrby("retriever_score_values",retriever,score)
    client.hincrby("retriever_score_counts",retriever,1)
    client.hincrby("memory_score_values",memory,score)
    client.hincrby("memory_score_counts",memory,1)


def get_scores():
    aggregate = {
        "llm":{},
        "retriever":{}, 
        "memory":{}
    }
    for component_type in aggregate.keys():
        scores = client.hgetall(f"{component_type}_score_values")
        counts = client.hgetall(f"{component_type}_score_counts")
        for name in scores.keys():
            score = int(scores.get(name,1))
            count = int(counts.get(name,1))
            avg = score/count
            aggregate[component_type][name] = [avg]
    return aggregate

