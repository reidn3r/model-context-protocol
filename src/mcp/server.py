from fastmcp import FastMCP
mcp = FastMCP("backoffice-mcp")

@mcp.tool()
def area_square(side: float) -> float:
    """Calcula área do quadrado dado o lado."""
    return side * side

# Tool: área do círculo
@mcp.tool()
def area_circle(radius: float) -> float:
    """Calcula área do círculo dado o raio."""
    import math
    return math.pi * radius * radius

if __name__ == "__main__":
    mcp.run()