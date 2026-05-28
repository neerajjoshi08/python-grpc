import asyncio

import concurrent
import concurrent.futures
import threading


async def io_bound() -> str:
    print("Hello...")
    await asyncio.sleep(5)
    return "Hello"


async def io_bound_2() -> str:
    print("Hello...")
    await asyncio.sleep(5)
    return "Hello_2"


async def coroutine() -> None:
    await io_bound()
    print("Completed")


async def coroutine_with_tasks() -> None:

    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(io_bound())
        task2 = tg.create_task(io_bound_2())

    print(f"Task completed: {task1.result()}, and {task2.result()}")


# CPU bound work
def cpu_bound_operation() -> int:
    print(f"Running with thread: {threading.current_thread().name}")
    return sum(x * x for x in range(5**2))


async def coroutine_multiprocessing() -> None:
    loop = asyncio.get_running_loop()

    with concurrent.futures.ThreadPoolExecutor(
        thread_name_prefix="custom-thread", max_workers=3
    ) as t:
        for _ in range(10):
            result1 = loop.run_in_executor(t, cpu_bound_operation)
            result2 = loop.run_in_executor(t, cpu_bound_operation)
            result3 = loop.run_in_executor(t, cpu_bound_operation)
            res1 = await result1
            res2 = await result2
            res3 = await result3
            print(f"{res1=}, {res2=}, {res3=}")


if __name__ == "__main__":
    asyncio.run(coroutine_multiprocessing())
