from pathlib import Path
from cerebrum.manager.tool import ToolManager

manager = ToolManager(base_url='https://my.aios.foundation')

tool = manager.load_tool(local=True, name='bing_search')

print(tool)