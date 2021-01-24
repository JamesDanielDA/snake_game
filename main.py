import game_controller
import asyncio


async def main():
    game =  game_controller.GameController()
    task1 = asyncio.create_task(game.input_handler())
    task2 = asyncio.create_task(game.mainloop())
    
    await task1
    await task2

if __name__ == "__main__":
    asyncio.run(main())