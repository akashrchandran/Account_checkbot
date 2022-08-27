from helper import message
import importlib as imp

def start_check(update, context):
    chat_id = update.callback_query.message.chat_id
    query = update.callback_query.data
    mod = imp.import_module(f'configs.{query}')
    # mod.test_run()
    context.job_queue.run_repeating()