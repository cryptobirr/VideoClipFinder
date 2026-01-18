"""AI-powered transcript analysis using Claude Agent SDK"""
import asyncio
import json
from typing import Any

from claude_agent_sdk import query


class TranscriptAnalyzer:
    """Analyzes video transcripts using Claude Agent SDK"""

    def __init__(self, max_concurrent_chunks: int = 5):
        self.max_concurrent_chunks = max_concurrent_chunks
        self.semaphore = asyncio.Semaphore(max_concurrent_chunks)

    async def analyze_transcript(
        self,
        transcript: str,
        video_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Analyze full transcript and return tagged moments

        Args:
            transcript: Full video transcript with timestamps
            video_metadata: Video title, creator, etc.

        Returns:
            List of moment dictionaries with tags and scores
        """
        # Split transcript into chunks
        chunks = self._chunk_transcript(transcript)

        # Process chunks in parallel with concurrency limit
        tasks = [self._analyze_chunk(chunk, video_metadata) for chunk in chunks]
        chunk_results = await asyncio.gather(*tasks)

        # Flatten and deduplicate moments
        all_moments = []
        for moments in chunk_results:
            all_moments.extend(moments)

        return self._deduplicate_moments(all_moments)

    async def _analyze_chunk(
        self,
        chunk: str,
        video_metadata: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Analyze a single chunk using moment-tagger agent"""
        async with self.semaphore:
            prompt = f"""Use the moment-tagger agent to analyze this transcript chunk.

Video: {video_metadata.get('title', 'Unknown')}
Creator: {video_metadata.get('creator', 'Unknown')}

Transcript:
{chunk}

Return a JSON array of moments with tags and scores."""

            moments = []
            async for message in query(prompt=prompt):
                # Parse agent response for JSON moments
                if hasattr(message, "content"):
                    for block in message.content:
                        if hasattr(block, "text"):
                            # Extract JSON from text
                            text = block.text
                            moments.extend(self._extract_moments_from_text(text))

            return moments

    def _chunk_transcript(
        self,
        transcript: str,
        chunk_size: int = 180,
        overlap: int = 30,
    ) -> list[str]:
        """
        Split transcript into overlapping chunks

        Args:
            transcript: Full transcript text
            chunk_size: Target chunk duration in seconds
            overlap: Overlap duration in seconds

        Returns:
            List of transcript chunks
        """
        # TODO: Implement timestamp-aware chunking
        # For now, split by line count as placeholder
        lines = transcript.split("\n")
        chunks = []
        step_size = max(1, len(lines) // 10)  # ~10 chunks

        for i in range(0, len(lines), step_size):
            chunk = "\n".join(lines[i : i + step_size + 5])  # Add overlap
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def _extract_moments_from_text(self, text: str) -> list[dict[str, Any]]:
        """Extract JSON moments from agent response text"""
        moments = []

        # Try to find JSON blocks in the text
        try:
            # Look for JSON array
            if "[" in text and "]" in text:
                start = text.index("[")
                end = text.rindex("]") + 1
                json_str = text[start:end]
                moments = json.loads(json_str)
        except (ValueError, json.JSONDecodeError):
            # Try to find individual JSON objects
            try:
                if "{" in text and "}" in text:
                    start = text.index("{")
                    end = text.rindex("}") + 1
                    json_str = text[start:end]
                    moment = json.loads(json_str)
                    moments = [moment]
            except (ValueError, json.JSONDecodeError):
                pass

        return moments if isinstance(moments, list) else []

    def _deduplicate_moments(self, moments: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Remove duplicate moments based on timestamp overlap"""
        if not moments:
            return []

        # Sort by start time
        sorted_moments = sorted(moments, key=lambda m: m.get("start_time", 0))

        deduplicated = [sorted_moments[0]]

        for moment in sorted_moments[1:]:
            last_moment = deduplicated[-1]
            last_end = last_moment.get("end_time", 0)
            current_start = moment.get("start_time", 0)

            # If moments don't overlap significantly, keep both
            if current_start >= last_end - 10:  # 10 second tolerance
                deduplicated.append(moment)
            else:
                # Keep the one with higher virality score
                last_score = last_moment.get("virality_scores", {}).get("overall", 0)
                current_score = moment.get("virality_scores", {}).get("overall", 0)
                if current_score > last_score:
                    deduplicated[-1] = moment

        return deduplicated
