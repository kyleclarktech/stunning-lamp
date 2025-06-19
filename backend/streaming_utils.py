"""
WebSocket Streaming Utilities

This module provides utilities for streaming responses through WebSocket connections,
allowing for progressive display of results and better perceived performance.
"""

import json
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class StreamChunk:
    """Represents a chunk of data to be streamed"""
    type: str  # 'query_progress', 'result_chunk', 'final'
    data: Any
    metadata: Optional[Dict] = None

class ResponseStreamer:
    """Handles streaming responses through WebSocket"""
    
    def __init__(self, websocket, chunk_size: int = 5):
        self.websocket = websocket
        self.chunk_size = chunk_size
        self.buffer = []
        
    async def send_chunk(self, chunk: StreamChunk):
        """Send a single chunk through the WebSocket"""
        message = {
            "type": "stream",
            "chunk_type": chunk.type,
            "data": chunk.data
        }
        if chunk.metadata:
            message["metadata"] = chunk.metadata
            
        await self.websocket.send_text(json.dumps(message))
        
    async def stream_query_generation(self, query_parts: List[str]):
        """Stream query generation progress"""
        for i, part in enumerate(query_parts):
            await self.send_chunk(StreamChunk(
                type="query_progress",
                data={"part": part, "progress": (i + 1) / len(query_parts)},
                metadata={"total_parts": len(query_parts)}
            ))
            await asyncio.sleep(0.1)  # Small delay for visual effect
            
    async def stream_results(self, results: List[Dict], total_count: int):
        """Stream results in chunks"""
        # Send initial metadata
        await self.send_chunk(StreamChunk(
            type="result_metadata",
            data={"total_count": total_count, "chunk_size": self.chunk_size}
        ))
        
        # Stream results in chunks
        for i in range(0, len(results), self.chunk_size):
            chunk = results[i:i + self.chunk_size]
            await self.send_chunk(StreamChunk(
                type="result_chunk",
                data={"results": chunk, "start_index": i, "end_index": min(i + self.chunk_size, len(results))},
                metadata={"chunk_number": i // self.chunk_size + 1}
            ))
            
            # Small delay between chunks for better UX
            if i + self.chunk_size < len(results):
                await asyncio.sleep(0.05)
                
        # Send completion signal
        await self.send_chunk(StreamChunk(
            type="stream_complete",
            data={"total_streamed": len(results)}
        ))
        
    async def stream_formatted_response(self, response_generator: AsyncGenerator):
        """Stream a formatted response as it's generated"""
        chunks = []
        async for chunk in response_generator:
            chunks.append(chunk)
            # Send partial response every few chunks
            if len(chunks) % 3 == 0:
                await self.send_chunk(StreamChunk(
                    type="formatted_chunk",
                    data={"content": "".join(chunks), "partial": True}
                ))
                
        # Send final complete response
        await self.send_chunk(StreamChunk(
            type="formatted_chunk",
            data={"content": "".join(chunks), "partial": False}
        ))

class StreamingFormatter:
    """Formats responses for streaming delivery"""
    
    @staticmethod
    async def format_results_streaming(results: List[Dict], query_type: str) -> AsyncGenerator[str, None]:
        """Generate formatted results in a streaming fashion"""
        if query_type == "team_members":
            yield "## Team Members\n\n"
            for i, person in enumerate(results):
                yield f"**{i+1}. {person.get('name', 'Unknown')}**\n"
                yield f"   - Role: {person.get('role', 'N/A')}\n"
                yield f"   - Email: {person.get('email', 'N/A')}\n"
                yield f"   - Department: {person.get('department', 'N/A')}\n\n"
                
        elif query_type == "policy_results":
            yield "## Relevant Policies\n\n"
            for policy in results:
                severity = policy.get('severity', 'normal')
                severity_icon = "🔴" if severity == "critical" else "🟡" if severity == "high" else "🟢"
                yield f"{severity_icon} **{policy.get('name', 'Unknown Policy')}**\n"
                yield f"   - Category: {policy.get('category', 'N/A')}\n"
                yield f"   - Description: {policy.get('description', 'N/A')}\n\n"
                
        else:
            # Generic formatting
            yield f"Found **{len(results)}** results:\n\n"
            for i, result in enumerate(results):
                yield f"{i+1}. "
                for key, value in result.items():
                    if key != 'labels' and value is not None:
                        yield f"**{key}**: {value} | "
                yield "\n"

def create_progress_messages(stage: str) -> List[str]:
    """Create progress messages for different stages"""
    messages = {
        "pattern_matching": [
            "⚡ Checking optimized patterns...",
            "🔍 Analyzing query structure...",
            "✅ Pattern matched!"
        ],
        "ai_generation": [
            "🤖 Preparing AI model...",
            "💭 Generating Cypher query...",
            "✍️ Finalizing query syntax..."
        ],
        "execution": [
            "🔄 Connecting to database...",
            "⚙️ Executing query...",
            "📊 Processing results..."
        ],
        "formatting": [
            "📝 Formatting results...",
            "🎨 Applying style...",
            "✨ Finalizing response..."
        ]
    }
    return messages.get(stage, ["Processing..."])