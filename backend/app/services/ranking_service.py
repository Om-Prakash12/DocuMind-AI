
class ReciprocalRankFusion:
    """
    Combine ranked search results using Reciprocal Rank Fusion.
    """

    def __init__(self, k: int = 60):
        if k <= 0:
            raise ValueError("RRF constant must be greater than zero.")

        self.k = k

    def fuse(
        self,
        *result_lists: list[dict],
        limit: int = 5
    ) -> list[dict]:
        """
        Merge multiple ranked result lists.

        Each result must contain a document dictionary.
        The document dictionary must contain a unique chunk_id.
        """

        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        fused_scores = {}
        documents = {}

        for results in result_lists:
            if not isinstance(results, list):
                raise TypeError("Each result list must be a list.")

            seen_in_list = set()

            for rank, result in enumerate(results, start=1):
                if not isinstance(result, dict):
                    raise TypeError("Each result must be a dictionary.")

                document = result.get("document")

                if not isinstance(document, dict):
                    raise ValueError("Each result must contain a document.")

                chunk_id = document.get("chunk_id")

                if not chunk_id:
                    raise ValueError("Document must contain chunk_id.")

                # Prevent duplicate contribution within one result list
                if chunk_id in seen_in_list:
                    continue

                seen_in_list.add(chunk_id)

                fused_scores[chunk_id] = (
                    fused_scores.get(chunk_id, 0.0)
                    + 1.0 / (self.k + rank)
                )

                documents[chunk_id] = document

        ranked = sorted(
            fused_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        return [
            {
                "rank": index,
                "score": score,
                "document": documents[chunk_id]
            }
            for index, (chunk_id, score) in enumerate(
                ranked[:limit],
                start=1
            )
        ]
