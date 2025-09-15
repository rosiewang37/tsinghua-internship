from zhipuai import ZhipuAI
import logging
from tqdm import tqdm


logger = logging.getLogger(__name__)

class GLMModel:
    GLM_4_Plus = 'glm-4-plus'
    GLM_4_0520 = 'GLM-4-0520'

    GLM_4_AirX = 'glm-4-airx'
    GLM_4_Air = 'glm-4-air'

    GLM_4_FlashX = 'glm-4-flashx'
    GLM_4_Flash = 'glm-4-flash'


def msg(role, content):
    assert role in ['system', 'user', 'assistant']
    return {'role': role, 'content': content}


def create_client():
    api_key = '6306367a14a96d92d3910a33b6d079a8.kGYlp3ommvTt6fFu'  # KEG
    # api_key = 'e81d34e4f06d954d5e25681d05bc0b64.cXOvO0Iy1cUSZ7bI'
    return ZhipuAI(api_key=api_key)


def query(messages, model, ret_reason=True, max_tokens=1024):
    result = ''
    reason = ''
    try:
        client = create_client()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        reason = response.choices[0].finish_reason
        result = response.choices[0].message.content
    except Exception as e:
        logger.error(f'Error during query: {e}')
        if 'response' in locals():
            logger.error(f'Response: {response}')
    if ret_reason:
        return result, reason
    return result


def async_create_batch(messages_list, model, task=None):
    client = create_client()
    async_id_list = []
    n = len(messages_list)
    for idx, messages in enumerate(tqdm(messages_list)):
        try:
            response = client.chat.asyncCompletions.create(
                model=model,
                messages=messages
            )
            async_id_list.append(response.id)
        except Exception as e:
            logger.error(f'Error during async_create: {e}')
            if 'response' in locals():
                logger.error(f'Response: {response}')
            async_id_list.append(None)

        if task:
            task.progress = (idx + 1) / n
            task.save()

    return async_id_list


def async_result_batch(async_id_list):
    client = create_client()
    n = len(async_id_list)
    results = [None] * n
    finished_flags = [False if i is not None else True for i in async_id_list]
    pbar = tqdm(total=n)

    while sum(finished_flags) < n:

        for idx, async_id in enumerate(async_id_list):
            if finished_flags[idx]:
                continue

            try:
                response = client.chat.asyncCompletions.retrieve_completion_result(id=async_id)
                status = response.task_status

                if status == 'PROCESSING':
                    continue
                # print(response.usage.total_tokens)
                finished_flags[idx] = True
                pbar.update(1)
                if status == 'SUCCESS':
                    results[idx] = response.choices[0].message.content

            except Exception as e:
                logger.error(f'Error during async_result: {e}')
                if 'response' in locals():
                    logger.error(f'Reponse: {response.model_dump_json()}')

                finished_flags[idx] = True
                pbar.update(1)
    
    return results

