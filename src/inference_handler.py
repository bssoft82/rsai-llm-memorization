from rsai_logging import add_rsai_log


def get_inference(client, model, messages):
    # if not isinstance(messages, list):
    #     messages_list = [messages]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        #max_tokens=1000,
      )

    add_rsai_log(f'response: {response}')
    return response.choices[0].message

