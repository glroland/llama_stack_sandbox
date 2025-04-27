import anyio
import click
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
from calculator import calculator

@click.command()
@click.option("--port", default=8080, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="sse",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    print("Starting Calculator MCP Server...")
    app = Server("calc")

    @app.call_tool()
    async def calculator_tool(name: str, arguments: dict) -> \
                list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        print ("Calculator Tool Invoked.  Name=", name, " Args=", arguments)
    
        if name != "calculator":
            raise ValueError(f"Unknown tool: {name}")

        if "x" not in arguments:
            raise ValueError("Missing required argument 'x'")
        x = float(arguments["x"])

        if "y" not in arguments:
            raise ValueError("Missing required argument 'y'")
        y = float(arguments["y"])

        if "operation" not in arguments:
            raise ValueError("Missing required argument 'operation'")
        operation = arguments["operation"]

        print ("Calling operational function now...")
        return await calculator(x, y, operation)

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        print ("List Tools invoked...")
        return [
            types.Tool(
                name="calculator",
                description="Performs the provided mathematical operation against two provided numbers.",
                inputSchema={
                    "type": "object",
                    "required": ["x", "y", "operation"],
                    "properties": {
                        "x": {
                            "type": "float",
                            "description": "First Number",
                        },
                        "y": {
                            "type": "float",
                            "description": "Second Number",
                        },
                        "operation": {
                            "type": "string",
                            "description": "One of the following opreations to perform: add, subtract, multiply, or divide",
                        },
                    },
                },
            )
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0

if __name__ == '__main__':
    main()
