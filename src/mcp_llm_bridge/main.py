# src/mcp_llm_bridge/main.py
import os
import asyncio
from dotenv import load_dotenv
from mcp import StdioServerParameters
from mcp_llm_bridge.config import BridgeConfig, LLMConfig
from mcp_llm_bridge.bridge import BridgeManager
import colorlog
import logging

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s%(reset)s:     %(cyan)s%(name)s%(reset)s - %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

async def main():
    # Load environment variables
    load_dotenv()

    # Get the project root directory (where test.db is located)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(project_root, "test.db")
    
    # Configure bridge
    config = BridgeConfig(
        mcp_server_params=StdioServerParameters(
            command="uvx",
            args=["mcp-server-sqlite", "--db-path", db_path],
            env=None
        ),
        # llm_config=LLMConfig(
        #     api_key=os.getenv("OPENAI_API_KEY"),
        #     model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        #     base_url=None
        # ),
        # llm_config=LLMConfig(
        #     api_key="ollama",  # Can be any string for local testing
        #     model="mistral-nemo:12b-instruct-2407-q8_0",
        #     base_url="http://192.168.87.34:11434/v1"  # Point to your local model's endpoint
        # ),
        llm_config=LLMConfig(
            api_key="not-needed",
            model="local-model",
            base_url="http://localhost:1234/v1"
        ),
        system_prompt="You are a helpful assistant that can use tools to help answer questions."
    )
    
    logger.info(f"Starting bridge with model: {config.llm_config.model}")
    logger.info(f"Using database at: {db_path}")
    
    # Use bridge with context manager
    async with BridgeManager(config) as bridge:
        while True:
            try:
                # user_input = input("\nEnter your prompt (or 'quit' to exit): ")
                # if user_input.lower() in ['quit', 'exit', 'q']:
                #     break
                    
                # response = await bridge.process_message(user_input)
                # print(f"\nResponse: {response}")

                user_input = input("\n請輸入您的提問（輸入 'quit' 結束）：")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break

                # 強制模型使用繁體中文回答
                zh_tw_prompt = "請用繁體中文回答以下問題：" + user_input
                response = await bridge.process_message(zh_tw_prompt)
                print(f"\n回應內容（繁體中文）：{response}")
                
            except KeyboardInterrupt:
                logger.info("\nExiting...")
                break
            except Exception as e:
                logger.error(f"\nError occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
